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
        # the arguments are	width - height - layoutOrientationOrizontal
        wid = gui.Widget(width=300, height=200)
        wid.set_layout_orientation(gui.Widget.LAYOUT_VERTICAL)
        self.lbl = gui.Label('Press the button', width='80%', height='50%')
        self.lbl.style['margin'] = 'auto'
        self.bt = gui.Button('Press me!', width=200, height=30)
        self.bt.style['margin'] = 'auto 50px'

        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        # appending a widget to another, the first argument is a string key
        wid.append(self.lbl)
        wid.append(self.bt)

        # returning the root widget
        return wid

    # listener function
    def on_button_pressed(self):
        self.lbl.set_text('A notification message should appear.')
        self.bt.set_text('Hi!')
        self.notification_message("Message title", "Hello world!", "")


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True)
