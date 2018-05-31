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

    def idle(self):
        #idle loop, you can place here custom code
        # avoid to use infinite iterations, it would stop gui update
        pass

    def main(self):
        #creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width=300, style={'margin':'0px auto'})

        
        
        m2 = gui.MenuItem('View', width=100, height=30)
        #m2.set_on_click_listener(self.menu_view_clicked)
        
        m12 = gui.MenuItem('Open', width=100, height=30)
        #m12.set_on_click_listener(self.menu_open_clicked)
        m111 = gui.MenuItem('Save', width=100, height=30)
        #m111.set_on_click_listener(self.menu_save_clicked)
        m112 = gui.MenuItem('Save as', width=100, height=30)
        #m112.set_on_click_listener(self.menu_saveas_clicked)
        m3 = gui.MenuItem('Dialog', width=100, height=30)
        #m3.set_on_click_listener(self.menu_dialog_clicked)

        m11 = gui.MenuItem('Save', [m111, m112], width=100, height=30)
        m1 = gui.MenuItem('File', [m11, m12], width=100, height=30)
        
        menu = gui.Menu([m1, m2, m3], width='100%', height='30px')
        

        menubar = gui.MenuBar(width='100%', height='30px')


        listview = gui.ListView(children={'0': gui.ListItem('zero'), 'n': 'n'})
        print( listview.append({'1': 'uno', '2': 'due'}) )
        print( listview.append(['tre', 'quattro']) )

        dropdown = gui.DropDown(children={'0': gui.DropDownItem('zero'), 'n': 'n'})
        print( dropdown.append({'1': 'uno', '2': 'due'}) )
        print( dropdown.append(['tre', 'quattro']) )

        table = gui.Table({'0': ['zero','zeroo','zerooo'], 'n':['n','nn','nnn']})
        print( table.append({'1': ['uno','unoo','unooo'], '2':['due','duee','dueee']}) )
        row3 = gui.TableRow()
        row3.append(['tre','tree','treee'])
        row4 = gui.TableRow()
        row4.append(['quattro','quattroo','quattrooo'])
        print( table.append({'3':row3 , '4':row4}) )
        print( table.append({'5':gui.TableRow(['5','55','555']) , '6':gui.TableRow(['6','66','666'])}) )
        print( table.append(gui.TableRow(['sette','settee','setteee']) ) )

        main_container.append([menubar, listview, dropdown, table])
        # returning the root widget
        return main_container


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='127.0.0.1', port=8081, host_name=None, start_browser=True, username=None, password=None)
