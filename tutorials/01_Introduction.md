<h1>Welcome</h1>
<p style="white-space:pre">

**Remi** is a Graphical User Interface library (GUI) for the Python language. Remi is designed to be lightweight, multiplatform, and accessed remotely via a web browser. In a few kilobytes of source code, you get a complete library that allows you to build rich and robust applications. Remi applications are compatible with almost all platforms that can run Python scripts (Remo also works on Android). You can even access your Remi applications remotely with a browser, making it possible to access your interfaces as a web page. 

Suppose you build a GPIO command interface for a Raspberry Pi. With a Remi GUI, you can send commands to your Raspberry Pi with your smartphone or laptop (or even both at the same time). 

Suppose you write an application for office management: all coworkers can access the application from their workstations using just a browser.

Remi has an API interface similar to other common GUI libraries. Each single GUI element is called a widget. Remi comes with many widgets such as Buttons, TextInput fields, Tables. The widgets collection is complete enough to make almost any kind of GUI application you would want. If you are comfortable with Object-Oriented development, you should be able to learn to build GUI applications quickly.

Presented below is a basic Hello World application:
</p>

```python
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def main(self):
        # creating a Label instance with 'Hello World!' content 
        self.label = gui.Label('Hello World!')

        # returning the widget that will be shown
        return self.label

if __name__ == "__main__":
    # starting the application
    start(MyApp)
```

When you run this script the web browser appears with the 'Hello World!' text.

So, give it a try, let's install remi:
```
pip install remi
```

Copy and paste the example above and run it. Let's say together.. WoooW!
Few thoughts, you installed it in a minute, no errors, no gigabytes of download, just a working script with a user interface.

The shown example is composed as follow:
- Importing the remi library
- Created a *MyApp* class that inherits the *App* class
- Created a *main* method that returns the widget to be shown
- Started the application by *start* function, giving it your *MyApp* class as parameter


<h2>Events</h2>
Now we can speak about events. 
Graphical User Interfaces must allow user interaction to execute commands and fill in data.
User interaction happens by means of a wide range of widgets. 
One of the most basic one is the Button.
Beside the graphical aspect, a button is characterized by an event that gets triggered by the **click** action.
An event is something that happens and for which the develper can link a function to, that will be executed when it occurs.
To better explain events, we can make a simple example that shows the "Hey mate" text when a button is clicked.

```python
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def main(self):
        self.container = gui.VBox()

        # creating a Label instance
        self.label = gui.Label('A label')

        # creating a Button instance
        self.button = gui.Button('Press Me')
        #the self.on_button_click method will be called when the button gets clicked
        self.button.onclick.do(self.on_button_click)

        self.container.append([self.label, self.button])

        # returning the widget that will be shown
        return self.container

    def on_button_click(self, emitter):
        self.label.set_text("Hey mate")

if __name__ == "__main__":
    # starting the application
    start(MyApp)
```
This program shows a label and a button. When clicked, the button triggers the event *onclick*. The event onclick is binded to the MyApp.on_button_click method that changes the text content of the label. The *on_button_click* method is called **listener** function, since it 'listens' for an event. Each listener function receives as first argument the 'event emitter' instance. This allows to handle multiple events with the same listener and get aware of the source of the event. In the shown example, the emitter will be the *self.button* instance. 


<h2>Append, widgets relationship, children</h2>

The "gui.Tag" is the basic remi class that represent an html element. Tags are arranged in a tree data structure. Non-Container tags are the leafs of the tree, thus can't contain childrens. Container tags (the ones that inherits the gui.Container class) can contain other tags. A Container tag stores his children in the *tag.childrens* dictionary. Each element in this dictionary is characterized by a *key* and a *value*. The key can be set by developer when appending the related child. The value is the child instance.
The tag.add_child(key, instance) method allows to add a child tag to another.
The tag.remove_child(instance) method allows to remove a child tag. 

The "gui.Widget" class inherits the "gui.Tag" class. Widget class exposes another method to add a child widget, it is called *widget.append(instance, key=None)*. 
A Tag is called "parent" for the child appended to it. A child can retrieve the parent instance with the method *tag.get_parent()*.

Style parameters

Attributes

Remi basics
    App
    Widgets
    Events
    Server
