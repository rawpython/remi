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
        wid = gui.VBox(width=300, height=300)

        self._items = ("/test/1", "/test/7")

        self.dd = gui.DropDown.new_from_list(self._items, width='80%', height=40)
        self.list = gui.ListView.new_from_list(self._items, width='80%', height='50%')
        self.ent = gui.TextInput(width=200, height=30, hint='enter words')
        self.bt = gui.Button('Update Models', width=200, height=30)
        self.bt.style['margin'] = 'auto 50px'

        self.bt.set_on_click_listener(self.on_button_pressed)

        # appending a widget to another, the first argument is a string key
        wid.append(self.dd)
        wid.append(self.list)
        wid.append(self.ent)
        wid.append(self.bt)

        # returning the root widget
        return wid

    # listener function
    def on_button_pressed(self, widget):
        txt = self.ent.get_text()
        if txt:
            self._items = tuple("/test/%s" % i for i in txt.split(' '))
        self.dd.synchronize_values(self._items)
        self.list.synchronize_values(self._items)


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True)
