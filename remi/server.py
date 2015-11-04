#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import traceback
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
try:
    import socketserver
except:
    import SocketServer as socketserver
import mimetypes
import webbrowser
import struct
from base64 import b64encode
import hashlib
import sys
import threading
import signal
import time
import os
import re
from threading import Timer
try:
    from urllib import unquote
    from urllib import quote
except:
    from urllib.parse import unquote
    from urllib.parse import quote
    from urllib.parse import unquote_to_bytes
import cgi

clients = {}
runtimeInstances = []

updateTimerStarted = False  # to start the update timer only once

pyLessThan3 = sys.version_info < (3,)

update_semaphore = threading.Semaphore()

DEBUG_MODE = 0 #0 - NO DEBUG  1 - ALERTS AND ERRORS  2 - MESSAGES
DEBUG_ALERT_ERR = 1
DEBUG_MESSAGE = 2


def debug_message(*args, **kwargs):
    if DEBUG_MESSAGE <= DEBUG_MODE:
        print( ''.join(map(lambda v: str(v),args)) )
        
        
def debug_alert(*args, **kwargs):
    if DEBUG_ALERT_ERR <= DEBUG_MODE:
        print( ''.join(map(lambda v: str(v),args)) )


def toWebsocket(data):
    #encoding end deconding utility function
    if pyLessThan3:
        return quote(data)
    return quote(data,encoding='latin-1')
        
        
def fromWebsocket(data):
    #encoding end deconding utility function
    if pyLessThan3:
        return unquote(data)
    return unquote(data,encoding='latin-1')


def encodeIfPyGT3(data):
    if not pyLessThan3:
        data = data.encode('latin-1')
    return data


def get_method_by(rootNode, idname):
    if idname.isdigit():
        return get_method_by_id(rootNode, idname)
    return get_method_by_name(rootNode, idname)


def get_method_by_name(rootNode, name, maxIter=5):
    val = None
    if hasattr(rootNode, name):
        val = getattr(rootNode, name)
    else:
        pass
    return val


def get_method_by_id(rootNode, _id, maxIter=5):
    global runtimeInstances
    for i in runtimeInstances:
        if id(i) == _id:
            return i

    maxIter = maxIter - 1
    if maxIter < 0:
        return None
    _id = int(_id)

    if id(rootNode) == _id:
        return rootNode

    try:
        if hasattr(rootNode, 'children'):
            for i in rootNode.children.values():
                val = get_method_by_id(i, _id, maxIter)
                if val is not None:
                    return val
    except:
        pass
    return None


def get_instance_key(handler):
    if not handler.server.multiple_instance:
        # overwrite the key value, so all clients will point the same
        # instance
        return 0
    ip = handler.client_address[0]
    unique_port = getattr(handler.server,'websocket_address', handler.server.server_address)[1]
    return ip, unique_port


class ThreadedWebsocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass, multiple_instance):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.multiple_instance = multiple_instance


