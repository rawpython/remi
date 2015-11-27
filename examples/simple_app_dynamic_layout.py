"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import remi.gui as gui
from remi import start, App


class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        # Add the widget, it's the white background
        # self is for making the widget part of the class to be able to modify it
        self.wid = gui.Widget(400, 300, False, 10)

        # To make it prettier put a tittle of what is this demo
        self.tittle_label = gui.Label(350, 20, "Dynamical layout change demo")
        self.description_label = gui.Label(350, 80, 
            """Choose from the dropdown a widget and it will be added to the interface. 
            If you change the dropdown selection it will substitute it.""")


        # Create dropdown and it's contents
        self.dropdown = gui.DropDown(200, 20)

        choose_ddi = gui.DropDownItem(200, 20, "Choose...")
        button_ddi = gui.DropDownItem(200, 20, "Add button")
        label_ddi  = gui.DropDownItem(200, 20, "Add label")

        self.dropdown.append(choose_ddi)
        self.dropdown.append(button_ddi)
        self.dropdown.append(label_ddi)

        # Add a listener
        self.dropdown.set_on_change_listener(self.on_dropdown_change)

        # Add the dropdown to the widget
        self.wid.append(self.tittle_label)
        self.wid.append(self.description_label)
        self.wid.append(self.dropdown)

        # returning the root widget
        return self.wid

    # listener function
    def on_dropdown_change(self, evt, value):
        print "Chosen dropdown value: " + str(value)
        # Create the widget chosen
        if "button" in value:
            dynamic_widget = gui.Button(100, 100, "Button")
        elif "label" in value:
            dynamic_widget = gui.Label(100, 100, "Label")

        # Add it, as we use the same ID '3' it will overwrite it if we add it again
        self.wid.append(dynamic_widget,'key')

if __name__ == "__main__":
    start(MyApp)
