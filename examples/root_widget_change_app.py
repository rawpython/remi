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

""" This example shows how to change the App's root widget. This allows to  
    mimic a page change behaviour. 
    It is done by the App.set_root_widget(mywidget) method.

"""

import remi.gui as gui
from remi import start, App
import os


class MyApp(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
        # static_file_path can be an array of strings allowing to define
        #  multiple resource path in where the resources will be placed
        super(MyApp, self).__init__(*args, static_file_path=res_path)

    def main(self):
        # creating two "pages" widgets to be shown alternatively
        lbl = gui.Label("Page 2. Press the button to change the page.", style={'font-size': '20px'})
        bt2 = gui.Button("change page")
        page2 = gui.HBox(children=[lbl, bt2], style={'margin': '0px auto', 'background-color': 'lightgray'})

        lbl = gui.Label("Page 1. Press the button to change the page.", style={'font-size': '20px'})
        bt1 = gui.Button("change page")
        page1 = gui.VBox(children=[lbl, bt1],
                         style={'width': '300px', 'height': '200px', 'margin': '0px auto', 'background-color': 'white'})

        bt1.onclick.do(self.set_different_root_widget, page2)
        bt2.onclick.do(self.set_different_root_widget, page1)

        # returning the root widget
        return page1

    def set_different_root_widget(self, emitter, page_to_be_shown):
        self.set_root_widget(page_to_be_shown)


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='0.0.0.0', port=0, start_browser=True, username=None, password=None)
