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
        #creating a container GridBox type
        main_container = gui.GridBox(width='100%', height='100%', style={'margin':'0px auto'})
        
        label = gui.Label('This is a label')
        label.style['background-color'] = 'lightgreen'
        
        button = gui.Button('Change layout', height='100%')
        button.set_on_click_listener(self.redefine_grid, main_container)
        
        text = gui.TextInput()
        
        #defining layout matrix, have to be iterable of iterable
        main_container.define_grid(['ab',
                                    'ac'])
        main_container.append({'a':label, 'b':button, 'c':text})
        #setting sizes for rows and columns
        main_container.style.update({'grid-template-columns':'10% 90%', 'grid-template-rows':'10% 90%'})

        # returning the root widget
        return main_container
    
    def redefine_grid(self, emitter, container):
        #redefining grid layout
        container.define_grid(['cab'])
        container.style.update({'grid-template-columns':'33% 33% 33%', 'grid-template-rows':'50%'})
        #emitter.set_text("Done")


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='127.0.0.1', port=8081, websocket_port=0, host_name=None, start_browser=True, username=None, password=None)
