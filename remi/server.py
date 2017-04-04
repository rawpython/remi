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
import logging
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
import socket
import base64
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
    from urlparse import urlparse
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import unquote
    from urllib.parse import quote
    from urllib.parse import unquote_to_bytes
    from urllib.parse import urlparse
    from urllib.parse import parse_qs
import cgi
import weakref

clients = {}
runtimeInstances = weakref.WeakValueDictionary()

pyLessThan3 = sys.version_info < (3,)

update_lock = threading.RLock()
update_event = threading.Event()
update_thread = None


_MSG_PING = '4'
_MSG_ACK = '3'
_MSG_JS = '2'
_MSG_UPDATE = '1'

def to_websocket(data):
    # encoding end decoding utility function
    if pyLessThan3:
        return quote(data)
    return quote(data, encoding='utf-8')


def from_websocket(data):
    # encoding end deconding utility function
    if pyLessThan3:
        return unquote(data)
    return unquote(data, encoding='utf-8')


def encode_text(data):
    if not pyLessThan3:
        return data.encode('utf-8')
    return data


def get_method_by_name(root_node, name):
    val = None
    if hasattr(root_node, name):
        val = getattr(root_node, name)
    return val


def get_method_by_id(_id):
    global runtimeInstances
    if str(_id) in runtimeInstances:
        return runtimeInstances[str(_id)]
    return None


def get_instance_key(handler):
    if not handler.server.multiple_instance:
        # overwrite the key value, so all clients will point the same
        # instance
        return 0
    ip = handler.client_address[0]
    unique_port = getattr(handler.server, 'websocket_address', handler.server.server_address)[1]
    return ip, unique_port


# noinspection PyPep8Naming
class ThreadedWebsocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass, multiple_instance):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.multiple_instance = multiple_instance


class WebSocketsHandler(socketserver.StreamRequestHandler):

    magic = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    timeout = 10

    def __init__(self, *args, **kwargs):
        self.last_ping = time.time()
        self.handshake_done = False
        self._log = logging.getLogger('remi.server.ws')
        socketserver.StreamRequestHandler.__init__(self, *args, **kwargs)

    def setup(self):
        global clients
        socketserver.StreamRequestHandler.setup(self)
        self._log.info('connection established: %r' % (self.client_address,))
        self.handshake_done = False

    def handle(self):
        self._log.debug('handle')
        # on some systems like ROS, the default socket timeout
        # is less than expected, we force it to infinite (None) as default socket value
        self.request.settimeout(None)
        while True:
            if not self.handshake_done:
                self.handshake()
            else:
                if not self.read_next_message():
                    k = get_instance_key(self)
                    clients[k].websockets.remove(self)
                    self.handshake_done = False
                    self._log.debug('ws ending websocket service')
                    break

    @staticmethod
    def bytetonum(b):
        if pyLessThan3:
            b = ord(b)
        return b

    def read_next_message(self):
        # noinspection PyBroadException
        try:
            length = self.rfile.read(2)
            length = self.bytetonum(length[1]) & 127
            if length == 126:
                length = struct.unpack('>H', self.rfile.read(2))[0]
            elif length == 127:
                length = struct.unpack('>Q', self.rfile.read(8))[0]
            masks = [self.bytetonum(byte) for byte in self.rfile.read(4)]
            decoded = ''
            for char in self.rfile.read(length):
                decoded += chr(self.bytetonum(char) ^ masks[len(decoded) % 4])
            self.on_message(from_websocket(decoded))
        except socket.timeout as e:
            self._log.debug('socket timed out: %s' % e)
            return False
        except Exception:
            self._log.error("error parsing websocket", exc_info=True)
            return False
        return True

    def ping(self):
        t = time.time()
        if (t - self.last_ping) > (0.5*self.timeout):
            self.last_ping = t
            self.send_message(_MSG_PING)

    def send_message(self, message):
        if not self.handshake_done:
            self._log.warning("ignoring message %s (handshake not done)" % message[:10])

        if message != _MSG_PING:
            self._log.debug('send_message: %s... -> %s' % (message[:10], self.client_address))
        out = bytearray()
        out.append(129)
        length = len(message)
        if length <= 125:
            out.append(length)
        elif 126 <= length <= 65535:
            out.append(126)
            out += struct.pack('>H', length)
        else:
            out.append(127)
            out += struct.pack('>Q', length)
        if not pyLessThan3:
            message = message.encode('utf-8')
        out = out + message
        self.request.send(out)

    def handshake(self):
        self._log.debug('handshake')
        data = self.request.recv(1024).strip()
        key = data.decode().split('Sec-WebSocket-Key: ')[1].split('\r\n')[0]
        digest = hashlib.sha1((key.encode("utf-8")+self.magic))
        digest = digest.digest()
        digest = base64.b64encode(digest)
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest.decode("utf-8")
        self._log.info('handshake complete')
        self.request.sendall(response.encode("utf-8"))
        self.handshake_done = True

    def on_message(self, message):
        global runtimeInstances
        global update_lock, update_event

        if message == 'pong':
            return

        self.send_message(_MSG_ACK)

        with update_lock:
            # noinspection PyBroadException
            try:
                # saving the websocket in order to update the client
                k = get_instance_key(self)
                if self not in clients[k].websockets:
                    clients[k].websockets.append(self)

                # parsing messages
                chunks = message.split('/')
                self._log.debug('on_message: %s' % chunks[0])

                if len(chunks) > 3:  # msgtype,widget,function,params
                    # if this is a callback
                    msg_type = 'callback'
                    if chunks[0] == msg_type:
                        widget_id = chunks[1]
                        function_name = chunks[2]
                        params = message[
                            len(msg_type) + len(widget_id) + len(function_name) + 3:]

                        param_dict = parse_parametrs(params)

                        callback = get_method_by_name(runtimeInstances[widget_id], function_name)
                        if callback is not None:
                            callback(**param_dict)

            except Exception:
                self._log.error('error parsing websocket', exc_info=True)

        update_event.set()


