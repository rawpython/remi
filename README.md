gui
===
python gui library based on HTML and so, platform indipendent

It allows to create platform indipendent GUI with python. The entire gui will be shown in the browser because it is represented in HTML. When your app starts, it starts a webserver that will be accessible on your network.

Why another gui lib?
Ok, Kivy is the best, Tk is historical, pyQt is also good, but for every platform that appears we have to wait a porting. This lib allows to show a user interface everywhere there is a browser.

Right now it is incomplete. These widgets are available:
- widget : like an empty panel
- buttonWidget
- textareaWidget : for the editable text
- spinboxWidget
- labelWidget
- inputDialog
- listWidget
- comboWidget
- imageWidget
- tableWidget
- objectWidget : allows to show embedded object like pdf,swf..
- canvasWidget : usefull to draw arbitrary geometries. It uses PIL's library.

A basic application appears like this:

<pre><code>
import gui
from gui import *

class App( BaseApp ):
	def __init__( self, *args ):
		super( App, self ).__init__( *args )
		
	def main( self ):
		#the arguments are	width - height - layoutOrientationOrizontal
		wid = gui.widget( 100, 60, False )
		self.lbl = gui.labelWidget( 100, 30, "Hello world!" )
		self.bt = gui.buttonWidget( 100, 30, "Press me!" )
			
		#setting the listener for the onclick event of the button
		self.bt.setOnClickListener( self, "onButtonPressed" )
			
		#appending a widget to another, the first argument is a string key
		wid.append( "1", self.lbl )
		wid.append( "2", self.bt )
			
		#return of the root widget
		return wid
	
	#listener function
	def onButtonPressed( self, x, y ):
		self.lbl.setText( "Button pressed!" )
		self.bt.text("Hi!")

#starts the webserver	
start( App )
</code></pre>

In order to see the user interface, open your preferred browser (I use Chrome) and type "http://127.0.0.1:8080".
You can change the url address, edit the "configuration.py" file.

Tested on Android, Linux, Windows with Google Chrome web browser.
