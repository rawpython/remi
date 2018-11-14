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
        #custom additional html head tags
        my_html_head = """<title>Bootstrap Test</title>"""

        #Load Boostrap Ressources from Online Source
        #One could download the files and put them into res folder for access without internet connection

        #Not all the Bootstrap functionality will work!! Just basic styling is possible.
 
        #For valid Bootstrap Classes check:  https://www.w3schools.com/bootstrap/bootstrap_ref_all_classes.asp

        #custom css
        my_css_head = """
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
            """

        #custom js
        my_js_head = """
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
            """
        #appending elements to page header
        self.page.children['head'].add_child('myhtml', my_html_head)
        self.page.children['head'].add_child('mycss', my_css_head)
        self.page.children['head'].add_child('myjs', my_js_head)

        #creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width='500px', height='500px', style={'margin':'0px auto','padding':'10px'})

        #Label
        self.lbl = gui.Label("  Label with Lock Icon")
        self.lbl.add_class("glyphicon glyphicon-lock label label-primary")
        
        #Text Input
        self.tf = gui.TextInput(hint='Your Input')
        self.tf.add_class("form-control input-lg")

        #Drop Down
        self.dd = gui.DropDown(width='200px')
        self.dd.style.update({'font-size':'large'})
        self.dd.add_class("form-control dropdown")
        self.item1 = gui.DropDownItem("First Choice")
        self.item2 = gui.DropDownItem("Second Item")
        self.dd.append(self.item1,'item1')
        self.dd.append(self.item2,'item2')
             
        #Table
        myList = [  ('ID','Lastname','Firstname','ZIP','City'),
                    ('1','Pan','Peter','99999','Neverland'),
                    ('2','Sepp','Schmuck','12345','Examplecity')  ]

        self.tbl = gui.Table.new_from_list(content=myList,width='400px',height='100px',margin='10px')
        self.tbl.add_class("table table-striped")
        
        #Buttons

        #btn adds basic design to a button like rounded corners and stuff
        #btn-success, btn-danger and similar adds theming based on the function
        #if you use btn-success without btn, the button will be standard, but with green background

        self.bt1 = gui.Button("OK", width="100px")
        self.bt1.add_class("btn-success")                   #Bootstrap Class:  btn-success

        self.bt2 = gui.Button("Abbruch",width="100px")
        self.bt2.add_class("btn btn-danger")                #Bootstrap Class:  btn btn-danger
                
        
        #Build up the gui
        main_container.append(self.lbl,'lbl')
        main_container.append(self.tf,'tf')
        main_container.append(self.dd,'dd')
        main_container.append(self.tbl,'tbl')
        main_container.append(self.bt1,'btn1')
        main_container.append(self.bt2,'btn2')
        
        # returning the root widget
        return main_container
    

if __name__ == "__main__":
    # starts the webserver
    start(MyApp, debug=True, address='127.0.0.1', port=8085, start_browser=True, username=None, password=None)


