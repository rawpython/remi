
<p align="center">
    <img src="https://raw.githubusercontent.com/dddomodossola/remi/development/remi/res/logo.png" width="430">
</p>

<p align="center" style="font-size:30px;">
    A Platform-independent Python GUI library for your applications
</p>


Remi is a GUI library for Python applications which transpiles an application's interface into HTML to be rendered in a web browser. This removes platform-specific dependencies and lets you easily develop cross-platform applications in Python!


Do you need support? Reach us on:
<p align="center">
<a href="https://www.reddit.com/r/RemiGUI" style="font-size:25px">Reddit - (subreddit RemiGUI)</a>
</p>


Would you like a **rapid overview**? Here is an online example, thanks to the powerful repl.it 
<p align="center">
<a href="http://remiexample--daviderosa.repl.co/ " style="font-size:25px">live example at repl.it</a>
</p>


There is also a drag n drop GUI editor. Look at the [Editor](https://github.com/dddomodossola/remi/tree/master/editor) subfolder to download your copy, or try it first at:
<p align="center">
<a href="http://remiguieditor--daviderosa.repl.co/ " style="font-size:25px">live try GUI editor overview at repl.it</a>
</p>


Changelog
===
The current branch includes a bunch of updates.
The major changes are related to the event infrastructure. Now, an event listener can be registered as:
```
widget.eventname.connect(listener)
```

instead of:
```
widget.set_on_xxx_listener(listener)
```

And so, in order to register a listener for the *onclick* event, you can do *button.onclick.connect(myapp.on_button_pressed)*.

The previous dialect is still compatible.


The parameter host_name is now deprecated. The server automatically catches the address where to connect from the HTTP request.


Getting Started
===
For a **stable** version:
```
pip install remi
```

For the most updated **experimental** version [Download](https://github.com/dddomodossola/remi/archive/master.zip) or check out Remi from git and install

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


Remi
===
Platform independent Python GUI library. In less than 100 Kbytes of source code, perfect for your diet.

<p align="center">
    <img src="https://raw.githubusercontent.com/dddomodossola/remi/development/remi/res/screenshot.png" title="Widgets overview">
</p>

Remi enables developers to create platform independent GUI with Python. The entire GUI is converted to HTML and is rendered in your browser. **No HTML** is required, Remi automatically translates your Python code into HTML. When your app starts, it starts a web server that will be accessible on your network.

A basic application appears like this:

```py
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=120, height=100)
        self.lbl = gui.Label('Hello world!')
        self.bt = gui.Button('Press me!')

        # setting the listener for the onclick event of the button
        self.bt.onclick.connect(self.on_button_pressed)

        # appending a widget to another, the first argument is a string key
        container.append(self.lbl)
        container.append(self.bt)

        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')

# starts the web server
start(MyApp)
```

In order to see the user interface, open your preferred browser and type "http://127.0.0.1:8081".
You can change the URL address by specific **kwargs at `start` function call. This will be discussed later.

Tested on Android, Linux, Windows.
Useful on Raspberry Pi for Python script development. It allows interacting with your Raspberry Pi remotely from your mobile device.


FAQ
===
- **Why another GUI lib?**
Kivy, PyQT, and PyGObject all require native code for the host operating system, which means installing or compiling large dependencies. Remi needs only a web browser to show your GUI.

- **Do I need to know HTML?**
NO, It is not required, you have to code only in Python.

- **Which browsers can I use this with?**
Tested on Chrome Firefox and Edge (on Windows, Linux, and Android) and haven't tested it elsewhere. It will probably work fine elsewhere though!

- **Is it open source?**
For sure! Remi is released under the Apache License. See the ``LICENSE`` file for more details.

- **Do I need some kind of web server?**
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
class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        lbl = gui.Label("Hello world!", width=100, height=30)

        # return of the root widget
        return lbl
```

Outside the main class start the application calling the function `start` passing as parameter the name of the class you declared previously.

```py
# starts the webserver
start(MyApp)
```

Run the script. If all it's OK the GUI will be opened automatically in your browser, otherwise, you have to type in the address bar "http://127.0.0.1:8081".

You can customize optional parameters in the `start` call like.

```py
start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False, enable_file_cache=True, update_interval=0.1, start_browser=True)
```

Parameters:
- address: network interface IP
- port: listen port
- multiple_instance: boolean, if True multiple clients that connect to your script has different App instances (identified by unique cookie session identifier)
- enable_file_cache: boolean, if True enable resource caching
- update_interval: GUI update interval in seconds. If zero, the update happens at each change. If zero, the App.idle method is not called.
- start_browser: boolean that defines if the browser should be opened automatically at startup
- standalone: boolean, indicates where to run the application as a standard Desktop application with its own window. If False, the interface is shown in a browser webpage.

Additional Parameters:
- username: for a basic HTTP authentication
- password: for a basic HTTP authentication
- certfile: SSL certificate filename
- keyfile: SSL key file
- ssl_version: authentication version (i.e. ssl.PROTOCOL_TLSv1_2). If None disables SSL encryption

All widgets constructors accept two standards**kwargs that are:
- width: can be expressed as int (and is interpreted as a pixel) or as str (and you can specify the measuring unit like '10%')
- height: can be expressed as int (and is interpreted as a pixel) or as str (and you can specify the measuring unit like '10%')


Events and callbacks
===
Widgets expose a set of events that happen during user interaction.
Such events are a convenient way to define the application behavior.
Each widget has its own callbacks, depending on the type of user interaction it allows.
The specific callbacks for the widgets will be illustrated later.

In order to register a function as an event listener you have to call a function like eventname.connect (i.e. onclick.connect) passing as parameters the callback that will manage the event.
Follows an example:

```py
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=120, height=100)
        self.lbl = gui.Label('Hello world!')
        self.bt = gui.Button('Press me!')

        # setting the listener for the onclick event of the button
        self.bt.onclick.connect(self.on_button_pressed)

        # appending a widget to another, the first argument is a string key
        container.append(self.lbl)
        container.append(self.bt)

        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')

