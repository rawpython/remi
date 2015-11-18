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
from threading import Timer


class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def idle(self):
        """ Usefull function to schedule tasks. 
        Called every configuration.UPDATE_ITERVAL """
        super(MyApp, self).idle()
        
    def main(self):
        verticalContainer = gui.Widget(640, 900, gui.Widget.LAYOUT_VERTICAL, 10)

        horizontalContainer = gui.Widget(620, 620, gui.Widget.LAYOUT_HORIZONTAL, 10)

        subContainerLeft = gui.Widget(340, 530, gui.Widget.LAYOUT_VERTICAL, 10)
        self.img = gui.Image(100, 100, '/res/logo.png')
        self.img.set_on_click_listener(self, 'on_img_clicked')

        self.table = gui.Table(300, 200)
        self.table.from_2d_matrix([['ID', 'First Name', 'Last Name']
                                  ,['101', 'Danny', 'Young']
                                  ,['102', 'Christine', 'Holand']
                                  ,['103', 'Lars', 'Gordon']
                                  ,['104', 'Roberto', 'Robitaille']
                                  ,['105', 'Maria', 'Papadopoulos']])

        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Widget(240, 560, gui.Widget.LAYOUT_VERTICAL, 10)

        self.count=0
        self.counter=gui.Label(200, 30, '')
        
        self.lbl = gui.Label(200, 30, 'This is a LABEL!')

        self.bt = gui.Button(200, 30, 'Press me!')
        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        self.txt = gui.TextInput(200, 30)
        self.txt.set_text('This is a TEXTAREA')
        self.txt.set_on_change_listener(self, 'on_text_area_change')

        self.spin = gui.SpinBox(200, 30, 100)
        self.spin.set_on_change_listener(self, 'on_spin_change')

        self.check = gui.CheckBoxLabel(200, 30, 'Label checkbox', True)
        self.check.set_on_change_listener(self, 'on_check_change')

        self.btInputDiag = gui.Button(200, 30, 'Open InputDialog')
        self.btInputDiag.set_on_click_listener(self, 'open_input_dialog')

        self.btFileDiag = gui.Button(200, 30, 'File Selection Dialog')
        self.btFileDiag.set_on_click_listener(self, 'open_fileselection_dialog')

        self.btUploadFile = gui.FileUploader(200, 30, './')
        self.btUploadFile.set_on_success_listener( self, 'fileupload_on_success')
        self.btUploadFile.set_on_failed_listener( self, 'fileupload_on_failed')

        self.listView = gui.ListView(300, 120)
        self.listView.set_on_selection_listener(self,"list_view_on_selected")
        li0 = gui.ListItem(279, 20, 'Danny Young')
        li1 = gui.ListItem(279, 20, 'Christine Holand')
        li2 = gui.ListItem(279, 20, 'Lars Gordon')
        li3 = gui.ListItem(279, 20, 'Roberto Robitaille')
        self.listView.append('0', li0)
        self.listView.append('1', li1)
        self.listView.append('2', li2)
        self.listView.append('3', li3)

        self.link = gui.Link(200, 20, "http://localhost:8081", "A link to here")

        self.dropDown = gui.DropDown(200, 20)
        c0 = gui.DropDownItem(200, 20, 'DropDownItem 0')
        c1 = gui.DropDownItem(200, 20, 'DropDownItem 1')
        self.dropDown.append('0', c0)
        self.dropDown.append('1', c1)
        self.dropDown.set_on_change_listener(self, 'drop_down_changed')
        self.dropDown.set_value('DropDownItem 0')

        self.slider = gui.Slider(200, 20, 10, 0, 100, 5)
        self.slider.set_on_change_listener(self, 'slider_changed')

        self.colorPicker = gui.ColorPicker(200, 20, '#ffbb00')
        self.colorPicker.set_on_change_listener(self, 'color_picker_changed')

        self.date = gui.Date(200, 20, '2015-04-13')
        self.date.set_on_change_listener(self, 'date_changed')

        self.video = gui.VideoPlayer(480, 270, 'http://www.w3schools.com/tags/movie.mp4', 
                    'http://www.oneparallel.com/wp-content/uploads/2011/01/placeholder.jpg')

        # appending a widget to another, the first argument is a string key
        subContainerRight.append('0', self.counter)        
        subContainerRight.append('1', self.lbl)
        subContainerRight.append('2', self.bt)
        subContainerRight.append('3', self.txt)
        subContainerRight.append('4', self.spin)
        subContainerRight.append('checkbox', self.check)
        subContainerRight.append('5', self.btInputDiag)
        subContainerRight.append('5_', self.btFileDiag)
        subContainerRight.append('5__', gui.FileDownloader(200, 30, 'download test', '../remi/res/logo.png'))
        subContainerRight.append('5___', self.btUploadFile)
        subContainerRight.append('6', self.dropDown)
        subContainerRight.append('7', self.slider)
        subContainerRight.append('8', self.colorPicker)
        subContainerRight.append('9', self.date)
        self.subContainerRight = subContainerRight

        subContainerLeft.append('0', self.img)
        subContainerLeft.append('1', self.table)
        subContainerLeft.append('2', self.listView)
        subContainerLeft.append('3', self.link)
        subContainerLeft.append('4', self.video)

        horizontalContainer.append('0', subContainerLeft)
        horizontalContainer.append('1', subContainerRight)

        menu = gui.Menu(620, 30)
        m1 = gui.MenuItem(100, 30, 'File')
        m2 = gui.MenuItem(100, 30, 'View')
        m2.set_on_click_listener(self, 'menu_view_clicked')
        m11 = gui.MenuItem(100, 30, 'Save')
        m12 = gui.MenuItem(100, 30, 'Open')
        m12.set_on_click_listener(self, 'menu_open_clicked')
        m111 = gui.MenuItem(100, 30, 'Save')
        m111.set_on_click_listener(self, 'menu_save_clicked')
        m112 = gui.MenuItem(100, 30, 'Save as')
        m112.set_on_click_listener(self, 'menu_saveas_clicked')
        m3 = gui.MenuItem(100,30,'Dialog')
        m3.set_on_click_listener(self, 'menu_dialog_clicked')

        menu.append('1',m1)
        menu.append('2',m2)
        menu.append('3',m3)
        m1.append('11',m11)
        m1.append('12',m12)
        m11.append('111',m111)
        m11.append('112',m112)

        menubar = gui.MenuBar(620, 30)
        menubar.append('1', menu)

        verticalContainer.append('0',menubar)
        verticalContainer.append('1',horizontalContainer)

        # kick of regular display of counter
        self.display_counter()
        
        # returning the root widget
        return verticalContainer

    def display_counter(self):
        self.counter.set_text('Running Time: ' + str(self.count))
        self.count+=1
        Timer(1,self.display_counter).start()         
        
    def menu_dialog_clicked(self):
        self.dialog=gui.GenericDialog(400,400,'Dialog Box','Click Ok to transfer content to main page')

        self.dtextinput= gui.TextInput(200, 30)
        self.dtextinput.set_value('Initial Text')
        self.dialog.add_field_with_label('dtextinput','Text Input',self.dtextinput)

        self.dcheck = gui.CheckBox(200, 30, False)
        self.dialog.add_field_with_label('dcheck','Label Checkbox',self.dcheck)        
        values=( 'Danny Young','Christine Holand','Lars Gordon','Roberto Robitaille')
        self.dlistView = gui.ListView(200, 120)
        key=0
        for value in values:
            obj = gui.ListItem(170, 20,value)
            self.dlistView.append(str(key), obj)
            key+=1
        self.dialog.add_field_with_label('dlistView','Listview',self.dlistView)

        self.ddropdown = gui.DropDown(200, 20)
        c0 = gui.DropDownItem(200, 20, 'DropDownItem 0')
        c1 = gui.DropDownItem(200, 20, 'DropDownItem 1')
        self.ddropdown.append('0', c0)
        self.ddropdown.append('1', c1)
        self.ddropdown.set_value('Value1')
        self.dialog.add_field_with_label('ddropdown','Dropdown',self.ddropdown)

        self.dspinbox= gui.SpinBox(200, 20,min=0, max=5000)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dspinbox','Spinbox',self.dspinbox)

        self.dslider= gui.Slider(200, 20, 10, 0, 100, 5)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dslider','Slider',self.dslider)

        self.dcolor= gui.ColorPicker(200, 20)
        self.dcolor.set_value('#ffff00')
        self.dialog.add_field_with_label('dcolor','Colour Picker',self.dcolor)

        self.ddate = gui.Date(200, 20,)
        self.ddate.set_value( '2000-01-01')
        self.dialog.add_field_with_label('ddate','Date',self.ddate)

        self.dialog.set_on_confirm_dialog_listener(self,'dialog_confirm')
        self.dialog.show(self)

    def dialog_confirm(self):
        result=self.dialog.get_field('dtextinput').get_value()
        self.txt.set_value(result)

        result=self.dialog.get_field('dcheck').get_value()
        self.check.set_value(result)
        
        result=self.dialog.get_field('ddropdown').get_value()
        self.dropDown.set_value(result)

        result=self.dialog.get_field('dspinbox').get_value()
        self.spin.set_value(result)

        result=self.dialog.get_field('dslider').get_value()
        self.slider.set_value(result)

        result=self.dialog.get_field('dcolor').get_value()
        self.colorPicker.set_value(result)

        result=self.dialog.get_field('ddate').get_value()
        self.date.set_value(result)

        result=self.dialog.get_field('dlistView').get_key()
        self.listView.select_by_key(result)

    # listener function
    def on_img_clicked(self):
        self.lbl.set_text('Image clicked!')

    def on_button_pressed(self):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')

    def on_text_area_change(self, newValue):
        self.lbl.set_text('Text Area value changed!')

    def on_spin_change(self, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def on_check_change(self, newValue):
        self.lbl.set_text('CheckBox changed, new value: ' + str(newValue))

    def open_input_dialog(self):
        self.inputDialog = gui.InputDialog(500, 160, 'Input Dialog', 'Your name?',
        initial_value='type here')
        self.inputDialog.set_on_confirm_value_listener(
            self, 'on_input_dialog_confirm')

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, value):
        self.lbl.set_text('Hello ' + value)
        
    def open_fileselection_dialog(self):
        self.fileselectionDialog = gui.FileSelectionDialog( 600, 310, 
            'File Selection Dialog', 'Select files and folders',False,'.')
        self.fileselectionDialog.set_on_confirm_value_listener(
            self, 'on_fileselection_dialog_confirm')

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def on_fileselection_dialog_confirm(self, filelist):
        #a list() of filenames and folders is returned
        self.lbl.set_text('Selected files:' + str(filelist))
        for f in filelist:
            self.subContainerRight.append('5__', gui.FileDownloader(200, 30, "download selected", f))

    def list_view_on_selected(self,selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        self.lbl.set_text('List selection: ' + self.listView.children[selected_item_key].get_text())

    def drop_down_changed(self, value):
        self.lbl.set_text('New Combo value: ' + value)

    def slider_changed(self, value):
        self.lbl.set_text('New slider value: ' + str(value))

    def color_picker_changed(self, value):
        self.lbl.set_text('New color value: ' + value)

    def date_changed(self, value):
        self.lbl.set_text('New date value: ' + value)

    def menu_save_clicked(self):
        self.lbl.set_text('Menu clicked: Save')

    def menu_saveas_clicked(self):
        self.lbl.set_text('Menu clicked: Save As')

    def menu_open_clicked(self):
        self.lbl.set_text('Menu clicked: Open')

    def menu_view_clicked(self):
        self.lbl.set_text('Menu clicked: View')
        
    def fileupload_on_success(self, filename):
        self.lbl.set_text('File upload success: ' + filename)

    def fileupload_on_failed(self, filename):
        self.lbl.set_text('File upload failed: ' + filename)
        
# setting up remi debug level 
#       2=all debug messages   1=error messages   0=no messages
# import remi.server
# remi.server.DEBUG_MODE = 2

# starts the webserver
# optional parameters   
#       start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)

start(MyApp)
