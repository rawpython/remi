<t1>Welcome</t1>

What is remi
Remi is a Graphical User Interface library (GUI) for python language. It is designed to be lightweight, multiplatform and remotable.
In a few kilobytes of source code you get a complete library that allows you build fancy powerful applications.
Remi applications are compatible with almost all platforms that allow to run python scripts (also on Android).
Your applications would benefit also of the remotable capability, making it possible to access your interfaces exactly as for a webpage with a common web browser. Suppose you build a raspberrypi GPIO commander, than you will be able to command your raspberrypi with your smartphone or laptop (or both at the same time). Suppose you write an application for office management, all coworkers will be able to access the application from every stations without installing nothing.  

Remi has an API interface similar to other common GUI libraries. The single GUI elements are called widgets, such as Buttons, TextInput fields, Tables and so on. The widgets collection is complete enough to make every kind of applications, from image processing to data plotting. If you feel comfortable with Object Oriented development you will feel great with it.

Here is presented a basic Hello World application:

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


<t2>Events<t2>
Now we can speak about events. Graphical User Interfaces must allow user interaction to execute commands and fill in data.
User interaction happens by means of a wide range of widgets. One of the most basic one is the Button.
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

This program shows a label and a button. When you click the button it triggers the event *onclick*. The event onclick is binded to the MyApp.on_button_click method that changes the text content of the label. The *on_button_click* method is called **listener** function, since it 'listens' for an event. Each listener function receives as first argument the 'event emitter' instance. This allows to handle multiple events with the same listener and get aware of the source of the event. In the shown example, the emitter will be the *self.button* instance. Here is an example of different buttons of which the onclick event is binded to the same listener.


```python
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def main(self):
        self.container = gui.VBox()

        # creating a Label instance
        self.label = gui.Label('A label')

        # creating a Button instance
        self.button1 = gui.Button('Button 1')
        self.button.onclick.do(self.on_button_click)

        # creating another Button instance
        self.button2 = gui.Button('Button 2')
        self.button.onclick.do(self.on_button_click)

        self.container.append([self.label, self.button1, self.button2])

        # returning the widget that will be shown
        return self.container

    def on_button_click(self, emitter):
        self.label.set_text("Pressed: " + emitter.get_text())

if __name__ == "__main__":
    # starting the application
    start(MyApp)
```


Children/parent
    Append
    remove_child

Style parameters

Attributes

Remi basics
    App
    Widgets
    Events
    Server
