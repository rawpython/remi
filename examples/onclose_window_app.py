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
        # margin 0px auto allows to center the app to the screen
        wid = gui.VBox(width=300, height=200, margin='0px auto')

        lbl = gui.Label("Close or reload the page, the console thread will stop automatically.")
        wid.append(lbl)

        #add the following 3 lines to your app and the on_window_close method to make the console close automatically
        tag = gui.Tag(_type='script')
        tag.add_child("javascript", """window.onunload=function(e){sendCallback('%s','%s');return "close?";};""" % (str(id(self)), "on_window_close")) 
        wid.add_child("onunloadevent", tag)
        
        # returning the root widget
        return wid
        
    def on_window_close(self):
        #here you can handle the unload
        print("app closing")
        self.close()


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True, start_browser=True) #standalone=True)