class WebSocketsHandler(socketserver.StreamRequestHandler):
    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def setup(self):
        global clients
        socketserver.StreamRequestHandler.setup(self)
        debug_message('websocket connection established', self.client_address)
        self.handshake_done = False

    def handle(self):
        debug_message('handle\n')
        while True:
            if not self.handshake_done:
                self.handshake()
            else:
                if not self.read_next_message():
                    debug_message('ending websocket service...')
                    break
            
    def bytetonum(self,b):
        if pyLessThan3:
            b = ord(b)
        return b

    def read_next_message(self):
        debug_message('read_next_message\n')
        length = self.rfile.read(2)
        try:
            length = self.bytetonum(length[1]) & 127
            if length == 126:
                length = struct.unpack('>H', self.rfile.read(2))[0]
            elif length == 127:
                length = struct.unpack('>Q', self.rfile.read(8))[0]
            masks = [self.bytetonum(byte) for byte in self.rfile.read(4)]
            decoded = ''
            for char in self.rfile.read(length):
                decoded += chr(self.bytetonum(char) ^ masks[len(decoded) % 4])
            self.on_message(fromWebsocket(decoded))
        except Exception as e:
            if DEBUG_MODE:
                debug_alert("Exception in server.py-read_next_message.")
                debug_alert(traceback.format_exc())
            return False
        return True

    def send_message(self, message):
        out = bytearray()
        out.append(129)
        debug_message('send_message\n')
        length = len(message)
        if length <= 125:
            out.append(length)
        elif length >= 126 and length <= 65535:
            out.append(126)
            out = out + struct.pack('>H', length)
        else:
            out.append(127)
            out = out + struct.pack('>Q', length)
        if not pyLessThan3:
            message = message.encode('utf-8')#'ascii',errors='replace')
        out = out + message
        self.request.send(out)

    def handshake(self):
        debug_message('handshake\n')
        data = self.request.recv(1024).strip()
        #headers = Message(StringIO(data.split(b'\r\n', 1)[1]))
        debug_message('Handshaking...')
        key = data.decode().split('Sec-WebSocket-Key: ')[1].split('\r\n')[0] #headers['Sec-WebSocket-Key']
        #key = key
        digest = hashlib.sha1((key.encode("utf-8")+self.magic))
        digest = digest.digest()
        digest = b64encode(digest)
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest.decode("utf-8")
        self.request.sendall(response.encode("utf-8"))
        self.handshake_done = True

    def on_message(self, message):
        global update_semaphore
        global runtimeInstances
        update_semaphore.acquire()

        try:
            # saving the websocket in order to update the client
            k = get_instance_key(self)
            if not self in clients[k].websockets:
                #clients[k].websockets.clear()
                clients[k].websockets.append(self)
            debug_message('on_message\n')
            #print('recv from websocket client: ' + str(message))

            # parsing messages
            chunks = message.split('/')
            if len(chunks) > 3:  # msgtype,widget,function,params
                # if this is a callback
                msgType = 'callback'
                if chunks[0] == msgType:
                    widgetID = chunks[1]
                    functionName = chunks[2]
                    params = message[
                        len(msgType) + len(widgetID) + len(functionName) + 3:]

                    paramDict = parse_parametrs(params)
                    #print('msgType: ' + msgType + ' widgetId: ' + widgetID +
                    #      ' function: ' + functionName + ' params: ' + str(params))

                    for w in runtimeInstances:
                        if str(id(w)) == widgetID:
                            callback = get_method_by_name(w, functionName)
                            if callback is not None:
                                callback(**paramDict)
        except Exception as e:
            debug_alert(traceback.format_exc())
        update_semaphore.release()


def parse_parametrs(p):
    """
    Parses the parameters given from POST or websocket reqs
    expecting the parameters as:  "11|par1='asd'|6|par2=1"
    returns a dict like {par1:'asd',par2:1}
    """
    ret = dict()
    while len(p) > 1 and p.count('|') > 0:
        s = p.split('|')
        l = int(s[0])  # length of param field
        if l > 0:
            p = p[len(s[0]) + 1:]
            fieldName = p.split('|')[0].split('=')[0]
            fieldValue = p[len(fieldName) + 1:l]
            p = p[l + 1:]
            if fieldValue.count("'") == 0 and fieldValue.count('"') == 0:
                if fieldValue.count('.') == 1 and fieldValue.replace('.','').isdigit():
                    fieldValue = float(fieldValue)
                if fieldValue.isdigit():
                    fieldValue = int(fieldValue)
            ret[fieldName] = fieldValue
    return ret


def update_clients(update_interval):
    global clients
    global update_semaphore
    update_semaphore.acquire()
    try:
        for client in clients.values():
            #here we check if the root window has changed
            if not hasattr(client,'old_root_window') or client.old_root_window != client.root:
                #a new window is shown, clean the old_runtime_widgets
                client.old_runtime_widgets = dict()
                for ws in client.websockets:
                    try:
                        html = client.root.repr(client)
                        ws.send_message('show_window,' + str(id(client.root)) + ',' + toWebsocket(html))
                    except:
                        client.websockets.remove(ws)
            client.old_root_window = client.root
            client.idle()
            gui_updater(client, client.root)
    except Exception as e:
        debug_alert(traceback.format_exc())
    update_semaphore.release()
    Timer(update_interval, update_clients, (update_interval,)).start()


