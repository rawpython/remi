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
import remi.dialogs as dialogs
from remi import start, App


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        # the margin 0px auto centers the main container
        verticalContainer = gui.Widget(
            width=540, margin='0px auto',
            style={'display': 'block', 'overflow': 'hidden'})

        error_bt = gui.Button('Show error dialog',
                              width=200, height=30, margin='10px')
        
        # setting the listener for the onclick event of the button
        error_bt.set_on_click_listener(self.show_error_dialog)

        verticalContainer.append(error_bt)

        # returning the root widget
        return verticalContainer

    def show_error_dialog(self, widget):
        dialogs.Error('Some error message', width=300).show(self)
        
if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)

    start(MyApp, debug=True, address='0.0.0.0', start_browser=True)
