from configuration import *
import server
from server import *

#simple and stupid tricks
def toPix(x):
	return str(x)+"px"
def fromPix(x):
	return int(x.replace("px",""))
def jsonize(d):
	return ";".join(map(lambda k,v:k+":"+v+"",d.keys(),d.values()))

#Manages the event propagation to the listeners functions
class eventManager():
	def __init__(self):
		self.listeners={}
	#if for an event there is a listener, it calls the listener passing the parameters
	def propagate(self,eventname,params):
		if not eventname in self.listeners.keys():
			return
		listener = self.listeners[eventname]
		return getattr(listener['instance'],listener['funcname'])(*params)
	#register a listener for a specific event
	def registerListener(self,eventname,instance,funcname):
		listener = {}
		listener['instance'] = instance
		listener['funcname'] = funcname
		self.listeners[eventname] = listener

#base class for gui widgets. In html, it is a DIV tag
#	the "self.type" 		attribute specifies the HTML tag representation
#	the "self.attributes[]"	attribute specifies the HTML attributes like "style" "class" "id"
#	the "self.style[]"		attribute specifies the CSS style content like "font" "color". It will be packet togheter with "self.attributes"
class widget(object):
	#w = numeric with 
	#h = numeric height
	#layout_orizontal = specifies the "float" css attribute
	#widget_spacing = specifies the "margin" css attribute for the children
	def __init__(self,w=1,h=1,layout_orizontal=True,widget_spacing=0):
		#the runtime instances are processed every time a requests arrives, searching for the called method
		#	if a class instance is not present in the runtimeInstances, it will we not callable
		runtimeInstances.append(self)
	
		self.renderChildrenList = list()
		self.children={}
		self.attributes={} #properties as class id style
		self.style = {}

		self.type = "div"
		
		self.layout_orizontal = layout_orizontal
		self.widget_spacing = widget_spacing
		
		#some constants for the events
		self.BASE_ADDRESS = BASE_ADDRESS
		self.EVENT_ONCLICK = "onclick"
		self.EVENT_ONDBLCLICK = "ondblclick"
		self.EVENT_ONMOUSEDOWN = "onmousedown"
		self.EVENT_ONMOUSEMOVE = "onmousemove"
		self.EVENT_ONMOUSEOVER = "onmouseover"
		self.EVENT_ONMOUSEOUT = "onmouseout"
		self.EVENT_ONMOUSEUP = "onmouseup"
		self.EVENT_ONKEYDOWN = "onkeydown"
		self.EVENT_ONKEYPRESS = "onkeypress"
		self.EVENT_ONKEYUP = "onkeyup"
		self.EVENT_ONCHANGE = "onchange"
		self.EVENT_ONFOCUS = "onfocus"
		self.EVENT_ONBLUR = "onblur"
		
		self.attributes['class']='widget'
		self.attributes['id']=str(id(self))

		self.style['width'] = toPix(w)
		self.style['height'] = toPix(h)
		self.style['margin'] = "0px auto"
		self.style['display'] = "block"

		self.eventManager = eventManager()

	#it is used to automatically represent the widget to HTML format
	#	packs all the attributes, children and so on
	def __repr__(self):
		self['style'] = jsonize(self.style)
		classname = self.__class__.__name__
		
		#concatenating innerHTML. in case of html object we use repr, in case of string we use directly the content
		innerHTML = ""
		for s in self.renderChildrenList:
			if type(s) == type(""):
				innerHTML = innerHTML + s
			else:
				innerHTML = innerHTML + repr(s)
		
		return "<%s %s>%s</%s>" % (self.type," ".join(map(lambda k,v:k+"=\""+v+"\"",self.attributes.keys(),self.attributes.values())),innerHTML,self.type)
		
	#it is used for fast access to "self.attributes[]"
	def __setitem__(self,key,value):
		self.attributes[key]=value
	
	#it allows to add child widgets to this. The key can be everything you want, in order to access to the specific child in this way "widget.children[key]".
	def append(self,key,value):
		if key in self.children.keys():
			self.renderChildrenList.remove(self.children[key])
		self.renderChildrenList.append(value)

		self.children[key]=value
		
		if hasattr(self.children[key],'style'):
			self.children[key].style['margin'] = toPix(self.widget_spacing)
			if self.layout_orizontal:
				self.children[key].style['float'] = 'left'
	