def gui_updater(client, leaf, no_update_because_new_subchild=False):
    if not hasattr(leaf, 'attributes'):
        return False

    # if there is not a copy of widgets, do it
    if not hasattr(client, 'old_runtime_widgets'):
        client.old_runtime_widgets = dict()  # idWidget,reprWidget

    __id = str(id(leaf))
    # if the widget is not contained in the copy
    if not (__id in client.old_runtime_widgets.keys()):
        client.old_runtime_widgets[__id] = leaf.repr(client,False)
        if not no_update_because_new_subchild:
            no_update_because_new_subchild = True
            # we ensure that the clients have an updated version
            for ws in client.websockets:
                try:
                    #print('insert_widget: ' +  leaf.attributes['parent_widget'] + '  type: ' + str(type(leaf)))
                    #here a new widget is found, but it must be added updating the parent widget
                    if 'parent_widget' in leaf.attributes.keys():
                        parentWidgetId = leaf.attributes['parent_widget']
                        debug_message("1" + leaf.attributes['class'] + "\n")
                        html = get_method_by_id(client.root,parentWidgetId).repr(client)
                        ws.send_message('update_widget,' + parentWidgetId + ',' + toWebsocket(html))
                    else:
                        debug_alert('the new widget seems to have no parent...')
                    #adding new widget with insert_widget causes glitches, so is preferred to update the parent widget
                    #ws.send_message('insert_widget,' + __id + ',' + parentWidgetId + ',' + repr(leaf))
                except:
                    client.websockets.remove(ws)

    # checking if subwidgets changed
    for subleaf in leaf.children.values():
        gui_updater(client, subleaf, no_update_because_new_subchild)

    newhtml = leaf.repr(client,False)
    if newhtml != client.old_runtime_widgets[__id]:
        #client.old_runtime_widgets[__id] = repr(leaf)
        for ws in client.websockets:
            #try:
            debug_message('update_widget: ' + __id + '  type: ' + str(type(leaf)))
            try:
                html = leaf.repr(client)
                ws.send_message('update_widget,' + __id + ',' + toWebsocket(html))
            except:
                client.websockets.remove(ws)
        client.old_runtime_widgets[__id] = newhtml
        return True
    # widget NOT changed
    return False


