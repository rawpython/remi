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
        wid = gui.VBox(width=300, height=200)
        lbl = gui.Label('Hello %s!' % name, width='80%', height='50%')
        lbl.style['margin'] = 'auto'

        self.bt = gui.Button('Press me!', width=200, height=30)
        self.bt.style['margin'] = 'auto 50px'

        # setting the listener for the onclick event of the button
        self.npressed = 0
        self.bt.set_on_click_listener(self, 'on_button_pressed', lbl)
        self.bt.set_on_mousedown_listener(self, 'on_button_mousedown', 'data1', 2,'three')
        
        #this will never be called, can't register an event more than one time
        self.bt.set_on_mouseup_listener(self, 'on_button_mouseup', 'data1') 
        
        self.bt.set_on_mouseup_listener(self, 'on_button_mouseup2')

        # appending a widget to another, the first argument is a string key
        wid.append(lbl)
        wid.append(self.bt)

        # returning the root widget
        return wid

    # listener function
    def on_button_pressed(self, widget, lbl):
        self.npressed += 1
        lbl.set_text('Button pressed %s times.' % self.npressed)
        self.bt.set_text('Hi!')
        
    def on_button_mousedown(self, widget, x, y, mydata1, mydata2, mydata3):
        print("x:%s  y:%s  data1:%s  data2:%s  data3:%s"%(x, y, mydata1, mydata2, mydata3))
        widget.style['background-color'] = 'red'
        
    def on_button_mouseup(self, widget, x, y, mydata1):
        print("x:%s  y:%s  data1:%s"%(x, y, mydata1))

    def on_button_mouseup2(self, widget, x, y):
        print("x:%s  y:%s  no userdata"%(x, y))
        widget.style['background-color'] = 'green'


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=False)