#button widget:
#	implements the onclick event. reloads the web page because it uses the GET call.
#requires
class buttonWidget(widget):
	def __init__(self,w,h,text=""):
		super(buttonWidget,self).__init__(w,h)
		self.type = "button"
		self.attributes['class']='buttonWidget'
		self.attributes[ self.EVENT_ONCLICK ]="event.cancelBubble=true;var t='?x='+event.x+'?y='+event.y ;window.location='" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCLICK + "'+t;return false;"
		self.text(text)
	def text(self,t):
		self.append( "text", t )
	#returns mouse "x" and "y" position
	def onclick(self,x,y):
		print( "buttonWidget pressed: ", self.children["text"] )
		return self.eventManager.propagate( self.EVENT_ONCLICK, (x,y) )
	#register a listener for the click event.
	#	listener = class instance
	#	funcname = the name of member function that will be called.
	#example:
	#	bt.setOnClickListener( listenerClass, "ontest" )
	def setOnClickListener(self,listener,funcname):
		self.eventManager.registerListener( self.EVENT_ONCLICK, listener, funcname )

#multiline text area widget
#	implements the onclick event. reloads the web page because it uses the GET call.
#	implements the onchange event with POST method, without reloading the web page
class textareaWidget(widget):
	def __init__(self,w,h):
		super(textareaWidget,self).__init__(w,h)
		self.type = "textarea"
		self.attributes['class']='textareaWidget'
		
		_identifier=self.attributes['id']

		self.attributes[ self.EVENT_ONCLICK ] = ""
		self.attributes[ self.EVENT_ONCHANGE ] = " var v=\'newValue=\'+document.getElementById('"+_identifier+"').value ;sendCommand('" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCHANGE + "',v);"
		self.text("")
	#sets the text content
	def text(self,t):
		self.append("text",t)
	def value(self):
		return self.children['text']
	#returns the new text value
	def onchange(self,newValue):
		self.text(newValue)
		params = list()
		params.append(newValue)
		return self.eventManager.propagate("onchange",params)
	#register the listener for the onchange event
	def setOnChangeListener(self,listener,funcname):
		self.eventManager.registerListener( "onchange",listener,funcname)
	def onclick(self,x,y):
		return self.eventManager.propagate("onclick",(x,y))
	def setOnClickListener(self,listener,funcname):
		self.attributes[ self.EVENT_ONCLICK ] = "event.cancelBubble=true;var t='?x='+event.x+'?y='+event.y ;window.location='" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCLICK + "'+t;return false;"
		self.eventManager.registerListener( "onclick",listener,funcname)

#spin box widget usefull as numeric input field
#	implements the onclick event. reloads the web page because it uses the GET call.
#	implements the onchange event with POST method, without reloading the web page
class spinboxWidget(widget):
	def __init__(self,w,h,min=100,max=5000,value=1000,step=1):
		super(spinboxWidget,self).__init__(w,h)
		self.type = "input"
		self.attributes['class']='spinboxWidget'
		self.attributes['type']='number'
		self.attributes['min']=str(min)
		self.attributes['max']=str(max)
		self.attributes['value']=str(value)
		self.attributes['step']=str(step)

		self.attributes[ self.EVENT_ONCLICK ] = ""
		self.attributes[ self.EVENT_ONCHANGE ] = " var v=\'newValue=\'+document.getElementById('"+str(id(self))+"').value ;sendCommand('" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCHANGE + "',v);"
	def onchange(self,newValue):
		params = list()
		params.append(newValue)
		return self.eventManager.propagate("onchange",params)
	def setOnChangeListener(self,listener,funcname):
		self.eventManager.registerListener( "onchange",listener,funcname)
	def onclick(self,x,y):
		return self.eventManager.propagate("onclick",(x,y))
	def setOnClickListener(self,listener,funcname):
		self.attributes[ self.EVENT_ONCLICK ] = "event.cancelBubble=true;var t='?x='+event.x+'?y='+event.y ;window.location='" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCLICK + "'+t;return false;"
		self.eventManager.registerListener( "onclick",listener,funcname)
	def value(self):
		return self.children['text']

class labelWidget(widget):
	def __init__(self,w,h,text):
		super(labelWidget,self).__init__(w,h)
		self.type = "p"
		self.attributes['class']='labelWidget'
		self.append( "content", text )
	def setText(self,t):
		self.append( "content", t )
	def getText(self):
		return self.children["content"]
	