class App(BaseHTTPRequestHandler, object):

    """
    This class will handles any incoming request from the browser
    The main application class can subclass this
    In the do_POST and do_GET methods it is expected to receive requests such as:
        - function calls with parameters
        - file requests
    """

    def instance(self):
        global clients
        global updateTimerStarted
        global runtimeInstances
        """
        This method is used to get the Application instance previously created
        managing on this, it is possible to switch to "single instance for
        multiple clients" or "multiple instance for multiple clients" execution way
        """
        k = get_instance_key(self)
        if not(k in clients.keys()):
            runtimeInstances.append(self)
            clients[k] = self
        wshost, wsport = self.server.websocket_address
        net_interface_ip = self.connection.getsockname()[0]

        #refreshing the script every instance() call, beacuse of different net_interface_ip connections
        #can happens for the same 'k'
        clients[k].attachments = """
<script>
var paramPacketize = function (ps){
    var ret = '';
    for (var pkey in ps) {
        if( ret.length>0 )ret = ret + '|';
        var pstring = pkey+'='+ps[pkey];
        pstring = pstring.length+'|'+pstring;
        ret = ret + pstring;
    }
    return ret;
};
var ws;
function openSocket(){
    try{
        ws = new WebSocket('ws://%s:%s/');
        console.debug('opening websocket');
        ws.onopen = function(evt) {
            ws.send('Hello from the client!');
        };
    }catch(ex){ws=false;alert('websocketnot supported or server unreachable');}
}
openSocket();
ws.onmessage = function (evt) {
    var received_msg = evt.data;
    console.debug('Message is received:' + received_msg);
    var s = received_msg.split(',');
    var command = s[0];
    var index = received_msg.indexOf(',')+1;
    received_msg = received_msg.substr(index,received_msg.length-index);/*removing the command from the message*/
    index = received_msg.indexOf(',')+1;
    var content = received_msg.substr(index,received_msg.length-index);
    if( command=='show_window' ){
        document.body.innerHTML = unescape(content);
    }else if( command=='update_widget'){
        var elem = document.getElementById(s[1]);
        var index = received_msg.indexOf(',')+1;
        elem.insertAdjacentHTML('afterend',unescape(content));
        elem.parentElement.removeChild(elem);
    }else if( command=='insert_widget'){
        if( document.getElementById(s[1])==null ){
            /*the content contains an additional field that we have to remove*/
            index = content.indexOf(',')+1;
            content = content.substr(index,content.length-index);
            var elem = document.getElementById(s[2]);
            elem.innerHTML = elem.innerHTML + unescape(content);
        }
    }
    console.debug('command:' + command);
    console.debug('content:' + content);
};
/*this uses websockets*/
var sendCallbackParam = function (widgetID,functionName,params /*a dictionary of name:value*/){
    if (ws.readyState != WebSocket.OPEN){
        console.debug('socket not opened');
        openSocket();
    }
    ws.send(escape('callback' + '/' + widgetID+'/'+functionName + '/' + paramPacketize(params)));
    console.debug('to client len:' + escape('callback' + '/' + widgetID+'/'+functionName + '/' + paramPacketize(params)));
};
/*this uses websockets*/
var sendCallback = function (widgetID,functionName){
    if (ws.readyState != WebSocket.OPEN){
        console.debug('socket not opened');
        openSocket();
    }
    ws.send(escape('callback' + '/' + widgetID+'/'+functionName+'/'));
    console.debug( 'to client len:' + escape('callback' + '/' + widgetID+'/'+functionName+'/'));
};
ws.onclose = function(evt){
    /* websocket is closed. */
    alert('Connection is closed...');
};
ws.onerror = function(evt){
    /* websocket is closed. */
    alert('Websocket error...');
};
</script>""" % (net_interface_ip, wsport)

        if not hasattr(clients[k], 'websockets'):
            clients[k].websockets = list()

        self.client = clients[k]

        if updateTimerStarted == False:
            updateTimerStarted = True
            Timer(self.server.update_interval, update_clients, (self.server.update_interval,)).start()

    def idle(self):
        """ Idle function called every UPDATE_INTERVAL before the gui update.
            Usefull to schedule tasks. """
        pass

    def do_POST(self):
        self.instance()
        file_data = None
        try:
            # Parse the form data posted
            savepath = self.headers['savepath']
            filename = self.headers['filename']
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                        })
            # Echo back information about what was posted in the form
            for field in form.keys():
                field_item = form[field]
                if field_item.filename:
                    # The field contains an uploaded file
                    file_data = field_item.file.read()
                    file_len = len(file_data)
                    #print('FILE DATA: ' + str(file_data))
                    debug_message('\tUploaded %s as "%s" (%d bytes)\n' % \
                            (field, field_item.filename, file_len))
                else:
                    # Regular form value
                    debug_message('\t%s=%s\n' % (field, form[field].value))

            if file_data!=None: #self.path=='/fileupload':
                debug_message('GUI - server.py do_POST: fileupload path=' + savepath + '   name=' + filename)
                with open(savepath+filename,'wb') as f:
                    f.write(file_data)
                    self.send_response(200)
        except Exception as e:
            debug_alert(traceback.format_exc())
            self.send_response(400)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        """Handler for the GET requests."""
        self.instance()
        path = str(unquote(self.path))
        self.process_all(path)
        return

    def process_all(self, function):
        static_file = re.match(r"^/*res\/(.*)$", function)
        attr_call = re.match(r"^\/*(\w+)\/(\w+)$", function)
        if (function == '/') or (not function):
            # build the root page once if necessary
            should_call_main = not hasattr(self.client, 'root')
            if should_call_main:
                self.client.root = self.main(*self.server.userdata)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(encodeIfPyGT3(
                "<link href='/res/style.css' rel='stylesheet' /><meta content='text/html;charset=utf-8' http-equiv='Content-Type'><meta content='utf-8' http-equiv='encoding'> "))
            self.wfile.write(encodeIfPyGT3(self.client.attachments))
            # render the HTML replacing any local absolute references to the correct IP of this instance
            html = self.client.root.repr(self.client)
            self.wfile.write(encodeIfPyGT3(html))
        elif static_file:
            filename = os.path.join(os.path.dirname(__file__), 'res', static_file.groups()[0])
            if not os.path.exists(filename):
                self.send_response(404)
                return

            mimetype,encoding = mimetypes.guess_type(filename)
            self.send_response(200)
            self.send_header('Content-type', mimetype if mimetype else 'application/octet-stream')
            if self.server.enable_file_cache:
                self.send_header('Cache-Control', 'public, max-age=86400')
            self.end_headers()
            with open(filename, 'rb') as f:
                content = f.read()
                self.wfile.write(content)
        elif attr_call:
            widget,function = attr_call.groups()
            try:
                content,headers = get_method_by(get_method_by(self.client.root, widget), function)()
                self.send_response(200)
            except IOError:
                self.send_response(404)
                return

            for k in headers.keys():
                self.send_header(k, headers[k])
            self.end_headers()
            self.wfile.write(content)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):

    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass, websocket_address, multiple_instance, enable_file_cache, update_interval, *userdata):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.websocket_address = websocket_address
        self.multiple_instance = multiple_instance
        self.enable_file_cache = enable_file_cache
        self.update_interval = update_interval
        self.userdata = userdata