def parse_parametrs(p):
    """
    Parses the parameters given from POST or websocket reqs
    expecting the parameters as:  "11|par1='asd'|6|par2=1"
    returns a dict like {par1:'asd',par2:1}
    """
    ret = {}
    while len(p) > 1 and p.count('|') > 0:
        s = p.split('|')
        l = int(s[0])  # length of param field
        if l > 0:
            p = p[len(s[0]) + 1:]
            field_name = p.split('|')[0].split('=')[0]
            field_value = p[len(field_name) + 1:l]
            p = p[l + 1:]
            ret[field_name] = field_value
    return ret


class _UpdateThread(threading.Thread):

    daemon = True

    def __init__(self, interval):
        threading.Thread.__init__(self)
        self._interval = interval
        self._log = logging.getLogger('remi.update')
        self.start()

    def _update_gui(self, client, node):
        changed_widgets = {}  # key = widget instance, value = html representation
        node.repr(client, changed_widgets)
        for widget in changed_widgets.keys():
            html = changed_widgets[widget]
            __id = str(widget.identifier)
            for ws in client.websockets:
                self._log.debug('update_widget: %s type: %s' % (__id, type(widget)))
                try:
                    ws.send_message(_MSG_UPDATE + __id + ',' + to_websocket(html))
                except:
                    client.websockets.remove(ws)

    def run(self):
        while True:
            global clients, runtimeInstances
            global update_lock, update_event

            update_event.wait(self._interval)
            with update_lock:
                # noinspection PyBroadException
                try:

                    for client in clients.values():
                        if not hasattr(client, 'root'):
                            continue

                        if client.websockets:
                            self._update_gui(client, client.root)

                            for ws in client.websockets:
                                ws.ping()

                        client.idle()

                except Exception:
                    self._log.error('error updating gui', exc_info=True)

                update_event.clear()