#input dialog, it opens a new webpage
#	allows the OK/ABORT functionality implementing the "onConfirm" and "onAbort" events
class inputDialog(widget):
	def __init__(self,title,message):
		w = 500
		h = 200
		super(inputDialog,self).__init__(w,h,False)
		
		self.EVENT_ONCONFIRM = "confirmValue"
		self.EVENT_ONABORT = "abortValue"
		self.style["font-family"] = "arial,sans-serif"
		t = labelWidget(w-50, 50, title)
		m = labelWidget(w-50, 30, message)
		self.inputText = textareaWidget(w-100, 30)
		self.conf = buttonWidget(50,30,"Ok")
		self.abort = buttonWidget(50,30,"Abort")
		
		t.style["font-size"] = "16px"
		t.style["font-weight"] = "bold"
		
		hlay = widget( w,30 )
		hlay.append("1",self.inputText)
		hlay.append("2",self.conf)
		hlay.append("3",self.abort)
		
		self.append("1",t)
		self.append("2",m)
		self.append("3",hlay)
		
		self.inputText.attributes[ self.EVENT_ONCHANGE ] = ""
		self.conf.attributes[ self.EVENT_ONCLICK ] = "var v=\'?value=\'+document.getElementById('"+str(id(self.inputText))+"').value ;window.location='" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCONFIRM + "' + v;"
		self.abort.attributes[ self.EVENT_ONCLICK ] = "window.location='" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONABORT + "';"
		self.inputText.attributes[ self.EVENT_ONCLICK ] = ""
	#event called pressing on OK button. propagates the string content of the input field
	def confirmValue(self,value):
		params = list()
		params.append(value)
		return self.eventManager.propagate(self.EVENT_ONCONFIRM,params)	
	def setOnConfirmValueListener(self,listener,funcname):
		self.eventManager.registerListener( self.EVENT_ONCONFIRM,listener,funcname)
	def abortValue(self):
		params = list()
		return self.eventManager.propagate(self.EVENT_ONABORT,params)	
	def setOnAbortValueListener(self,listener,funcname):
		self.eventManager.registerListener( self.EVENT_ONABORT,listener,funcname)

#list widget
#	it can contain listItems
class listWidget(widget):
	def __init__(self,w,h):
		super(listWidget,self).__init__(w,h)
		self.type = "ul"
		self.attributes['class'] = "listWidget"

#item widget for the listWidget
#	implements the onclick event. reloads the web page because it uses the GET call.
class listItem(widget):
	def __init__(self,w,h,text):
		super(listItem,self).__init__(w,h)
		self.type = "li"
		self.attributes['class'] = "listItem"
		
		self.attributes[ self.EVENT_ONCLICK ]=""
		self.append("1",text)
	def onclick(self,x,y):
		return self.eventManager.propagate("onclick",(x,y))
	def setOnClickListener(self,listener,funcname):
		self.attributes[ self.EVENT_ONCLICK ]="event.cancelBubble=true;var t='?x='+event.x+'?y='+event.y ;window.location='" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCLICK + "'+t;return false;"	
		self.eventManager.registerListener( "onclick",listener,funcname)		

#combo box widget
#	implements the onchange event with POST method, without reloading the web page
class comboWidget(widget):
	def __init__(self,w,h):
		super(comboWidget,self).__init__(w,h)
		self.type = "select"
		self.attributes['class'] = "comboWidget"
		self.attributes[ self.EVENT_ONCHANGE ] = " var v=\'newValue=\'+document.getElementById('"+str(id(self))+"').value ;sendCommand('" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCHANGE + "',v);"
		
	def onchange(self,newValue):
		params = list()
		params.append(newValue)
		print("combo box. selected", newValue)
		return self.eventManager.propagate("onchange",params)
	def setOnChangeListener(self,listener,funcname):
		self.eventManager.registerListener( "onchange",listener,funcname)

#item widget for the comboWidget
#	implements the onclick event. reloads the web page because it uses the GET call.
class comboItem(widget):
	def __init__(self,w,h,text):
		super(comboItem,self).__init__(w,h)
		self.type = "option"
		self.attributes['class'] = "comboItem"
		self.attributes[ self.EVENT_ONCLICK ]=""
		self.append("1",text)
		self.attributes['value'] = text
	def onclick(self,x,y):
		return self.eventManager.propagate("onclick",(x,y))
	def setOnClickListener(self,listener,funcname):
		self.attributes[ self.EVENT_ONCLICK ]="event.cancelBubble=true;var t='?x='+event.x+'?y='+event.y ;window.location='" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONCLICK + "'+t;return false;"	
		self.eventManager.registerListener( "onclick",listener,funcname)		

#image widget
class imageWidget(widget):
	#filename should be an URL
	def __init__(self,w,h,filename):
		super(imageWidget,self).__init__(w,h)
		self.type = "image"
		self.attributes['class'] = "imageWidget"
		self.attributes['src'] = filename