class Server(object):
    def __init__(self, gui_class, start=True, address='127.0.0.1', port=8081, multiple_instance=False,
                 enable_file_cache=True, update_interval=0.1, start_browser=True, userdata=()):
        self._gui = gui_class
        self._wsserver = self._sserver = None
        self._wsth = self._sth = None
        self._address = address
        self._sport = port
        self._multiple_instance = multiple_instance
        self._enable_file_cache = enable_file_cache
        self._update_interval = update_interval
        self._start_browser = start_browser

        if not isinstance(userdata, tuple):
            raise ValueError('userdata must be a tuple')

        if start:
            self.start(*userdata)

    def start(self, *userdata):
        # here the websocket is started on an ephemereal port
        self._wsserver = ThreadedWebsocketServer((self._address, 0), WebSocketsHandler, self._multiple_instance)
        wshost, wsport = self._wsserver.socket.getsockname()[:2]
        debug_message('Started websocket server %s:%s' % (wshost, wsport))
        self._wsth = threading.Thread(target=self._wsserver.serve_forever)
        self._wsth.daemon = True
        self._wsth.start()
        
        # Create a web server and define the handler to manage the incoming
        # request
        self._sserver = ThreadedHTTPServer((self._address, self._sport), self._gui,
                                           (wshost, wsport), self._multiple_instance, self._enable_file_cache,
                                           self._update_interval, *userdata)
        shost, sport = self._sserver.socket.getsockname()[:2]
        #when listening on multiple net interfaces the browsers connects to localhost
        if shost=='0.0.0.0':
            shost = '127.0.0.1'
        base_address = 'http://%s:%s/' % (shost,sport)
        debug_message('Started httpserver %s' % base_address)
        if self._start_browser:
            try:
                import android
                android.webbrowser.open(base_address)
            except:
                # use default browser instead of always forcing IE on Windows
                if os.name == 'nt':
                    webbrowser.get('windows-default').open('file://' + os.path.realpath(base_address))
                else:
                    webbrowser.open(base_address)
        self._sth = threading.Thread(target=self._sserver.serve_forever)
        self._sth.daemon = True
        self._sth.start()

    def serve_forever(self):
        # we could join on the threads, but join blocks all interupts (including
        # ctrl+c, so just spin here
        try:
            while True:
                signal.pause()
        except Exception:
            # signal.pause() is missing for Windows; wait 1ms and loop instead
            while True:
                time.sleep(1)

    def stop(self):
        self._wsserver.shutdown()
        self._wsth.join()
        self._sserver.shutdown()
        self._sth.join()


def start(mainGuiClass, **kwargs):
    """This method starts the webserver with a specific App subclass."""
    s = Server(mainGuiClass, start=True, **kwargs)
    s.serve_forever()