# noinspection PyPep8Naming
class App(BaseHTTPRequestHandler, object):

    """
    This class will handles any incoming request from the browser
    The main application class can subclass this
    In the do_POST and do_GET methods it is expected to receive requests such as:
        - function calls with parameters
        - file requests
    """

    re_static_file = re.compile(r"^/res/([-_. \w\d]+)\?{0,1}(?:[\w\d]*)")  # https://regex101.com/r/uK1sX1/1
    re_attr_call = re.compile(r"^/*(\w+)\/(\w+)\?{0,1}(\w*\={1}(\w|\.)+\&{0,1})*$")

    def __init__(self, request, client_address, server, **app_args):
        self._app_args = app_args
        self.client = None
        self._log = logging.getLogger('remi.request')
        super(App, self).__init__(request, client_address, server)

    def _get_list_from_app_args(self, name):
        try:
            v = self._app_args[name]
            if isinstance(v, (tuple, list)):
                vals = v
            else:
                vals = [v]
        except KeyError:
            vals = []
        return vals

    def log_message(self, format_string, *args):
        msg = format_string % args
        self._log.debug("%s %s" % (self.address_string(), msg))

    def log_error(self, format_string, *args):
        msg = format_string % args
        self._log.error("%s %s" % (self.address_string(), msg))

    def _instance(self):
        global clients
        global runtimeInstances
        global update_event, update_thread
        """
        This method is used to get the Application instance previously created
        managing on this, it is possible to switch to "single instance for
        multiple clients" or "multiple instance for multiple clients" execution way
        """
        k = get_instance_key(self)
        if not(k in clients):
            runtimeInstances[str(id(self))] = self
            clients[k] = self
        wshost, wsport = self.server.websocket_address

        net_interface_ip = self.connection.getsockname()[0]
        if self.server.host_name is not None:
            net_interface_ip = self.server.host_name

        websocket_timeout_timer_ms = str(self.server.websocket_timeout_timer_ms)
        pending_messages_queue_length = str(self.server.pending_messages_queue_length)

        # refreshing the script every instance() call, beacuse of different net_interface_ip connections
        # can happens for the same 'k'
        clients[k].js_body_end = """
<script>
// from http://stackoverflow.com/questions/5515869/string-length-in-bytes-in-javascript
// using UTF8 strings I noticed that the javascript .length of a string returned less
// characters than they actually were
var pendingSendMessages = [];
var ws = null;
var comTimeout = null;
var failedConnections = 0;

function byteLength(str) {
  // returns the byte length of an utf8 string
  var s = str.length;
  for (var i=str.length-1; i>=0; i--) {
    var code = str.charCodeAt(i);
    if (code > 0x7f && code <= 0x7ff) s++;
    else if (code > 0x7ff && code <= 0xffff) s+=2;
    if (code >= 0xDC00 && code <= 0xDFFF) i--; //trail surrogate
  }
  return s;
}

var paramPacketize = function (ps){
    var ret = '';
    for (var pkey in ps) {
        if( ret.length>0 )ret = ret + '|';
        var pstring = pkey+'='+ps[pkey];
        var pstring_length = byteLength(pstring);
        pstring = pstring_length+'|'+pstring;
        ret = ret + pstring;
    }
    return ret;
};

function openSocket(){
    try{
        ws = new WebSocket('ws://%s:%s/');
        console.debug('opening websocket');
        ws.onopen = websocketOnOpen;
        ws.onmessage = websocketOnMessage;
        ws.onclose = websocketOnClose;
        ws.onerror = websocketOnError;
    }catch(ex){ws=false;alert('websocketnot supported or server unreachable');}
}

openSocket();

function websocketOnMessage (evt){
    var received_msg = evt.data;

    if( received_msg[0]=='0' ){ /*show_window*/
        var index = received_msg.indexOf(',')+1;
        /*var idRootNodeWidget = received_msg.substr(0,index-1);*/
        var content = received_msg.substr(index,received_msg.length-index);

        document.body.innerHTML = '<div id="loading" style="display: none;"><div id="loading-animation"></div></div>';
        document.body.innerHTML += decodeURIComponent(content);
    }else if( received_msg[0]=='1' ){ /*update_widget*/
        var focusedElement = document.activeElement.id;
        var index = received_msg.indexOf(',')+1;
        var idElem = received_msg.substr(1,index-2);
        var content = received_msg.substr(index,received_msg.length-index);

        var elem = document.getElementById(idElem);
        elem.insertAdjacentHTML('afterend',decodeURIComponent(content));
        elem.parentElement.removeChild(elem);

        var elemToFocus = document.getElementById(focusedElement);
        if( elemToFocus != null ){
            document.getElementById(focusedElement).focus();
        }
    }else if( received_msg[0]=='2' ){ /*javascript*/
        var content = received_msg.substr(1,received_msg.length-1);
        try{
            eval(content);
        }catch(e){console.debug(e.message);};
    }else if( received_msg[0]=='3' ){ /*ack*/
        pendingSendMessages.shift() /*remove the oldest*/
        if(comTimeout!=null)clearTimeout(comTimeout);
    }else if( received_msg[0]=='4' ){ /*ping*/
        ws.send('pong');
    }
};

/*this uses websockets*/
var sendCallbackParam = function (widgetID,functionName,params /*a dictionary of name:value*/){
    var paramStr = '';
    if(params!=null) paramStr=paramPacketize(params);
    var message = encodeURIComponent(unescape('callback' + '/' + widgetID+'/'+functionName + '/' + paramStr));
    pendingSendMessages.push(message);
    if( pendingSendMessages.length < %s ){
        ws.send(message);
        if(comTimeout==null)
            comTimeout = setTimeout(checkTimeout, %s);
    }else{
        console.debug('Renewing connection, ws.readyState when trying to send was: ' + ws.readyState)
        renewConnection();
    }
};

/*this uses websockets*/
var sendCallback = function (widgetID,functionName){
    sendCallbackParam(widgetID,functionName,null);
};

function renewConnection(){
    // ws.readyState:
    //A value of 0 indicates that the connection has not yet been established.
    //A value of 1 indicates that the connection is established and communication is possible.
    //A value of 2 indicates that the connection is going through the closing handshake.
    //A value of 3 indicates that the connection has been closed or could not be opened.
    if( ws.readyState == 1){
        try{
            ws.close();
        }catch(err){};
    }
    else if(ws.readyState == 0){
     // Don't do anything, just wait for the connection to be stablished
    }
    else{
        openSocket();
    }
};

function checkTimeout(){
    if(pendingSendMessages.length>0)
        renewConnection();
};

function websocketOnClose(evt){
    /* websocket is closed. */
    console.debug('Connection is closed... event code: ' + evt.code + ', reason: ' + evt.reason);
    // Some explanation on this error: http://stackoverflow.com/questions/19304157/getting-the-reason-why-websockets-closed
    // In practice, on a unstable network (wifi with a lot of traffic for example) this error appears
    // Got it with Chrome saying:
    // WebSocket connection to 'ws://x.x.x.x:y/' failed: Could not decode a text frame as UTF-8.
    // WebSocket connection to 'ws://x.x.x.x:y/' failed: Invalid frame header

    try {
        document.getElementById("loading").style.display = '';
    } catch(err) {
        console.log('Error hiding loading overlay ' + err.message);
    }

    failedConnections += 1;

    console.debug('failed connections=' + failedConnections + ' queued messages=' + pendingSendMessages.length);

    if(failedConnections > 3) {

        // check if the server has been restarted - which would give it a new websocket address,
        // new state, and require a reload
        console.debug('Checking if GUI still up ' + location.href);

        var http = new XMLHttpRequest();
        http.open('HEAD', location.href);
        http.onreadystatechange = function() {
            if (http.status == 200) {
                // server is up but has a new websocket address, reload
                location.reload();
            }
        };
        http.send();

        failedConnections = 0;
    }

    if(evt.code == 1006){
        renewConnection();
    }

};

function websocketOnError(evt){
    /* websocket is closed. */
    /* alert('Websocket error...');*/
    console.debug('Websocket error... event code: ' + evt.code + ', reason: ' + evt.reason);
};

function websocketOnOpen(evt){
    if(ws.readyState == 1){
        ws.send('connected');

        try {
            document.getElementById("loading").style.display = 'none';
        } catch(err) {
            console.log('Error hiding loading overlay ' + err.message);
        }

        failedConnections = 0;

        while(pendingSendMessages.length>0){
            ws.send(pendingSendMessages.shift()); /*whithout checking ack*/
        }
    }
    else{
        console.debug('onopen fired but the socket readyState was not 1');
    }
};

function uploadFile(widgetID, eventSuccess, eventFail, eventData, file){
    var url = '/';
    var xhr = new XMLHttpRequest();
    var fd = new FormData();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('filename', file.name);
    xhr.setRequestHeader('listener', widgetID);
    xhr.setRequestHeader('listener_function', eventData);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            /* Every thing ok, file uploaded */
            var params={};params['filename']=file.name;
            sendCallbackParam(widgetID, eventSuccess,params);
            console.log('upload success: ' + file.name);
        }else if(xhr.status == 400){
            var params={};params['filename']=file.name;
            sendCallbackParam(widgetID,eventFail,params);
            console.log('upload failed: ' + file.name);
        }
    };
    fd.append('upload_file', file);
    xhr.send(fd);
};
</script>""" % (net_interface_ip, wsport, pending_messages_queue_length, websocket_timeout_timer_ms)

        # add built in js, extend with user js
        clients[k].js_body_end += ('\n' + '\n'.join(self._get_list_from_app_args('js_body_end')))
        # use the default css, but append a version based on its hash, to stop browser caching
        with open(self._get_static_file('style.css'), 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
            clients[k].css_head = "<link href='/res/style.css?%s' rel='stylesheet' />\n" % md5
        # add built in css, extend with user css
        clients[k].css_head += ('\n' + '\n'.join(self._get_list_from_app_args('css_head')))

        # add user supplied extra html,css,js
        clients[k].html_head = '\n'.join(self._get_list_from_app_args('html_head'))
        clients[k].html_body_start = '\n'.join(self._get_list_from_app_args('html_body_start'))
        clients[k].html_body_end = '\n'.join(self._get_list_from_app_args('html_body_end'))
        clients[k].js_body_start = '\n'.join(self._get_list_from_app_args('js_body_start'))
        clients[k].js_head = '\n'.join(self._get_list_from_app_args('js_head'))

        if not hasattr(clients[k], 'websockets'):
            clients[k].websockets = []

        self.client = clients[k]

        if update_thread is None:
            # we need to, at least, ping the websockets to keep them alive. we might also ping more frequently if the
            # user requested we do so
            ping_time = self.server.websocket_timeout_timer_ms / 2000.0  # twice the timeout in ms
            if self.server.update_interval is None:
                interval = ping_time
            else:
                interval = min(ping_time, self.server.update_interval)
            update_thread = _UpdateThread(interval)
            update_event.set()  # update now

    def idle(self):
        """ Idle function called every UPDATE_INTERVAL before the gui update.
            Useful to schedule tasks. """
        pass

    def set_root_widget(self, widget):
        global update_lock, update_event
        #update_event.wait()
        self.root = widget
        # here we check if the root window has changed
        for ws in self.websockets:
            try:
                html = self.root.repr(self)
                ws.send_message('0' + self.root.identifier + ',' + to_websocket(html)) ##0==show_window message
            except:
                self.websockets.remove(ws)
        #update_event.clear()

    def _send_spontaneous_websocket_message(self, message):
        global update_lock
        with update_lock:
            for ws in self.client.websockets:
                # noinspection PyBroadException
                try:
                    self._log.debug("sending websocket spontaneous message")
                    ws.send_message(message)
                except:
                    self._log.error("sending websocket spontaneous message", exc_info=True)
                    self.client.websockets.remove(ws)
        update_event.clear()

    def execute_javascript(self, code):
        self._send_spontaneous_websocket_message(_MSG_JS + code)

    def notification_message(self, title, content, icon=""):
        """This function sends "javascript" message to the client, that executes its content.
           In this particular code, a notification message is shown
        """
        code = """
            var options = {
                body: "%(content)s",
                icon: "%(icon)s"
            }
            if (!("Notification" in window)) {
                alert("%(content)s");
            }else if (Notification.permission === "granted") {
                var notification = new Notification("%(title)s", options);
            }else if (Notification.permission !== 'denied') {
                Notification.requestPermission(function (permission) {
                    if (permission === "granted") {
                        var notification = new Notification("%(title)s", options);
                    }
                });
            }
        """ % {'title': title, 'content': content, 'icon': icon}
        self.execute_javascript(code)

    def do_POST(self):
        self._instance()
        file_data = None
        listener_widget = None
        listener_function = None
        try:
            # Parse the form data posted
            filename = self.headers['filename']
            listener_widget = runtimeInstances[self.headers['listener']]
            listener_function = self.headers['listener_function']
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_TYPE': self.headers['Content-Type']})
            # Echo back information about what was posted in the form
            for field in form.keys():
                field_item = form[field]
                if field_item.filename:
                    # The field contains an uploaded file
                    file_data = field_item.file.read()
                    file_len = len(file_data)
                    self._log.debug('post: uploaded %s as "%s" (%d bytes)\n' % (field, field_item.filename, file_len))
                    get_method_by_name(listener_widget, listener_function)(file_data, filename)
                else:
                    # Regular form value
                    self._log.debug('post: %s=%s\n' % (field, form[field].value))

            if file_data is not None:
                # the filedata is sent to the listener
                self._log.debug('GUI - server.py do_POST: fileupload name= %s' % (filename))
                self.send_response(200)
        except Exception as e:
            self._log.error('post: failed', exc_info=True)
            self.send_response(400)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Protected\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """Handler for the GET requests."""
        do_process = False
        if self.server.auth is None:
            do_process = True
        else:
            if not ('Authorization' in self.headers) or self.headers['Authorization'] is None:
                self._log.info("Authenticating")
                self.do_AUTHHEAD()
                self.wfile.write(encode_text('no auth header received'))
            elif self.headers['Authorization'] == 'Basic ' + self.server.auth.decode():
                do_process = True
            else:
                self.do_AUTHHEAD()
                self.wfile.write(encode_text(self.headers['Authorization']))
                self.wfile.write(encode_text('not authenticated'))

        if do_process:
            path = str(unquote(self.path))
            # noinspection PyBroadException
            try:
                self._instance()
                # build the page (call main()) in user code, if not built yet
                with update_lock:
                    # build the root page once if necessary
                    if not hasattr(self.client, 'root'):
                        self._log.info('built UI (path=%s)' % path)
                        self.client.root = self.main(*self.server.userdata)
                self._process_all(path)
            except:
                self._log.error('error processing GET request', exc_info=True)

    def _get_static_file(self, filename):
        static_paths = [os.path.join(os.path.dirname(__file__), 'res')]
        static_paths.extend(self._get_list_from_app_args('static_file_path'))
        for s in reversed(static_paths):
            path = os.path.join(s, filename)
            if os.path.exists(path):
                return path

    def _process_all(self, function):
        global update_lock

        self._log.debug('get: %s' % function)

        static_file = self.re_static_file.match(function)
        attr_call = self.re_attr_call.match(function)

        if (function == '/') or (not function):
            with update_lock:
                # render the HTML
                html = self.client.root.repr(self.client)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(encode_text("<!DOCTYPE html>\n"))
            self.wfile.write(encode_text("<html>\n<head>\n"))
            self.wfile.write(encode_text(
                """<meta content='text/html;charset=utf-8' http-equiv='Content-Type'>
                <meta content='utf-8' http-equiv='encoding'>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">"""))
            self.wfile.write(encode_text(self.client.css_head))
            self.wfile.write(encode_text(self.client.html_head))
            self.wfile.write(encode_text(self.client.js_head))
            self.wfile.write(encode_text("\n<title>%s</title>\n" % self.server.title))
            self.wfile.write(encode_text("\n</head>\n<body>\n"))
            self.wfile.write(encode_text(self.client.js_body_start))
            self.wfile.write(encode_text(self.client.html_body_start))
            self.wfile.write(encode_text('<div id="loading"><div id="loading-animation"></div></div>'))
            self.wfile.write(encode_text(html))
            self.wfile.write(encode_text(self.client.html_body_end))
            self.wfile.write(encode_text(self.client.js_body_end))
            self.wfile.write(encode_text("</body>\n</html>"))
        elif static_file:
            filename = self._get_static_file(static_file.groups()[0])
            if not filename:
                self.send_response(404)
                return
            mimetype, encoding = mimetypes.guess_type(filename)
            self.send_response(200)
            self.send_header('Content-type', mimetype if mimetype else 'application/octet-stream')
            if self.server.enable_file_cache:
                self.send_header('Cache-Control', 'public, max-age=86400')
            self.end_headers()
            with open(filename, 'rb') as f:
                content = f.read()
                self.wfile.write(content)
        elif attr_call:
            with update_lock:
                param_dict = parse_qs(urlparse(function).query)
                # parse_qs returns patameters as list, here we take the first element
                for k in param_dict:
                    param_dict[k] = param_dict[k][0]

                widget, function = attr_call.group(1, 2)
                try:
                    content, headers = get_method_by_name(get_method_by_id(widget), function)(**param_dict)
                    if content is None:
                        self.send_response(503)
                        return
                    self.send_response(200)
                except IOError:
                    self._log.error('attr %s/%s call error' % (widget, function), exc_info=True)
                    self.send_response(404)
                    return
                except (TypeError, AttributeError):
                    self._log.error('attr %s/%s not available' % (widget, function))
                    self.send_response(503)
                    return

            for k in headers:
                self.send_header(k, headers[k])
            self.end_headers()
            try:
                self.wfile.write(content)
            except:
                self.wfile.write(encode_text(content))


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):

    daemon_threads = True

    # noinspection PyPep8Naming
    def __init__(self, server_address, RequestHandlerClass, websocket_address,
                 auth, multiple_instance, enable_file_cache, update_interval,
                 websocket_timeout_timer_ms, host_name, pending_messages_queue_length,
                 title, *userdata):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.websocket_address = websocket_address
        self.auth = auth
        self.multiple_instance = multiple_instance
        self.enable_file_cache = enable_file_cache
        self.update_interval = update_interval
        self.websocket_timeout_timer_ms = websocket_timeout_timer_ms
        self.host_name = host_name
        self.pending_messages_queue_length = pending_messages_queue_length
        self.title = title
        self.userdata = userdata


