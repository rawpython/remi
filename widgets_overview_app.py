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


class App(BaseApp):

    def __init__(self, *args):
        super(App, self).__init__(*args)

    def main(self):
        mainContainer = gui.widget(600, 530, True, 10)

        subContainerLeft = gui.widget(300, 370, False, 10)
        self.img = gui.imageWidget(100, 100, 'logo.png')

        self.table = gui.tableWidget(300, 200)
        row = gui.rowTable()
        item = gui.titleTable()
        item.append(str(id(item)), 'ID')
        row.append(str(id(item)), item)
        item = gui.titleTable()
        item.append(str(id(item)), 'First Name')
        row.append(str(id(item)), item)
        item = gui.titleTable()
        item.append(str(id(item)), 'Last Name')
        row.append(str(id(item)), item)
        self.table.append(str(id(row)), row)
        self.addTableRow(self.table, '101', 'Danny', 'Young')
        self.addTableRow(self.table, '102', 'Christine', 'Holand')
        self.addTableRow(self.table, '103', 'Lars', 'Gordon')
        self.addTableRow(self.table, '104', 'Roberto', 'Robitaille')
        self.addTableRow(self.table, '105', 'Maria', 'Papadopoulos')

        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.widget(240, 390, False, 10)

        self.lbl = gui.labelWidget(200, 30, 'This is a LABEL!')

        self.bt = gui.buttonWidget(200, 30, 'Press me!')
        # setting the listener for the onclick event of the button
        self.bt.setOnClickListener(self, 'onButtonPressed')

        self.txt = gui.textareaWidget(200, 30)
        self.txt.text('This is a TEXTAREA')
        self.txt.setOnChangeListener(self, 'onTextAreaChange')

        self.spin = gui.spinboxWidget(200, 30)
        self.spin.setOnChangeListener(self, 'onSpinChange')

        self.btInputDiag = gui.buttonWidget(200, 30, 'Open InputDialog')
        self.btInputDiag.setOnClickListener(self, 'openInputDialog')

        self.listWidget = gui.listWidget(300, 120)
        li0 = gui.listItem(279, 20, 'Danny Young')
        li0.setOnClickListener(self, 'listItem0_selected')
        li1 = gui.listItem(279, 20, 'Christine Holand')
        li1.setOnClickListener(self, 'listItem1_selected')
        li2 = gui.listItem(279, 20, 'Lars Gordon')
        li2.setOnClickListener(self, 'listItem2_selected')
        li3 = gui.listItem(279, 20, 'Roberto Robitaille')
        li3.setOnClickListener(self, 'listItem3_selected')
        self.listWidget.append('0', li0)
        self.listWidget.append('1', li1)
        self.listWidget.append('2', li2)
        self.listWidget.append('3', li3)

        self.combo = gui.comboWidget(200, 20)
        c0 = gui.comboItem(200, 20, 'Combo 0')
        c1 = gui.comboItem(200, 20, 'Combo 1')
        self.combo.append('0', c0)
        self.combo.append('1', c1)
        self.combo.setOnChangeListener(self, 'comboChanged')

        self.slider = gui.sliderWidget(200, 20, 10, 0, 100, 5)
        self.slider.setOnChangeListener(self, 'sliderChanged')

        self.colorPicker = gui.colorPickerWidget(200, 20, '#ffbb00')
        self.colorPicker.setOnChangeListener(self, 'colorPickerChanged')

        self.date = gui.dateWidget(200, 20, '2015-04-13')
        self.date.setOnChangeListener(self, 'dateChanged')

        # appending a widget to another, the first argument is a string key
        subContainerRight.append('1', self.lbl)
        subContainerRight.append('2', self.bt)
        subContainerRight.append('3', self.txt)
        subContainerRight.append('4', self.spin)
        subContainerRight.append('5', self.btInputDiag)
        subContainerRight.append('6', self.combo)
        subContainerRight.append('7', self.slider)
        subContainerRight.append('8', self.colorPicker)
        subContainerRight.append('9', self.date)

        subContainerLeft.append('0', self.img)
        subContainerLeft.append('1', self.table)
        subContainerLeft.append('2', self.listWidget)

        mainContainer.append('0', subContainerLeft)
        mainContainer.append('1', subContainerRight)
        # returning the root widget
        return mainContainer

    def addTableRow(self, table, field1, field2, field3):
        row = gui.rowTable()
        item = gui.itemTable()
        item.append(str(id(item)), field1)
        row.append(str(id(item)), item)
        item = gui.itemTable()
        item.append(str(id(item)), field2)
        row.append(str(id(item)), item)
        item = gui.itemTable()
        item.append(str(id(item)), field3)
        row.append(str(id(item)), item)
        table.append(str(id(row)), row)

    # listener function
    def onButtonPressed(self):
        self.lbl.setText('Button pressed!')
        self.bt.text('Hi!')

    def onTextAreaChange(self, newValue):
        self.lbl.setText('Text Area value changed!')

    def onSpinChange(self, newValue):
        self.lbl.setText('SpinBox changed, new value: ' + str(newValue))

    def openInputDialog(self):
        self.inputDialog = gui.inputDialog('Input Dialog', 'Your name?')
        self.inputDialog.setOnConfirmValueListener(
            self, 'onInputDialogConfirm')

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def onInputDialogConfirm(self, value):
        self.lbl.setText('Hello ' + value)

    def listItem0_selected(self):
        self.lbl.setText('Danny selected')

    def listItem1_selected(self):
        self.lbl.setText('Christine selected')

    def listItem2_selected(self):
        self.lbl.setText('Lars selected')

    def listItem3_selected(self):
        self.lbl.setText('Roberto selected')

    def comboChanged(self, value):
        self.lbl.setText('New Combo value: ' + value)

    def sliderChanged(self, value):
        self.lbl.setText('New slider value: ' + str(value))

    def colorPickerChanged(self, value):
        self.lbl.setText('New color value: ' + value)

    def dateChanged(self, value):
        self.lbl.setText('New date value: ' + value)

# starts the webserver
start(App)
