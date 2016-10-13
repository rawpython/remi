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
        wid = gui.VBox(width=300, height=400)
        
        self.tree = gui.TreeView(width=200, height=300)
        self.tree.append(gui.TreeItem("item1", width=100))
        it2 = gui.TreeItem("item2", width=100)
        self.tree.append(it2)
        
        it2.append(gui.TreeItem("sub item1"))
        subit2 = gui.TreeItem("sub item2")
        it2.append(subit2)
        it2.append(gui.TreeItem("sub item3"))
        
        subit2.append(gui.TreeItem("sub sub item1"))
        subit2.append(gui.TreeItem("sub sub item2"))
        subit2.append(gui.TreeItem("sub sub item3"))
        
        wid.append(self.tree)

        # returning the root widget
        return wid


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True)
