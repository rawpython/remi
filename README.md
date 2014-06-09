gui
===
Platform indipendent python gui library.

It allows to create platform indipendent GUI with python. The entire gui will be shown in the browser because it is represented in HTML. You have to write NO HTML code, because the library itself converts the python code automatically in HTML. When your app starts, it starts a webserver that will be accessible on your network.

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

FAQ
===
-Should I know HTML?
NO, It is not required, you have to code only in python.
-Can I use this library with other browsers?
Yes you can, but I haven't tested it and probably something couldn't work fine.
-It is open source?
For sure!
-Where is the documentation?
I'm working on this, but it requires time. If you need support you can contact me directly on dddomodossola(at)gmail(dot)com


Brief tutorial
===
Import gui library and all submodules.

<pre><code>

import gui
from gui import *

</code></pre>


Subclass the <code>BaseApp</code> class and declare a <code>main</code> function that will be the entry point of the application. Inside the main function you have to <code>return</code> the root widget.

<pre><code>

class App( BaseApp ):
	def __init__( self, *args ):
		super( App, self ).__init__( *args )
		
	def main( self ):
		lbl = gui.labelWidget( 100, 30, "Hello world!" )
		
		#return of the root widget
		return lbl

</code></pre>


Outside the main class start the application calling the function <code>start</code> passing as parameter the name of the class you declared previuosly.

<pre><code>

#starts the webserver	
start( App )

</code></pre>

Run the script. If all it's OK the gui will be opened automatically opened in yout browser, otherwise you have to type in the address bar "http://127.0.0.1:8080".

The configuration.py file contains the IP and PORT values. You can change these values in order to make the gui accessible on other devices on the network.


All widgets constructors require three standard parameters that are in sequence:
-width in pixel
-height in pixel
-layout orientation (boolean, where True means orizontal orientation)


Styling
===
It's possible to change the style of the gui editing the style.css file. Here you can define the css properties of each gui widget.

