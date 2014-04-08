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

#!/usr/bin/python
import sys
import urllib2
from configuration import *
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import webbrowser

clients = {}

#tarocco to speedup server reply
def _bare_address_string(self):
    host, port = self.client_address[:2]
    return str(host)
BaseHTTPRequestHandler.address_string = \
        _bare_address_string


def getMethodBy(rootNode,idname):
	if idname.isdigit():
	  return getMethodById(rootNode,idname)
	return getMethodByName(rootNode,idname)

def getMethodByName(rootNode,name,maxIter=5):
	val = None
	if hasattr(rootNode,name):
	 val = getattr(rootNode,name)
	else:
		pass
	 	#print("the method '" + name + "' is not part of this instance type:" + str(rootNode)) 
	return val

def getMethodById(rootNode,_id,maxIter=5):
	for i in runtimeInstances:
		if id(i)==_id:
			return i

	maxIter = maxIter - 1
	if maxIter<0:
	 	return None
	_id = int(_id)
	
	if id(rootNode)==_id:
		return rootNode
	
	try:
	 	if hasattr(rootNode,'children'):	
	 	 	for i in rootNode.children.values():
	 	 	 	#print(str(i))
		 	 	val = getMethodById(i,_id, maxIter )
		 	 	if val!=None:
			 	 	return val
	except:
	 	pass
	return None


#This class will handles any incoming request from the browser 
#The main application class can subclass this
#	In the do_POST and do_GET methods it is expected to receive requests such as:
#		- function calls with parameters
#		- file requests
class BaseApp(BaseHTTPRequestHandler,object):

	#this method is used to get the Application instance previously created
	#	managing on this, it is possible to switch to "single instance for multiple clients" or "multiple instance for multiple clients" execution way
	def instance(self):
		k = self.client_address[0]
		if not MULTIPLE_INSTANCE:
			k = 0 #overwrite the key value, so all clients will point the same instance
		if not(k in clients.keys()):
			runtimeInstances.append(self)
			
			clients[k]=self
			clients[k].attachments = "<script>var sendCommand = function (url,params) { var request = new XMLHttpRequest(); request.open('POST', url, false); request.send(params); };</script>"
		self.client = clients[k]

	def do_POST(self):
		self.instance()
		varLen = int(self.headers['Content-Length'])
		postVars = self.rfile.read(varLen)
		postVars = str(urllib2.unquote(postVars).decode('utf8'))
		postVars = postVars.split("&")
		paramDict = {}
		for s in postVars:
			paramDict[s.split("=")[0]] = s.split("=")[1]
		
		function = str(urllib2.unquote(self.path).decode('utf8'))
		self.processAll(function, paramDict)
	
	#Handler for the GET requests
	def do_GET(self):
		self.instance()
		params = str(urllib2.unquote(self.path).decode('utf8'))

		params = params.split("?")
		paramDict = dict()
		function = ""

		for p in params:
			if p.count("=")==0:
				function = p
				continue
			paramDict[p.split("=")[0]]=p.split("=")[1]

			if paramDict[p.split("=")[0]].count("'")==0 and paramDict[p.split("=")[0]].count('"')==0 and paramDict[p.split("=")[0]].count('.')==1:
				paramDict[p.split("=")[0]] = float(paramDict[p.split("=")[0]])
			else:
				if paramDict[p.split("=")[0]].isdigit() and paramDict[p.split("=")[0]].count("'")==0 and paramDict[p.split("=")[0]].count('"')==0 and paramDict[p.split("=")[0]].count('.')==0:
					paramDict[p.split("=")[0]] = int(paramDict[p.split("=")[0]])

		function=function[1:]
		self.processAll(function, paramDict)

		return
	
	def processAll(self, function, paramDict):
		ispath = True
		snake = None
		doNotCallMain = False
		if len(function.split("/"))>1:
			for attr in function.split("/"):
				if len(attr)==0:
					continue
				if ispath==False:
					break
				if snake==None:
					snake = getMethodBy(self.client.root,attr)
					ispath = ispath and (None!=snake)	
					continue
				snake = getMethodBy(snake,attr)
				ispath = ispath and (None!=snake)
		else:
			function=function.replace('/','')
			if len(function)>0:
				snake = getMethodBy(self.client,function)
				ispath = ispath and (None!=snake)
			else:
				doNotCallMain = hasattr( self.client, "root" )
				ispath = True
				snake = self.main
			
		if ispath:
			ret = None
			if not doNotCallMain:
				ret = snake(**paramDict)
				
			if ret==None:
				self.send_response(200)
				self.send_header('Content-type','text/html')				
				self.end_headers()
				
				self.wfile.write(self.client.attachments);
				self.wfile.write("<link href='" + BASE_ADDRESS + "style.css' rel='stylesheet' />");
				
				self.wfile.write( repr(self.client.root) )
			else:
				#here is the function that should return the content type
				self.send_response(200)
				self.send_header('Content-type',ret[1])
				self.end_headers()
				self.wfile.write( ret[0] )
				
		else:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			
			f = open("./"+function,"r+b")
			content = "".join(f.readlines())
			f.close()
			self.wfile.write(content)
			
#this method starts the webserver with a specific BaseApp subclass
def start(mainGuiClass):
	try:
		#Create a web server and define the handler to manage the incoming request
		server = HTTPServer(('', PORT_NUMBER), mainGuiClass)
		print( 'Started httpserver on port ' , PORT_NUMBER )
		try:
			import android
			android.webbrowser.open( BASE_ADDRESS )
		except:
			webbrowser.open( BASE_ADDRESS )
		server.serve_forever()
		

	except KeyboardInterrupt:
		print( '^C received, shutting down the web server' )
		server.socket.close()

