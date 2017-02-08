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
from cli import start_app


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        #margin 0px auto allows to center the app to the screen
        wid = gui.VBox(width=300, height=200, margin='0px auto')
        lbl = gui.Label('Hello %s!' % name, width='80%', height='50%')
        lbl.style['margin'] = 'auto'

        bt = gui.Button('Press me!', width=200, height=30)
        bt.style['margin'] = 'auto 50px'

        # setting the listener for the onclick event of the button
        self.npressed = 0

        bt.set_on_click_listener(self.on_button_pressed, lbl)
        bt.set_on_mousedown_listener(self.on_button_mousedown, 'data1', 2,'three')
        
        #this will never be called, can't register an event more than one time
        bt.set_on_mouseup_listener(self.on_button_mouseup, 'data1') 

        # appending a widget to another, the first argument is a string key
        wid.append(lbl)
        wid.append(bt)

        # returning the root widget
        return wid

    # listener function
    def on_button_pressed(self, widget, lbl):
        self.npressed += 1
        lbl.set_text('Button pressed %s times.' % self.npressed)
        widget.set_text('Hi!')
        
    def on_button_mousedown(self, widget, x, y, mydata1, mydata2, mydata3):
        print("x:%s  y:%s  data1:%s  data2:%s  data3:%s"%(x, y, mydata1, mydata2, mydata3))
        
    def on_button_mouseup(self, widget, x, y, mydata1):
        print("x:%s  y:%s  data1:%s"%(x, y, mydata1))

    def on_button_mouseup2(self, widget, x, y):
        print("x:%s  y:%s  no userdata"%(x, y))


if __name__ == "__main__":
    start_app(MyApp, debug=True)
