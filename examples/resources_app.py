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
        #declare here resource folders as a dictionary, the parameter is *static_file_path*
        super(MyApp, self).__init__(*args, static_file_path={'my_res_folder':res_path})

    def main(self):
        #you can load an image from resource file declaration, as for remi convention /key:filename
        # you must declare resource folders in App.__init__ function using the parameter *static_file_path* dictionary
        resource_image = gui.Image("/my_res_folder:mine.png", width="30", height="30")

        #you can load an image directly by its path and filename using convenient function *load_resource*
        local_image = gui.Image(gui.load_resource("./res/mine.png"), width="30", height="30")

        standard_widget = gui.Widget(width="30", height="30", style={'background-repeat':'no-repeat'})

        standard_widget2 = gui.Widget(width="30", height="30", style={'background-repeat':'no-repeat'})

        #style image attributes like *background-image* requires to encase the filename with url('')
        # you can use the convenient function *to_uri* 
        standard_widget.style['background-image'] = gui.to_uri("/my_res_folder:mine.png")
        standard_widget2.style['background-image'] = gui.to_uri(gui.load_resource("./res/mine.png"))

        print(gui.to_uri("/my_res_folder:mine.png"))
        print(gui.to_uri(gui.load_resource("./res/mine.png")))
        main_container = gui.VBox(children=[resource_image, local_image, standard_widget, standard_widget2], width=200, height=300, style={'margin':'0px auto'})
        
        # returning the root widget
        return main_container


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='0.0.0.0', port=0, start_browser=True, username=None, password=None)
