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

    def main(self):
        mainContainer = gui.Widget(600, 530, True, 10)

        subContainerLeft = gui.Widget(300, 370, False, 10)
        self.img = gui.Image(100, 100, 'logo.png')

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
        subContainerRight = gui.Widget(240, 390, False, 10)

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

        self.listView = gui.ListView(300, 120)
        li0 = gui.ListItem(279, 20, 'Danny Young')
        li0.set_on_click_listener(self, 'list_item0_selected')
        li1 = gui.ListItem(279, 20, 'Christine Holand')
        li1.set_on_click_listener(self, 'list_item1_selected')
        li2 = gui.ListItem(279, 20, 'Lars Gordon')
        li2.set_on_click_listener(self, 'list_item2_selected')
        li3 = gui.ListItem(279, 20, 'Roberto Robitaille')
        li3.set_on_click_listener(self, 'list_item3_selected')
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
        subContainerRight.append('6', self.dropDown)
        subContainerRight.append('7', self.slider)
        subContainerRight.append('8', self.colorPicker)
        subContainerRight.append('9', self.date)

        subContainerLeft.append('0', self.img)
        subContainerLeft.append('1', self.table)
        subContainerLeft.append('2', self.listView)

        mainContainer.append('0', subContainerLeft)
        mainContainer.append('1', subContainerRight)
        # returning the root widget
        return mainContainer

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
        self.bt.show(self)

    def on_text_area_change(self, newValue):
        self.lbl.set_text('Text Area value changed!')

    def on_spin_change(self, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def open_input_dialog(self):
        self.inputDialog = gui.InputDialog('Input Dialog', 'Your name?')
        self.inputDialog.set_on_confirm_value_listener(
            self, 'on_input_dialog_confirm')

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, value):
        self.lbl.set_text('Hello ' + value)

    def list_item0_selected(self):
        self.lbl.set_text('Danny selected')

    def list_item1_selected(self):
        self.lbl.set_text('Christine selected')

    def list_item2_selected(self):
        self.lbl.set_text('Lars selected')

    def list_item3_selected(self):
        self.lbl.set_text('Roberto selected')

    def drop_down_changed(self, value):
        self.lbl.set_text('New Combo value: ' + value)

    def slider_changed(self, value):
        self.lbl.set_text('New slider value: ' + str(value))

    def color_picker_changed(self, value):
        self.lbl.set_text('New color value: ' + value)

    def date_changed(self, value):
        self.lbl.set_text('New date value: ' + value)

# starts the webserver
start(MyApp)
