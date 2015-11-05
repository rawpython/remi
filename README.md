
> ##*simple things make the world simpler*

let's start
===
Just download it without installation

##[**download RemI**](https://github.com/dddomodossola/remi/archive/master.zip)

Run the installation:
```
python setup.py install
```

Then start the test script:
```
python widgets_overview_app.py
```

RemI
===
Platform independent python gui library. In less than 100 Kbytes of source code, perfect for your diet.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/remi/res/screenshot.png "Widgets overview")

It allows to create platform independent GUI with python. The entire gui will be shown in the browser because it is represented in HTML. You have to write NO HTML code, because the library itself converts the python code automatically in HTML. When your app starts, it starts a webserver that will be accessible on your network.

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

```py
import remi.gui as gui
from remi import start, App

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
```

In order to see the user interface, open your preferred browser (I use Chrome) and type "http://127.0.0.1:8081".
You can change the url address, edit the "configuration.py" file.

Tested on Android, Linux, Windows with Google Chrome web browser.
Useful on raspberry pi for python script development. It allows to interact with your raspberry remotely from your mobile device.


FAQ
===
- Should I know HTML? NO, It is not required, you have to code only in python.
- Can I use this library with other browsers? Yes you can, but I haven't tested it and probably something couldn't work fine.
- Is it open source? For sure!
- Where is the documentation? I'm working on this, but it requires time. If you need support you can contact me directly on dddomodossola(at)gmail(dot)com


Brief tutorial
===
Import remi library and all submodules.

```py
import remi.gui as gui
from remi import start, App
```

Subclass the `App` class and declare a `main` function that will be the entry point of the application. Inside the main function you have to <code>return</code> the root widget.

```py
class MyApp( App ):
	def __init__( self, *args ):
		super( MyApp, self ).__init__( *args )
		
	def main( self ):
		lbl = gui.Label( 100, 30, "Hello world!" )
		
		#return of the root widget
		return lbl
```

Outside the main class start the application calling the function `start` passing as parameter the name of the class you declared previously.

```py
#starts the webserver	
start( MyApp )
```

Run the script. If all it's OK the gui will be opened automatically in your browser, otherwise you have to type in the address bar "http://127.0.0.1:8081".

You can customize optional parameters in the `start` call like.

```py
start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True) 
```

Parameters:
- address = network interface ip
- port: listen port
- multiple_instance: boolean, if True multiple clients that connects to your script has different App instances
- enable_file_cache: boolean, if True enable resource caching
- update_interval: gui update interval in seconds
- start_browser: boolean that defines if the browser should be opened automatically at startup
You can change these values in order to make the gui accessible on other devices on the network.


All widgets constructors require three standard parameters that are in sequence:
- width in pixel
- height in pixel
- layout orientation (boolean, where True means horizontal orientation)


Events and callbacks
===
Widgets exposes a set of events that happens during user interaction. 
Such events are a convenient way to define the application behavior.
Each widget has its own callbacks, depending on the type of input it allows.
The specific callbacks for the widgets will be illustrated later.

In order to register a function as an event listener you have to call a function like set_on_xxx_listener passing as parameters the instance of widget that will manage the event and the literal string name of the listener function.
Follows an example:

```py
import remi.gui as gui
from remi import start, App

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
```

In the shown example *self.bt.set_on_click_listener(self, 'on_button_pressed')* registers the self's *on_button_pressed* function as a listener for the event *onclick* exposed by the Button widget.
Simple, easy.


HTML Attribute accessibility
===
Sometimes could be required to access Widget's HTML representation in order to manipulate html attributes.
The library allows to access these information easly.

A simple example: It is the case where you would like to add an hover text to a widget. This can be achieved by the *title* attribute of an html tag.
In order to do this:

```py
    widget_instance.attributes['title'] = 'Your title content'
```

A special case of html attribute is the *style*.
The style attributes can be altered in this way:

```py
    widget_instance.style['color'] = 'red'
```

The assignment of a new attribute automatically creates it.

Take care about internally used attributes. These are:
- **class**: It is used to store the Widget class name for styling purpose
- **id**: It is used to store the instance id of the widget for callback management

Styling
===
It's possible to change the style of the gui editing the style.css file. Here you can define the css properties of each gui widget.
