<t1>Welcome</t1>
As shown in the Introduction tutorial, each listener function receives as first argument the 'event emitter' instance. This allows to handle multiple events with the same listener and get aware of the source of the event. 
Here is an example of different buttons of which the **onclick** event is binded to the same listener.

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
        self.button1.onclick.do(self.on_button_click)

        # creating another Button instance
        self.button2 = gui.Button('Button 2')
        self.button2.onclick.do(self.on_button_click)

        self.container.append([self.label, self.button1, self.button2])

        # returning the widget that will be shown
        return self.container

    def on_button_click(self, emitter):
        self.label.set_text("Pressed: " + emitter.get_text())

if __name__ == "__main__":
    # starting the application
    start(MyApp)
```

In this example the *onclick* event of both self.button1 and self.button2 is binded to the listener *on_button_click*. Of course you can create a different listener for each button, ie:

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
        self.button1.onclick.do(self.on_button_click_1)

        # creating another Button instance
        self.button2 = gui.Button('Button 2')
        self.button2.onclick.do(self.on_button_click_2)

        self.container.append([self.label, self.button1, self.button2])

        # returning the widget that will be shown
        return self.container

    def on_button_click_1(self, emitter):
        self.label.set_text("Pressed: " + emitter.get_text())

    def on_button_click_2(self, emitter):
        self.label.set_text("Pressed: " + emitter.get_text())

if __name__ == "__main__":
    # starting the application
    start(MyApp)
```

When binding an event to a listener function it is also possible to send custom user parameters. These parameters will be stored and sent to the listener function when the event occurs:

```python
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def main(self):
        self.container = gui.VBox()

        # creating a Label instance
        self.label = gui.Label('What to buy?')

        # creating a Button instance
        self.button1 = gui.Button('Candies')
        #next to the listener function, two additional custom parameters are passed to the binding function
        self.button1.onclick.do(self.on_button_click, 'chocolate', 'strawberry candies')

        # creating another Button instance
        self.button2 = gui.Button('Meat')
        #next to the listener function, two additional custom parameters are passed to the binding function
        self.button2.onclick.do(self.on_button_click, 'beef', 'polpette')

        self.container.append([self.label, self.button1, self.button2])

        # returning the widget that will be shown
        return self.container

    #here we will receive the additional parameters
    def on_button_click(self, emitter, param1, param2):
        self.label.set_text("Buy list: " + param1 + ' ' + param2)

if __name__ == "__main__":
    # starting the application
    start(MyApp)
```

In this example next to the listener function, two additional custom parameters are passed to the binding function **do**. The button1 sends 'chocolate' and 'strawberry candies', the button2 sends 'beef' and 'polpette'. Of course the listener function must be able to receive these parameters, and so two additionals parameters are in its definition.




Event classes

The event mechanism
    Widgets id

    Javascript generate events
        sendCallback
        sendCallbackParam
    
    Other widgets can trigger an event

    Event parameters

    User parameters (additional parameters)
    