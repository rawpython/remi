
## *A Platform independent Python GUI library for your applications*

[![Join the chat at https://gitter.im/dddomodossola/remi](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/dddomodossola/remi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Remi is a GUI library for Python applications which transpiles an application's interface into HTML to be rendered in a web browser. This removes platform-specific dependencies and lets you easily develop cross-platform applications in Python!

Getting Started
===
[Download](https://github.com/dddomodossola/remi/archive/master.zip) or check out Remi from git and install

```
python setup.py install
```
or install directly using pip

```
pip install git+https://github.com/dddomodossola/remi.git
```

Then start the test script:
```
python widgets_overview_app.py
```

we recommend installing Remi into a virtualenv. Remi is not yet API stable.

Remi
===
Platform independent Python GUI library. In less than 100 Kbytes of source code, perfect for your diet.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/remi/res/screenshot.png "Widgets overview")

Remi enables developers to create platform independent GUI with Python. The entire GUI is converted to HTML and is rendered in your browser. **No HTML** is required, Remi automatically translates your Python code into HTML. When your app starts, it starts a webserver that will be accessible on your network.

These widgets are available:
- Widget : base class of all widgets. it can be used as a generic container
- HBox : horizontal container
- VBox : vertical container
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
- VideoPlayer

A basic application appears like this:

```py
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width = 120, height = 100)
        self.lbl = gui.Label('Hello world!')
        self.bt = gui.Button('Press me!')

        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        # appending a widget to another, the first argument is a string key
        container.append(self.lbl)
        container.append(self.bt)

        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')

# starts the webserver
start(MyApp)
```

In order to see the user interface, open your preferred browser and type "http://127.0.0.1:8081".
You can change the url address by specific **kwargs at `start` function call. This will be discussed later.

Tested on Android, Linux, Windows.
Useful on Raspberry Pi for Python script development. It allows to interact with your Raspberry Pi remotely from your mobile device.


FAQ
===
- **Why another GUI lib?**  
Kivy, PyQT and PyGObject all require native code for the host operating system, which means installing or compiling large dependencies. Remi needs only a web browser to show your GUI.

- **Do I need to know HTML?**  
NO, It is not required, you have to code only in Python.

- **Which browsers can I use this with?**  
I have developed this using Chrome (on Windows, Linux and Android) and haven't tested it elsewhere. It will probably work fine elsewhere though!

- **Is it open source?**  
For sure! Remi is released under the Apache License. See the ``LICENSE`` file for more details.

- **Where is the documentation?**  
I'm working on this, but it requires time. If you need support you can contact me directly on dddomodossola(at)gmail(dot)com

- **Do I need some kind of webserver?**
No, it's included.


Brief tutorial
===
Import Remi library and some other useful stuff.

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
		lbl = gui.Label( "Hello world!", width=100, height=30 )
		
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
- address: network interface ip
- port: listen port
- multiple_instance: boolean, if True multiple clients that connects to your script has different App instances
- enable_file_cache: boolean, if True enable resource caching
- update_interval: gui update interval in seconds
- start_browser: boolean that defines if the browser should be opened automatically at startup
- websocket_port: integer, port number for websocket communication
You can change these values in order to make the gui accessible on other devices on the network.


All widgets constructors accepts two standard **kwargs that are:
- width: can be expressed as int (and is interpreted as pixel) or as str (and you can specify the measure unit like '10%')
- height: can be expressed as int (and is interpreted as pixel) or as str (and you can specify the measure unit like '10%')


Events and callbacks
===
Widgets exposes a set of events that happens during user interaction. 
Such events are a convenient way to define the application behavior.
Each widget has its own callbacks, depending on the type of user interaction it allows.
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
        container = gui.VBox(width = 120, height = 100)
        self.lbl = gui.Label('Hello world!')
        self.bt = gui.Button('Press me!')

        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        # appending a widget to another, the first argument is a string key
        container.append(self.lbl)
        container.append(self.bt)

        # returning the root widget
        return container

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
The library allows to access these information easily.

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


Remote access
===
If you are using your REMI app remotely, with a DNS and a behind a firewall, you can specify special parameters in the `start` call:
- **websocket_port**: an integer number of the port used by websocket. Don't forget to NAT this port on your router;
- **host_name**: a string containing the host name or remote ip address that allows to access to your app.

```py
start(MyApp, address='0.0.0.0', port=8081, websocket_port=8082, host_name='myhostname.net') 
```


Standalone Execution
===
Remi is an effective solution for building your Remote Interface, but what about standalone execution? 
Sure you can use it with your browser, but for applications where remote access is not required, than the native GUI is the best.
This can be simply obtained joining REMI and [PyWebView](https://github.com/r0x0r/pywebview). 
Here is an example about this [desktop_app.py](https://github.com/dddomodossola/remi/blob/master/examples/desktop_app.py).


Authentication
===
In order to limit the remote access to your interface you can define a username and password. It consists in a simple authentication process.
Just define the parameters **username** and **password** in the start call:
```py
start(MyApp, username='myusername', password='mypassword') 
```


Styling
===
It's possible to change the style of the gui editing the style.css file. Here you can define the css properties of each gui widget.


Compatibility
===
Remi is made to be compatible from Python2.7 to Python3.X . Please notify compatibility issues.


Contributors
===
Thank you for collaborating with us to make Remi better!
The real power of opensource are contributors. Please feel free to partecipate to this project, and consider to add yourself to the following list.
Yes I know that github already provides a list of contributors, but I feel that I must mention who helps.
[Davide Rosa](https://github.com/dddomodossola)
[John Stowers](https://github.com/nzjrs)
[Claudio Cannatà](https://github.com/cyberpro4)
[Sam Pfeiffer](https://github.com/awesomebytes)
[Ken Thompson](https://github.com/KenT2)
[Paarth Tandon](https://github.com/Paarthri)
[Ally Weir](https://github.com/allyjweir)
[Timothy Cyrus](https://github.com/tcyrus)
[John Hunter Bowen](https://github.com/jhb188)
[Martin Spasov](https://github.com/SuburbanFilth)
[Wellington Castello](https://github.com/wcastello)
[PURPORC](https://github.com/PURPORC)
[ttufts](https://github.com/ttufts)
[Chris Braun](https://github.com/cryzed)
