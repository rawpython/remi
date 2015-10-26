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

import gui
from gui import *


class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)
        
    def idle(self):
        """ Usefull function to schedule tasks. 
        Called every configuration.UPDATE_ITERVAL """
        super(MyApp, self).idle()
        
    def main(self):
        verticalContainer = gui.Widget(640, 680, gui.Widget.LAYOUT_VERTICAL, 10)

        horizontalContainer = gui.Widget(620, 620, gui.Widget.LAYOUT_HORIZONTAL, 10)

        subContainerLeft = gui.Widget(340, 530, gui.Widget.LAYOUT_VERTICAL, 10)
        self.img = gui.Image(100, 100, './res/logo.png')

        self.table = gui.Table(300, 200)
        row = gui.TableRow()
        item = gui.TableTitle()
        item.append(str(id(item)), 'ID')
        row.append(str(id(item)), item)
        item = gui.TableTitle()
        item.append(str(id(item)), 'First Name')
        row.append(str(id(item)), item)
        item = gui.TableTitle()
        item.append(str(id(item)), 'Last Name')
        row.append(str(id(item)), item)
        self.table.append(str(id(row)), row)
        self.add_table_row(self.table, '101', 'Danny', 'Young')
        self.add_table_row(self.table, '102', 'Christine', 'Holand')
        self.add_table_row(self.table, '103', 'Lars', 'Gordon')
        self.add_table_row(self.table, '104', 'Roberto', 'Robitaille')
        self.add_table_row(self.table, '105', 'Maria', 'Papadopoulos')

        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Widget(240, 560, gui.Widget.LAYOUT_VERTICAL, 10)

        self.lbl = gui.Label(200, 30, 'This is a LABEL!')

        self.bt = gui.Button(200, 30, 'Press me!')
        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        self.txt = gui.TextInput(200, 30)
        self.txt.set_text('This is a TEXTAREA')
        self.txt.set_on_change_listener(self, 'on_text_area_change')

        self.spin = gui.SpinBox(200, 30)
        self.spin.set_on_change_listener(self, 'on_spin_change')

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

        # appending a widget to another, the first argument is a string key
        subContainerRight.append('1', self.lbl)
        subContainerRight.append('2', self.bt)
        subContainerRight.append('3', self.txt)
        subContainerRight.append('4', self.spin)
        subContainerRight.append('5', self.btInputDiag)
        subContainerRight.append('5_', self.btFileDiag)
        subContainerRight.append('5__', gui.FileDownloader(200, 30, 'download test', './res/logo.png'))
        subContainerRight.append('5___', self.btUploadFile)
        subContainerRight.append('6', self.dropDown)
        subContainerRight.append('7', self.slider)
        subContainerRight.append('8', self.colorPicker)
        subContainerRight.append('9', self.date)
        self.subContainerRight = subContainerRight

        subContainerLeft.append('0', self.img)
        subContainerLeft.append('1', self.table)
        subContainerLeft.append('2', self.listView)

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

        menu.append('1',m1)
        menu.append('2',m2)
        m1.append('11',m11)
        m1.append('12',m12)
        m11.append('111',m111)
        m11.append('112',m112)

        verticalContainer.append('0',menu)
        verticalContainer.append('1',horizontalContainer)

        # returning the root widget
        return verticalContainer

    def add_table_row(self, table, field1, field2, field3):
        row = gui.TableRow()
        item = gui.TableItem()
        item.append(str(id(item)), field1)
        row.append(str(id(item)), item)
        item = gui.TableItem()
        item.append(str(id(item)), field2)
        row.append(str(id(item)), item)
        item = gui.TableItem()
        item.append(str(id(item)), field3)
        row.append(str(id(item)), item)
        table.append(str(id(row)), row)

    # listener function
    def on_button_pressed(self):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')

    def on_text_area_change(self, newValue):
        self.lbl.set_text('Text Area value changed!')

    def on_spin_change(self, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def open_input_dialog(self):
        self.inputDialog = gui.InputDialog(500, 160, 'Input Dialog', 'Your name?')
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
        
# starts the webserver
start(MyApp)
