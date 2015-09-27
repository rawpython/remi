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
from configuration import runtimeInstances, MULTIPLE_INSTANCE, ENABLE_FILE_CACHE, BASE_ADDRESS, HTTP_PORT_NUMBER, WEBSOCKET_PORT_NUMBER, IP_ADDR, UPDATE_INTERVAL, AUTOMATIC_START_BROWSER
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
try:
    import socketserver
except:
    import SocketServer as socketserver
import webbrowser
import struct
import binascii
from base64 import b64encode
import hashlib
from hashlib import sha1
import sys
import threading
from threading import Timer
try:
    from urllib import unquote
    from urllib import quote
except:
    from urllib.parse import unquote
    from urllib.parse import quote
    from urllib.parse import unquote_to_bytes

clients = {}
updateTimerStarted = False  # to start the update timer only once

pyLessThan3 = sys.version_info < (3,)

update_semaphore = threading.Semaphore()

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
        #print("the method '" + name + "' is not part of this instance type:" + str(rootNode))
    return val


def get_method_by_id(rootNode, _id, maxIter=5):
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
                # print(str(i))
                val = get_method_by_id(i, _id, maxIter)
                if val is not None:
                    return val
    except:
        pass
    return None


class ThreadedWebsocketServer(
        socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class WebSocketsHandler(socketserver.StreamRequestHandler):
    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def setup(self):
        global clients
        socketserver.StreamRequestHandler.setup(self)
        print('websocket connection established', self.client_address)
        self.handshake_done = False

    def handle(self):
        print('handle\n')
        while True:
            if not self.handshake_done:
                self.handshake()
            else:
                if not self.read_next_message():
                    print('ending websocket service...')
                    break
            
    def bytetonum(self,b):
        if pyLessThan3:
            b = ord(b)
        return b

    def read_next_message(self):
        print('read_next_message\n')
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
            print("Exception in server.py-read_next_message.")
            print(traceback.format_exc())
            return False
        return True

    def send_message(self, message):
        out = bytearray()
        out.append(129)
        print('send_message\n')
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
        print('handshake\n')
        data = self.request.recv(1024).strip()
        #headers = Message(StringIO(data.split(b'\r\n', 1)[1]))
        print('Handshaking...')
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
        update_semaphore.acquire()
        try:
            # saving the websocket in order to update the client
            k = self.client_address[0]
            if not MULTIPLE_INSTANCE:
                # overwrite the key value, so all clients will point the same
                # instance
                k = 0
            if not self in clients[k].websockets:
                #clients[k].websockets.clear()
                clients[k].websockets.append(self)
            print('on_message\n')
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
            print(traceback.format_exc())
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


def update_clients():
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
                        ws.send_message('show_window,' + str(id(client.root)) + ',' + toWebsocket(repr(client.root)))
                    except:
                        client.websockets.remove(ws)
            client.old_root_window = client.root
            client.idle()
            gui_updater(client, client.root)
    except Exception as e:
        print(traceback.format_exc())
    update_semaphore.release()
    Timer(UPDATE_INTERVAL, update_clients, ()).start()


def gui_updater(client, leaf, no_update_because_new_subchild=False):
    if not hasattr(leaf, 'attributes'):
        return False

    # if there is not a copy of widgets, do it
    if not hasattr(client, 'old_runtime_widgets'):
        client.old_runtime_widgets = dict()  # idWidget,reprWidget

    __id = str(id(leaf))
    # if the widget is not contained in the copy
    if not (__id in client.old_runtime_widgets.keys()):
        client.old_runtime_widgets[__id] = leaf.repr_without_children()
        if not no_update_because_new_subchild:
            no_update_because_new_subchild = True
            # we ensure that the clients have an updated version
            for ws in client.websockets:
                try:
                    #print('insert_widget: ' +  leaf.attributes['parent_widget'] + '  type: ' + str(type(leaf)))
                    #here a new widget is found, but it must be added updating the parent widget
                    if 'parent_widget' in leaf.attributes.keys():
                        parentWidgetId = leaf.attributes['parent_widget']
                        print("1" + leaf.attributes['class'] + "\n")
                        ws.send_message('update_widget,' + parentWidgetId + ',' + toWebsocket(repr(get_method_by_id(client.root,parentWidgetId))))
                    else:
                        print('the new widget seems to have no parent...')
                    #adding new widget with insert_widget causes glitches, so is preferred to update the parent widget
                    #ws.send_message('insert_widget,' + __id + ',' + parentWidgetId + ',' + repr(leaf))
                except:
                    client.websockets.remove(ws)

    # checking if subwidgets changed
    for subleaf in leaf.children.values():
        gui_updater(client, subleaf, no_update_because_new_subchild)

    if leaf.repr_without_children() != client.old_runtime_widgets[__id]:
        #client.old_runtime_widgets[__id] = repr(leaf)
        for ws in client.websockets:
            #try:
            print('update_widget: ' + __id + '  type: ' + str(type(leaf)))
            try:
                ws.send_message('update_widget,' + __id + ',' + toWebsocket(repr(leaf)))
            except:
                client.websockets.remove(ws)
        client.old_runtime_widgets[__id] = leaf.repr_without_children()
        return True
    # widget NOT changed
    return False


class App(BaseHTTPRequestHandler, WebSocketsHandler, object):

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
        """
        This method is used to get the Application instance previously created
        managing on this, it is possible to switch to "single instance for
        multiple clients" or "multiple instance for multiple clients" execution way
        """
        k = self.client_address[0]
        if not MULTIPLE_INSTANCE:
            # overwrite the key value, so all clients will point the same
            # instance
            k = 0
        if not(k in clients.keys()):
            runtimeInstances.append(self)

            clients[k] = self
            clients[
                k].attachments = "<script>\
var paramPacketize = function (ps){\
    var ret = '';\
    for (var pkey in ps) {\
        if( ret.length>0 )ret = ret + '|';\
        var pstring = pkey+'='+ps[pkey];\
        pstring = pstring.length+'|'+pstring;\
        ret = ret + pstring;\
    }\
    return ret;\
};\
var ws;\
function openSocket(){\
    try{\
        ws = new WebSocket('ws://" + IP_ADDR + ':' + str(WEBSOCKET_PORT_NUMBER) + "/'); \
        console.debug('opening websocket');\
        ws.onopen = function(evt) { \
            ws.send('Hello from the client!'); \
        }; \
    }catch(ex){ws=false;alert('websocketnot supported or server unreachable');}\
}\
openSocket();\
ws.onmessage = function (evt) { \
    var received_msg = evt.data; \
    console.debug('Message is received:' + received_msg); \
    var s = received_msg.split(',');\
    var command = s[0];\
    var index = received_msg.indexOf(',')+1;\
    received_msg = received_msg.substr(index,received_msg.length-index);/*removing the command from the message*/\
    index = received_msg.indexOf(',')+1;\
    var content = received_msg.substr(index,received_msg.length-index);\
    if( command=='show_window' ){\
        document.body.innerHTML = unescape(content);\
    }else if( command=='update_widget'){\
        var elem = document.getElementById(s[1]);\
        var index = received_msg.indexOf(',')+1;\
        elem.insertAdjacentHTML('afterend',unescape(content));\
        elem.parentElement.removeChild(elem);\
    }else if( command=='insert_widget'){\
        if( document.getElementById(s[1])==null ){\
            /*the content contains an additional field that we have to remove*/\
            index = content.indexOf(',')+1;\
            content = content.substr(index,content.length-index);\
            var elem = document.getElementById(s[2]);\
            elem.innerHTML = elem.innerHTML + unescape(content);\
        }\
    }\
    console.debug('command:' + command);\
    console.debug('content:' + content);\
}; \
/*this uses websockets*/\
var sendCallbackParam = function (widgetID,functionName,params /*a dictionary of name:value*/){\
    if (ws.readyState != WebSocket.OPEN){\
        console.debug('socket not opened');\
        openSocket();\
    }\
    ws.send(escape('callback' + '/' + widgetID+'/'+functionName + '/' + paramPacketize(params)));\
    console.debug('to client len:' + escape('callback' + '/' + widgetID+'/'+functionName + '/' + paramPacketize(params)));\
};\
/*this uses websockets*/\
var sendCallback = function (widgetID,functionName){\
    if (ws.readyState != WebSocket.OPEN){\
        console.debug('socket not opened');\
        openSocket();\
    }\
    ws.send(escape('callback' + '/' + widgetID+'/'+functionName+'/'));\
    console.debug( 'to client len:' + escape('callback' + '/' + widgetID+'/'+functionName+'/'));\
};\
ws.onclose = function(evt){ \
    /* websocket is closed. */\
    alert('Connection is closed...'); \
};\
ws.onerror = function(evt){ \
    /* websocket is closed. */\
    alert('Websocket error...'); \
};\
</script>"

        if not hasattr(clients[k], 'websockets'):
            clients[k].websockets = list()

        self.client = clients[k]

        if updateTimerStarted == False:
            updateTimerStarted = True
            Timer(UPDATE_INTERVAL, update_clients, ()).start()

    def idle(self):
        """ Idle function called every UPDATE_INTERVAL before the gui update.
            Usefull to schedule tasks. """
        pass

    def do_POST(self):
        self.instance()
        varLen = int(self.headers['Content-Length'])
        postVars = self.rfile.read(varLen)
        postVars = str(unquote(postVars))
        paramDict = parse_parametrs(postVars)
        function = str(unquote(self.path))
        self.process_all(function, paramDict, True)

    def do_GET(self):
        """Handler for the GET requests."""
        self.instance()
        params = str(unquote(self.path))

        params = params.split('?')
        function = params[0]

        function = function[1:]
        self.process_all(function, dict(), False)

        return

    def process_all(self, function, paramDict, isPost):
        encoding='latin-1'
        ispath = True
        snake = None
        doNotCallMain = False
        if len(function.split('/')) > 1:
            for attr in function.split('/'):
                if len(attr) == 0:
                    continue
                if ispath == False:
                    break
                if snake is None:
                    snake = get_method_by(self.client.root, attr)
                    ispath = ispath and (None != snake)
                    continue
                snake = get_method_by(snake, attr)
                ispath = ispath and (None != snake)
        else:
            function = function.replace('/', '')
            if len(function) > 0:
                snake = get_method_by(self.client, function)
                ispath = ispath and (None != snake)
            else:
                doNotCallMain = hasattr(self.client, 'root')
                ispath = True
                snake = self.main

        if ispath:
            ret = None
            if not doNotCallMain:
                ret = snake(**paramDict)

                # setting up the root widget, if the 'ret' becomes from the
                # main call
                if snake == self.main:
                    self.client.root = ret
                    ret = None

            if ret is None:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(encodeIfPyGT3(
                    "<link href='" +
                    BASE_ADDRESS +
                    "style.css' rel='stylesheet' /><meta content='text/html;charset=utf-8' http-equiv='Content-Type'><meta content='utf-8' http-equiv='encoding'> "))
                self.wfile.write(encodeIfPyGT3(self.client.attachments))
                self.wfile.write(encodeIfPyGT3(repr(self.client.root)))
            else:
                # here is the function that should return the content type
                self.send_response(200)
                self.send_header('Content-type', ret[1])

                self.end_headers()

                # if is requested a widget, but not by post, so we suppose is
                # requested to show a new page, we attach javascript and style
                if(ret[1] == 'text/html' and isPost == False):
                    self.wfile.write(encodeIfPyGT3(
                        "<link href='" +
                        BASE_ADDRESS +
                        "style.css' rel='stylesheet' /><meta content='text/html;charset=utf-8' http-equiv='Content-Type'><meta content='utf-8' http-equiv='encoding'> "))
                    self.wfile.write(encodeIfPyGT3(self.client.attachments))
                self.wfile.write(encodeIfPyGT3(ret[0]))

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            if ENABLE_FILE_CACHE:
                self.send_header('Cache-Control', 'public, max-age=86400')
            self.end_headers()
            filename = './' + function
            try:
                f = open(filename, 'r+b')
                content = b''.join(f.readlines())
                f.close()
                self.wfile.write(content)
            except:
                print('Managed exception in server.py - App.process_all. The requested file was not found or cannot be opened ',filename)
                #print(traceback.format_exc())



class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):

    """This class allows to handle requests in separated threads.

    No further content needed, don't touch this.

    """


def start(mainGuiClass):
    """This method starts the webserver with a specific App subclass."""
    try:
        # here the websocket is started
        wsserver = ThreadedWebsocketServer(
            (IP_ADDR, WEBSOCKET_PORT_NUMBER), WebSocketsHandler)
        th = threading.Thread(target=wsserver.serve_forever)
        th.setDaemon(True)
        th.start()
        
        # Create a web server and define the handler to manage the incoming
        # request
        server = ThreadedHTTPServer(('', HTTP_PORT_NUMBER), mainGuiClass)
        print('Started httpserver on port ', HTTP_PORT_NUMBER)
        if AUTOMATIC_START_BROWSER:
            try:
                import android
                android.webbrowser.open(BASE_ADDRESS)
            except:
                webbrowser.open(BASE_ADDRESS)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