# starts the web server
start(MyApp)
```

In the shown example *self.bt.onclick.connect(self.on_button_pressed)* registers the self's *on_button_pressed* function as a listener for the event *onclick* exposed by the Button widget.
Simple, easy.

Listener's callbacks will receive the emitter's instance firstly, then all other parameters provided by the specific event.


Besides the standard event registration (as aforementioned), it is possible to pass user parameters to listener functions. This can be achieves appending parameters to the *connect* function call.

```py
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width=120, height=100)
        self.lbl = gui.Label('Hello world!')
        self.bt = gui.Button('Hello name!')
        self.bt2 = gui.Button('Hello name surname!')

        # setting the listener for the onclick event of the buttons
        self.bt.onclick.connect(self.on_button_pressed, "Name")
        self.bt2.onclick.connect(self.on_button_pressed, "Name", "Surname")

        # appending a widget to another
        container.append(self.lbl)
        container.append(self.bt)
        container.append(self.bt2)

        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self, widget, name='', surname=''):
        self.lbl.set_text('Button pressed!')
        widget.set_text('Hello ' + name + ' ' + surname)

# starts the web server
start(MyApp)
```

This allows great flexibility, getting different behaviors with the same event listener definition.


HTML Attribute accessibility
===
Sometimes could be required to access Widget's HTML representation in order to manipulate HTML attributes.
The library allows accessing this information easily.

A simple example: It is the case where you would like to add a hover text to a widget. This can be achieved by the *title* attribute of an HTML tag.
In order to do this:

```py
    widget_instance.attributes['title'] = 'Your title content'
```

A special case of HTML attribute is the *style*.
The style attributes can be altered in this way:

```py
    widget_instance.style['color'] = 'red'
```

The assignment of a new attribute automatically creates it.

For a reference list of HTML attributes, you can refer to https://www.w3schools.com/tags/ref_attributes.asp

For a reference list of style attributes, you can refer to https://www.w3schools.com/cssref/default.asp

Take care about internally used attributes. These are:
- **class**: It is used to store the Widget class name for styling purpose
- **id**: It is used to store the instance id of the widget for callback management


Remote access
===
If you are using your REMI app remotely, with a DNS and behind a firewall, you can specify special parameters in the `start` call:
- **port**: HTTP server port. Don't forget to NAT this port on your router;

```py
start(MyApp, address='0.0.0.0', port=8081)
```


Standalone Execution
===
I suggest using the browser as a standard interface window.

However, you can avoid using the browser.
This can be simply obtained joining REMI and [PyWebView](https://github.com/r0x0r/pywebview).
Here is an example about this [standalone_app.py](https://github.com/dddomodossola/remi/blob/development/examples/standalone_app.py).

**Be aware that PyWebView uses qt, gtk and so on to create the window. An outdated version of these libraries can cause UI problems. If you experience UI issues, update these libraries, or better avoid standalone execution.**


Authentication
===
In order to limit the remote access to your interface, you can define a username and password. It consists of a simple authentication process.
Just define the parameters **username** and **password** in the start call:
```py
start(MyApp, username='myusername', password='mypassword')
```


Styling
===
In order to define a new style for your app, you have to do the following.
Create a *res* folder and pass it to your App class constructor:
```python
class MyApp(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(MyApp, self).__init__(*args, static_file_path=res_path)
```

Make a copy the standard style.css from the remi folder and paste it inside your *res* folder. Edit it in order to customize.
This way the standard *style.css* file gets overridden by the one you created.


Compatibility
===
Remi is made to be compatible from Python2.7 to Python3.X. Please notify compatibility issues.


Security
===
Remi should be intended as a standard desktop GUI framework.
The library itself doesn't implement security strategies, and so it is advised to not expose its access to unsafe public networks.

When loading data from external sources, consider protecting the application from potential javascript injection before displaying the content directly.


Supporting the project
===
*Are you able to support the Remi project?*

Are you aware that remi is on Patreon?
That's a brilliant way to support this project.

**[SUPPORT Remi now](https://patreon.com/remigui)**

Also, a small amount is really welcome.


Contributors
===
Thank you for collaborating with us to make Remi better!

The real power of opensource is contributors. Please feel free to participate in this project, and consider to add yourself to the following list.
Yes, I know that GitHub already provides a list of contributors, but I feel that I must mention who helps.

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

[Alan Yorinks](https://github.com/MrYsLab)

[Bernhard E. Reiter](https://github.com/bernhardreiter)

[saewoonam](https://github.com/saewoonam)


Projects using Remi
===
[Web based dynamic reconfigure for ROS robots](https://github.com/awesomebytes/web_dyn_reconf)

[razmq](https://github.com/MrYsLab/razmq)

[Espresso-ARM](http://hallee.github.io/espresso-arm/)

[PiPresents](https://github.com/KenT2/pipresents-gapless)

[The Python Banyan Framework](https://github.com/MrYsLab/python_banyan)


Other Implementations
===
Here are listed other implementations of this library:
- [**cremi**](https://github.com/cyberpro4/cremi): (WIP) developed for your C++ projects by [Claudio Cannatà](https://github.com/cyberpro4).
