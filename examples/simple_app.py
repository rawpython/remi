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
        # the arguments are	width - height - layoutOrientationOrizontal
        wid = gui.Widget(120, 100, False, 10)
        self.lbl = gui.Label(100, 30, 'Hello %s!' % name)
        self.bt = gui.Button(100, 30, 'Press me!')

        # setting the listener for the onclick event of the button
        self.npressed = 0
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        # appending a widget to another, the first argument is a string key
        wid.append(self.lbl)
        wid.append(self.bt)

        # returning the root widget
        return wid

    # listener function
    def on_button_pressed(self):
        self.npressed += 1
        self.lbl.set_text('Button pressed %s times' % self.npressed)
        self.bt.set_text('Hi!')


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=False)
