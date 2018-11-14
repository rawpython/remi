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
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
        #static_file_path can be an array of strings allowing to define
        #  multiple resource path in where the resources will be placed
        super(MyApp, self).__init__(*args, static_file_path=res_path)

    def main(self):
        #creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width=300, height=200, style={'margin':'0px auto'})
        self.page.children['head'].add_child('test', '<meta patate>')
        self.page.children['body'].style['background-color'] = 'lightyellow'
        # returning the root widget
        return main_container
    
    def onload(self, emitter):
        print(">>>>>>>>> ON PAGE LOADED")

    def onerror(self, emitter, message, source, line, col):
        print(">>>>>>>>> ON ERROR: %s\n%s\n%s\n%s"%(message, source, line, col))
        self.execute_javascript('document.onkeydo')


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, debug=True, address='0.0.0.0', port=8081)
