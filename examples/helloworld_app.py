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

    def main(self):
        #creating a container VBox type, vertical
        wid = gui.VBox(width=300, height=200)

        #creating a text label
        self.lbl = gui.Label('Hello', width='80%', height='50%')

        #a button for simple interaction
        bt = gui.Button('Press me!', width=200, height=30)

        #setting up the listener for the click event
        bt.onclick.connect(self.on_button_pressed)
        
        #adding the widgets to the main container
        wid.append(self.lbl)
        wid.append(bt)

        # returning the root widget
        return wid

    # listener function
    def on_button_pressed(self, emitter):
        self.lbl.set_text('Hello World!')
        

if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True)