class Server(object):
    # noinspection PyShadowingNames
    def __init__(self, gui_class, title='', start=True, address='127.0.0.1', port=8081, username=None, password=None,
                 multiple_instance=False, enable_file_cache=True, update_interval=0.1, start_browser=True,
                 websocket_timeout_timer_ms=1000, websocket_port=0, host_name=None,
                 pending_messages_queue_length=1000, userdata=()):
        self._gui = gui_class
        self._title = title or gui_class.__name__
        self._wsserver = self._sserver = None
        self._wsth = self._sth = None
        self._base_address = ''
        self._address = address
        self._sport = port
        self._multiple_instance = multiple_instance
        self._enable_file_cache = enable_file_cache
        self._update_interval = update_interval
        self._start_browser = start_browser
        self._websocket_timeout_timer_ms = websocket_timeout_timer_ms
        self._websocket_port = websocket_port
        self._host_name = host_name
        self._pending_messages_queue_length = pending_messages_queue_length
        self._userdata = userdata
        if username and password:
            self._auth = base64.b64encode(encode_text("%s:%s" % (username, password)))
        else:
            self._auth = None

        if not isinstance(userdata, tuple):
            raise ValueError('userdata must be a tuple')

        self._log = logging.getLogger('remi.server')

        if start:
            self.start()
            self.serve_forever()

    @property
    def title(self):
        return self._title

    @property
    def address(self):
        return self._base_address

    def start(self):
        # here the websocket is started on an ephemereal port
        self._wsserver = ThreadedWebsocketServer((self._address, self._websocket_port), WebSocketsHandler,
                                                 self._multiple_instance)
        wshost, wsport = self._wsserver.socket.getsockname()[:2]
        self._log.info('Started websocket server %s:%s' % (wshost, wsport))
        self._wsth = threading.Thread(target=self._wsserver.serve_forever)
        self._wsth.daemon = True
        self._wsth.start()

        # Create a web server and define the handler to manage the incoming
        # request
        self._sserver = ThreadedHTTPServer((self._address, self._sport), self._gui,
                                           (wshost, wsport), self._auth,
                                           self._multiple_instance, self._enable_file_cache,
                                           self._update_interval, self._websocket_timeout_timer_ms,
                                           self._host_name, self._pending_messages_queue_length,
                                           self._title, *self._userdata)
        shost, sport = self._sserver.socket.getsockname()[:2]
        # when listening on multiple net interfaces the browsers connects to localhost
        if shost == '0.0.0.0':
            shost = '127.0.0.1'
        self._base_address = 'http://%s:%s/' % (shost,sport)
        self._log.info('Started httpserver %s' % self._base_address)
        if self._start_browser:
            try:
                import android
                android.webbrowser.open(self._base_address)
            except ImportError:
                # use default browser instead of always forcing IE on Windows
                if os.name == 'nt':
                    webbrowser.get('windows-default').open(self._base_address)
                else:
                    webbrowser.open(self._base_address)
        self._sth = threading.Thread(target=self._sserver.serve_forever)
        self._sth.daemon = True
        self._sth.start()

    def serve_forever(self):
        # we could join on the threads, but join blocks all interupts (including
        # ctrl+c, so just spin here
        # noinspection PyBroadException
        try:
            while True:
                signal.pause()
        except Exception:
            # signal.pause() is missing for Windows; wait 1ms and loop instead
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def stop(self):
        self._wsserver.shutdown()
        self._wsth.join()
        self._sserver.shutdown()
        self._sth.join()


