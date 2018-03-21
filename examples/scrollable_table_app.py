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
        #margin 0px auto allows to center the app to the screen
        container = gui.Widget(width=350, height=200, margin='0px auto')
        container.style['overflow'] = 'auto'
        self.table = gui.Table.new_from_list([('ID', 'First Name', 'Last Name'),
                                   ('101', 'Danny', 'Young'),
                                   ('102', 'Christine', 'Holand'),
                                   ('103', 'Lars', 'Gordon'),
                                   ('104', 'Roberto', 'Robitaille'),
                                   ('105', 'Maria', 'Papadopoulos'),
                                   ('106', 'Teresa', 'Ma'),
                                   ('107', 'Richard', 'Stal'),
                                   ('108', 'Linus', 'Tor'),
                                   ('109', 'Mattew', 'Zender'),
                                   ('110', 'Francisco', 'Franco'),
                                   ('111', 'Ros', 'Illedi')], width='100%', height='100%', margin='0px')

        container.append(self.table)

        # returning the root widget
        return container


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True)
