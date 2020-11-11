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
import os


class MyApp(App):
    def main(self):
        # creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width=300, height=200, style={'margin': '0px auto'})

        label = gui.Label("Select a fruit")

        selection_input = gui.SelectionInputWidget(['banana', 'apple', 'pear', 'apricot'], 'banana', 'text')
        selection_input.oninput.do(lambda emitter, value: label.set_text("event oninput: %s"%value))
        main_container.append([label, selection_input])

        # returning the root widget
        return main_container


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='0.0.0.0', port=0, start_browser=True, username=None, password=None)
