

> ##*simple things makes the world simpler*

Just download it without installation
#[**_download GUI_**](https://github.com/dddomodossola/gui/archive/master.zip)

gui
===
Platform indipendent python gui library. In less than 100 Kbytes of source code, perfect for your diet.

![Alt text](https://raw.githubusercontent.com/dddomodossola/gui/master/res/screenshot.png "Widgets overview")

It allows to create platform indipendent GUI with python. The entire gui will be shown in the browser because it is represented in HTML. You have to write NO HTML code, because the library itself converts the python code automatically in HTML. When your app starts, it starts a webserver that will be accessible on your network.

Why another gui lib?
Ok, Kivy is the best, Tk is historical, pyQt is also good, but for every platform that appears we have to wait a porting. This lib allows to show a user interface everywhere there is a browser.

These widgets are available:
- Widget : like an empty panel
- Button
- TextInput : for the editable text
- SpinBox
- Label
- InputDialog
- ListView
- DropDown
- Image
- Table
- GenericObject : allows to show embedded object like pdf,swf..
- Slider
- ColorPicker
- Date
- FileSelectionDialog
- Menu
- MenuItem

A basic application appears like this:

<pre><code>
import gui
from gui import *


class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        # the arguments are	width - height - layoutOrientationOrizontal
        wid = gui.Widget(120, 100, False, 10)
        self.lbl = gui.Label(100, 30, 'Hello world!')
        self.bt = gui.Button(100, 30, 'Press me!')

        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        # appending a widget to another, the first argument is a string key
        wid.append('1', self.lbl)
        wid.append('2', self.bt)

        # returning the root widget
        return wid

    # listener function
    def on_button_pressed(self):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')


# starts the webserver
start(MyApp)
</code></pre>

In order to see the user interface, open your preferred browser (I use Chrome) and type "http://127.0.0.1:8081".
You can change the url address, edit the "configuration.py" file.

Tested on Android, Linux, Windows with Google Chrome web browser.
Usefull on raspberry pi for python script development. It allows to interact with your raspberry remotely from your mobile device.

FAQ
===
- Should I know HTML? NO, It is not required, you have to code only in python.
- Can I use this library with other browsers? Yes you can, but I haven't tested it and probably something couldn't work fine.
- It is open source? For sure!
- Where is the documentation? I'm working on this, but it requires time. If you need support you can contact me directly on dddomodossola(at)gmail(dot)com


Brief tutorial
===
Import gui library and all submodules.

<pre><code>

import gui
from gui import *

</code></pre>


Subclass the <code>App</code> class and declare a <code>main</code> function that will be the entry point of the application. Inside the main function you have to <code>return</code> the root widget.

<pre><code>

class MyApp( App ):
	def __init__( self, *args ):
		super( MyApp, self ).__init__( *args )
		
	def main( self ):
		lbl = gui.Label( 100, 30, "Hello world!" )
		
		#return of the root widget
		return lbl

</code></pre>


Outside the main class start the application calling the function <code>start</code> passing as parameter the name of the class you declared previously.

<pre><code>

#starts the webserver	
start( MyApp )

</code></pre>

Run the script. If all it's OK the gui will be opened automatically in your browser, otherwise you have to type in the address bar "http://127.0.0.1:8081".

The configuration.py file contains the IP and PORT values. You can change these values in order to make the gui accessible on other devices on the network.


All widgets constructors require three standard parameters that are in sequence:
- width in pixel
- height in pixel
- layout orientation (boolean, where True means orizontal orientation)


Styling
===
It's possible to change the style of the gui editing the style.css file. Here you can define the css properties of each gui widget.