class StandaloneServer(Server):
    def __init__(self, gui_class, title='', width=800, height=600, resizable=True, fullscreen=False, start=True,
                 userdata=()):
        Server.__init__(self, gui_class, title=title, start=False, address='127.0.0.1', port=0, username=None,
                        password=None,
                        multiple_instance=False, enable_file_cache=True, update_interval=0.1, start_browser=False,
                        websocket_timeout_timer_ms=1000, websocket_port=0, host_name=None,
                        pending_messages_queue_length=1000, userdata=userdata)

        self._application_conf = {'width':width, 'height':height, 'resizable':resizable, 'fullscreen':fullscreen}

        if start:
            self.serve_forever()

    def serve_forever(self):
        try:
            import webview
            Server.start(self)
            webview.create_window(self.title, self.address, **self._application_conf)
            Server.stop(self)
        except ImportError:
            raise ImportError('PyWebView is missing. Please install it by:\n    '
                              'pip install pywebview\n    '
                              'more info at https://github.com/r0x0r/pywebview')


def start(mainGuiClass, **kwargs):
    """This method starts the webserver with a specific App subclass."""
    debug = kwargs.pop('debug', False)
    standalone = kwargs.pop('standalone', False)

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                        format='%(name)-16s %(levelname)-8s %(message)s')
    logging.getLogger('remi').setLevel(
            level=logging.DEBUG if debug else logging.INFO)

    if standalone:
        s = StandaloneServer(mainGuiClass, start=True, **kwargs)
    else:
        s = Server(mainGuiClass, start=True, **kwargs)

