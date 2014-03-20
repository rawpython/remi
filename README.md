gui
===
This is an pre-pre-pre-alpha version!!

python gui library based on HTML and so, platform indipendent

It allows to create platform indipendent GUI with python. The entire gui will be shown in the browser because it is represented in HTML. When your app starts, it starts a webserver that will be accessible on your network.

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
			
		#setting up the root widget
		self.client.root = wid
	
	#listener function
	def onButtonPressed( self, x, y ):
		self.lbl.setText( "Button pressed!" )
		self.bt.text("testo")

#starts the webserver	
start( App )
</code></pre>


Tested on Android, Linux, Windows.
