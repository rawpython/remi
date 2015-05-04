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

import urllib2
from configuration import runtimeInstances, MULTIPLE_INSTANCE, ENABLE_FILE_CACHE, BASE_ADDRESS, HTTP_PORT_NUMBER, WEBSOCKET_PORT_NUMBER, IP_ADDR, UPDATE_INTERVAL
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SocketServer
import webbrowser
import struct
from base64 import b64encode
from hashlib import sha1
from mimetools import Message
from StringIO import StringIO
import threading
from threading import Timer
import copy


clients = {}
updateTimerStarted = False  # to start the update timer only once


def getMethodBy(rootNode, idname):
    if idname.isdigit():
        return getMethodById(rootNode, idname)
    return getMethodByName(rootNode, idname)


def getMethodByName(rootNode, name, maxIter=5):
    val = None
    if hasattr(rootNode, name):
        val = getattr(rootNode, name)
    else:
        pass
        #print("the method '" + name + "' is not part of this instance type:" + str(rootNode))
    return val


def getMethodById(rootNode, _id, maxIter=5):
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
                val = getMethodById(i, _id, maxIter)
                if val is not None:
                    return val
    except:
        pass
    return None


class ThreadedWebsocketServer(
        SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


class WebSocketsHandler(SocketServer.StreamRequestHandler):
    magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def setup(self):
        global clients
        SocketServer.StreamRequestHandler.setup(self)
        print 'websocket connection established', self.client_address
        self.handshake_done = False

    def handle(self):
        print('handle\n')
        while True:
            if not self.handshake_done:
                self.handshake()
            else:
                if not self.read_next_message():
                    break

    def read_next_message(self):
        try:
            print('read_next_message\n')
            length = ord(self.rfile.read(2)[1]) & 127
            if length == 126:
                length = struct.unpack('>H', self.rfile.read(2))[0]
            elif length == 127:
                length = struct.unpack('>Q', self.rfile.read(8))[0]
            masks = [ord(byte) for byte in self.rfile.read(4)]
            decoded = ''
            for char in self.rfile.read(length):
                decoded += chr(ord(char) ^ masks[len(decoded) % 4])
            self.on_message(decoded)
            return True
        except:
            return False

    def send_message(self, message):
        print('send_message\n')
        self.request.send(chr(129))
        length = len(message)
        if length <= 125:
            self.request.send(chr(length))
        elif length >= 126 and length <= 65535:
            self.request.send(chr(126))
            self.request.send(struct.pack('>H', length))
        else:
            self.request.send(chr(127))
            self.request.send(struct.pack('>Q', length))
        self.request.send(message)

    def handshake(self):
        print('handshake\n')
        data = self.request.recv(1024).strip()
        headers = Message(StringIO(data.split('\r\n', 1)[1]))
        # if headers.get("Upgrade", None) != "websocket":
        #    return
        print 'Handshaking...'
        key = headers['Sec-WebSocket-Key']
        digest = b64encode(sha1(key + self.magic).hexdigest().decode('hex'))
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
        self.handshake_done = self.request.send(response)

    def on_message(self, message):
        # saving the websocket in order to update the client
        k = self.client_address[0]
        if not MULTIPLE_INSTANCE:
            # overwrite the key value, so all clients will point the same
            # instance
            k = 0
        if not self in clients[k].websockets:
            clients[k].websockets.append(self)
        print('on_message\n')
        print 'recv from websocket client: ' + message

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

                paramDict = parseParametrs(params)
                print('msgType: ' + msgType + ' widgetId: ' + widgetID +
                      ' function: ' + functionName + ' params: ' + str(params))

                for w in runtimeInstances:
                    if str(id(w)) == widgetID:
                        callback = getMethodByName(w, functionName)
                        if callback is not None:
                            callback(**paramDict)


def parseParametrs(p):
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
                if fieldValue.count('.') == 1:
                    fieldValue = float(fieldValue)
                if fieldValue.isdigit():
                    fieldValue = int(fieldValue)
            ret[fieldName] = fieldValue
    return ret


def update_clients():
    global clients
    for client in clients.values():
        gui_updater(client, client.root)
    Timer(UPDATE_INTERVAL, update_clients, ()).start()


def gui_updater(client, leaf):
    # if there is not a copy of widgets, do it
    if not hasattr(client, 'old_runtime_widgets'):
        client.old_runtime_widgets = dict()  # idWidget,reprWidget

    __id = str(id(leaf))
    # if the widget is not contained in the copy
    if not (__id in client.old_runtime_widgets.keys()):
        # considering that this leaf is not in the old runtimes and it is a
        # root window, a new window is shown, clean the old_runtime_widgets
        if client.root == leaf:
            client.old_runtime_widgets = dict()
            client.old_runtime_widgets[__id] = repr(leaf)  # copy.copy(leaf)
            for ws in client.websockets:
                ws.send_message('show_window,' + __id + ',' + repr(leaf))
            return True
        client.old_runtime_widgets[__id] = repr(leaf)  # copy.copy(leaf)
    # if the widget has changed or its subwidgets
    if repr(leaf) != client.old_runtime_widgets[__id]:
        client.old_runtime_widgets[__id] = repr(leaf)
        subleafs_changed = False
        try:
            for subleaf in leaf.children.values():
                subleafs_changed = subleafs_changed or gui_updater(client, subleaf)
        except:
            pass
        # if no subleafs changed it means that we have to send the updated
        # widget
        if not subleafs_changed:
            #client.old_runtime_widgets[__id] = repr(leaf)
            for ws in client.websockets:
                try:
                    print("update_widget: " + __id + "  type: " + str(type(leaf)))
                    ws.send_message('update_widget,' + __id + ',' + repr(leaf))
                except:
                    pass
        return True
    # widget NOT changed
    return False


class BaseApp(BaseHTTPRequestHandler, WebSocketsHandler, object):

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
        document.body.innerHTML = content;\
    }else if( command=='update_widget'){\
        var elem = document.getElementById(s[1]);\
        var index = received_msg.indexOf(',')+1;\
        elem.insertAdjacentHTML('afterend',content);\
        elem.parentElement.removeChild(elem);\
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
    ws.send('callback' + '/' + widgetID+'/'+functionName + '/' + paramPacketize(params));\
};\
/*this uses websockets*/\
var sendCallback = function (widgetID,functionName){\
    if (ws.readyState != WebSocket.OPEN){\
        console.debug('socket not opened');\
        openSocket();\
    }\
    ws.send('callback' + '/' + widgetID+'/'+functionName+'/');\
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
        # here the websocket is started
        server = ThreadedWebsocketServer(
            (IP_ADDR, WEBSOCKET_PORT_NUMBER), WebSocketsHandler)
        threading.Thread(target=server.serve_forever).start()
        if updateTimerStarted == False:
            updateTimerStarted = True
            Timer(UPDATE_INTERVAL, update_clients, ()).start()

    def do_POST(self):
        self.instance()
        varLen = int(self.headers['Content-Length'])
        postVars = self.rfile.read(varLen)
        postVars = str(urllib2.unquote(postVars).decode('utf8'))
        paramDict = parseParametrs(postVars)
        function = str(urllib2.unquote(self.path).decode('utf8'))
        self.processAll(function, paramDict, True)

    def do_GET(self):
        """Handler for the GET requests."""
        self.instance()
        params = str(urllib2.unquote(self.path).decode('utf8'))

        params = params.split('?')
        function = params[0]

        function = function[1:]
        self.processAll(function, dict(), False)

        return

    def processAll(self, function, paramDict, isPost):
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
                    snake = getMethodBy(self.client.root, attr)
                    ispath = ispath and (None != snake)
                    continue
                snake = getMethodBy(snake, attr)
                ispath = ispath and (None != snake)
        else:
            function = function.replace('/', '')
            if len(function) > 0:
                snake = getMethodBy(self.client, function)
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

                self.wfile.write(self.client.attachments)
                self.wfile.write(
                    "<link href='" +
                    BASE_ADDRESS +
                    "style.css' rel='stylesheet' />")

                self.wfile.write(repr(self.client.root))
            else:
                # here is the function that should return the content type
                self.send_response(200)
                self.send_header('Content-type', ret[1])

                self.end_headers()

                # if is requested a widget, but not by post, so we suppose is
                # requested to show a new page, we attach javascript and style
                if(ret[1] == 'text/html' and isPost == False):
                    self.wfile.write(self.client.attachments)
                    self.wfile.write(
                        "<link href='" +
                        BASE_ADDRESS +
                        "style.css' rel='stylesheet' />")

                self.wfile.write(ret[0])

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            if ENABLE_FILE_CACHE:
                self.send_header('Cache-Control', 'public, max-age=86400')
            self.end_headers()

            f = open('./' + function, 'r+b')
            content = ''.join(f.readlines())
            f.close()
            self.wfile.write(content)


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):

    """This class allows to handle requests in separated threads.

    No further content needed, don't touch this.

    """


def start(mainGuiClass):
    """This method starts the webserver with a specific BaseApp subclass."""
    try:
        # Create a web server and define the handler to manage the incoming
        # request
        server = ThreadedHTTPServer(('', HTTP_PORT_NUMBER), mainGuiClass)
        print('Started httpserver on port ', HTTP_PORT_NUMBER)
        try:
            import android
            android.webbrowser.open(BASE_ADDRESS)
        except:
            webbrowser.open(BASE_ADDRESS)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
