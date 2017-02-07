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
from remi import App
from threading import Timer
from cli import start_app


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        verticalContainer = gui.Widget(width=540, margin='0px auto') #the margin 0px auto centers the main container
        verticalContainer.style['display'] = 'block'
        verticalContainer.style['overflow'] = 'hidden'

        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0px')
        horizontalContainer.style['display'] = 'block'
        horizontalContainer.style['overflow'] = 'auto'

        subContainerLeft = gui.Widget(width=320)
        subContainerLeft.style['display'] = 'block'
        subContainerLeft.style['overflow'] = 'auto'
        subContainerLeft.style['text-align'] = 'center'
        self.img = gui.Image('/res/logo.png', width=100, height=100, margin='10px')
        self.img.set_on_click_listener(self.on_img_clicked)

        self.table = gui.Table.new_from_list([('ID', 'First Name', 'Last Name'),
                                   ('101', 'Danny', 'Young'),
                                   ('102', 'Christine', 'Holand'),
                                   ('103', 'Lars', 'Gordon'),
                                   ('104', 'Roberto', 'Robitaille'),
                                   ('105', 'Maria', 'Papadopoulos')], width=300, height=200, margin='10px')

        # the arguments are	width - height - layoutOrientationOrizontal
        subContainerRight = gui.Widget()
        subContainerRight.style['width'] = '220px'
        subContainerRight.style['display'] = 'block'
        subContainerRight.style['overflow'] = 'auto'
        subContainerRight.style['text-align'] = 'center'
        self.count = 0
        self.counter = gui.Label('', width=200, height=30, margin='10px')

        self.lbl = gui.Label('This is a LABEL!', width=200, height=30, margin='10px', id="main-output-label")

        self.bt = gui.Button('Press me!', width=200, height=30, margin='10px')
        # setting the listener for the onclick event of the button
        self.bt.set_on_click_listener(self.on_button_pressed)

        self.txt = gui.TextInput(width=200, height=30, margin='10px', id="text-area-input")
        self.txt.set_text('This is a TEXTAREA')
        self.txt.set_on_change_listener(self.on_text_area_change)

        self.spin = gui.SpinBox(100, width=200, height=30, margin='10px')
        self.spin.set_on_change_listener(self.on_spin_change)

        self.check = gui.CheckBoxLabel('Label checkbox', True, width=200, height=30, margin='10px')
        self.check.set_on_change_listener(self.on_check_change)

        self.btInputDiag = gui.Button('Open InputDialog', width=200, height=30, margin='10px')
        self.btInputDiag.set_on_click_listener(self.open_input_dialog)

        self.btFileDiag = gui.Button('File Selection Dialog', width=200, height=30, margin='10px')
        self.btFileDiag.set_on_click_listener(self.open_fileselection_dialog)

        self.btUploadFile = gui.FileUploader('./', width=200, height=30, margin='10px')
        self.btUploadFile.set_on_success_listener(self.fileupload_on_success)
        self.btUploadFile.set_on_failed_listener(self.fileupload_on_failed)

        items = ('Danny Young','Christine Holand','Lars Gordon','Roberto Robitaille')
        self.listView = gui.ListView.new_from_list(items, width=300, height=120, margin='10px')
        self.listView.set_on_selection_listener(self.list_view_on_selected)

        self.link = gui.Link("http://localhost:8081", "A link to here", width=200, height=30, margin='10px')

        self.dropDown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1'),
                                                   width=200, height=20, margin='10px')
        self.dropDown.set_on_change_listener(self.drop_down_changed)
        self.dropDown.select_by_value('DropDownItem 0')

        self.slider = gui.Slider(10, 0, 100, 5, width=200, height=20, margin='10px')
        self.slider.set_on_change_listener(self.slider_changed)

        self.colorPicker = gui.ColorPicker('#ffbb00', width=200, height=20, margin='10px')
        self.colorPicker.set_on_change_listener(self.color_picker_changed)

        self.date = gui.Date('2015-04-13', width=200, height=20, margin='10px')
        self.date.set_on_change_listener(self.date_changed)

        self.video = gui.VideoPlayer('http://www.w3schools.com/tags/movie.mp4',
                                     'http://www.oneparallel.com/wp-content/uploads/2011/01/placeholder.jpg',
                                     width=300, height=270, margin='10px')

        self.tree = gui.TreeView(width='100%', height=300)
        ti1 = gui.TreeItem("Item1")
        ti2 = gui.TreeItem("Item2")
        ti3 = gui.TreeItem("Item3")
        subti1 = gui.TreeItem("Sub Item1")
        subti2 = gui.TreeItem("Sub Item2")
        subti3 = gui.TreeItem("Sub Item3")
        subti4 = gui.TreeItem("Sub Item4")
        subsubti1 = gui.TreeItem("Sub Sub Item1")
        subsubti2 = gui.TreeItem("Sub Sub Item2")
        subsubti3 = gui.TreeItem("Sub Sub Item3")
        self.tree.append(ti1)
        self.tree.append(ti2)
        self.tree.append(ti3)
        ti2.append(subti1)
        ti2.append(subti2)
        ti2.append(subti3)
        ti2.append(subti4)
        subti4.append(subsubti1)
        subti4.append(subsubti2)
        subti4.append(subsubti3)

        # appending a widget to another, the first argument is a string key
        subContainerRight.append(self.counter)
        subContainerRight.append(self.lbl)
        subContainerRight.append(self.bt)
        subContainerRight.append(self.txt)
        subContainerRight.append(self.spin)
        subContainerRight.append(self.check)
        subContainerRight.append(self.btInputDiag)
        subContainerRight.append(self.btFileDiag)
        # use a defined key as we replace this widget later
        fdownloader = gui.FileDownloader('download test', '../remi/res/logo.png', width=200, height=30, margin='10px')
        subContainerRight.append(fdownloader, key='file_downloader')
        subContainerRight.append(self.btUploadFile)
        subContainerRight.append(self.dropDown)
        subContainerRight.append(self.slider)
        subContainerRight.append(self.colorPicker)
        subContainerRight.append(self.date)
        subContainerRight.append(self.tree)
        self.subContainerRight = subContainerRight

        subContainerLeft.append(self.img)
        subContainerLeft.append(self.table)
        subContainerLeft.append(self.listView)
        subContainerLeft.append(self.link)
        subContainerLeft.append(self.video)

        horizontalContainer.append(subContainerLeft)
        horizontalContainer.append(subContainerRight)

        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('File', width=100, height=30, id='file-menu-item')
        m2 = gui.MenuItem('View', width=100, height=30)
        m2.set_on_click_listener(self.menu_view_clicked)
        m11 = gui.MenuItem('Save', width=100, height=30, id='file-save-menu-item')
        m12 = gui.MenuItem('Open', width=100, height=30)
        m12.set_on_click_listener(self.menu_open_clicked)
        m111 = gui.MenuItem('Save', width=100, height=30, id='file-save-save-menu-item')
        m111.set_on_click_listener(self.menu_save_clicked)
        m112 = gui.MenuItem('Save as', width=100, height=30)
        m112.set_on_click_listener(self.menu_saveas_clicked)
        m3 = gui.MenuItem('Dialog', width=100, height=30)
        m3.set_on_click_listener(self.menu_dialog_clicked)

        menu.append(m1)
        menu.append(m2)
        menu.append(m3)
        m1.append(m11)
        m1.append(m12)
        m11.append(m111)
        m11.append(m112)

        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        verticalContainer.append(menubar)
        verticalContainer.append(horizontalContainer)

        # kick of regular display of counter
        self.display_counter()

        # returning the root widget
        return verticalContainer

    def display_counter(self):
        self.counter.set_text('Running Time: ' + str(self.count))
        self.count += 1
        Timer(1, self.display_counter).start()

    def menu_dialog_clicked(self, widget):
        self.dialog = gui.GenericDialog(title='Dialog Box', message='Click Ok to transfer content to main page', width='500px')
        self.dtextinput = gui.TextInput(width=200, height=30)
        self.dtextinput.set_value('Initial Text')
        self.dialog.add_field_with_label('dtextinput', 'Text Input', self.dtextinput)

        self.dcheck = gui.CheckBox(False, width=200, height=30)
        self.dialog.add_field_with_label('dcheck', 'Label Checkbox', self.dcheck)
        values = ('Danny Young', 'Christine Holand', 'Lars Gordon', 'Roberto Robitaille')
        self.dlistView = gui.ListView.new_from_list(values, width=200, height=120)
        self.dialog.add_field_with_label('dlistView', 'Listview', self.dlistView)

        self.ddropdown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1'),
                                                    width=200, height=20)
        self.dialog.add_field_with_label('ddropdown', 'Dropdown', self.ddropdown)

        self.dspinbox = gui.SpinBox(min=0, max=5000, width=200, height=20)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dspinbox', 'Spinbox', self.dspinbox)

        self.dslider = gui.Slider(10, 0, 100, 5, width=200, height=20)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dslider', 'Slider', self.dslider)

        self.dcolor = gui.ColorPicker(width=200, height=20)
        self.dcolor.set_value('#ffff00')
        self.dialog.add_field_with_label('dcolor', 'Colour Picker', self.dcolor)

        self.ddate = gui.Date(width=200, height=20)
        self.ddate.set_value('2000-01-01')
        self.dialog.add_field_with_label('ddate', 'Date', self.ddate)

        self.dialog.set_on_confirm_dialog_listener(self.dialog_confirm)
        self.dialog.show(self)

    def dialog_confirm(self, widget):
        result = self.dialog.get_field('dtextinput').get_value()
        self.txt.set_value(result)

        result = self.dialog.get_field('dcheck').get_value()
        self.check.set_value(result)

        result = self.dialog.get_field('ddropdown').get_value()
        self.dropDown.select_by_value(result)

        result = self.dialog.get_field('dspinbox').get_value()
        self.spin.set_value(result)

        result = self.dialog.get_field('dslider').get_value()
        self.slider.set_value(result)

        result = self.dialog.get_field('dcolor').get_value()
        self.colorPicker.set_value(result)

        result = self.dialog.get_field('ddate').get_value()
        self.date.set_value(result)

        result = self.dialog.get_field('dlistView').get_value()
        self.listView.select_by_value(result)

    # listener function
    def on_img_clicked(self, widget):
        self.lbl.set_text('Image clicked!')

    def on_button_pressed(self, widget):
        self.lbl.set_text('Button pressed!')
        self.bt.set_text('Hi!')

    def on_text_area_change(self, widget, newValue):
        self.lbl.set_text('Text Area value changed!')

    def on_spin_change(self, widget, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def on_check_change(self, widget, newValue):
        self.lbl.set_text('CheckBox changed, new value: ' + str(newValue))

    def open_input_dialog(self, widget):
        self.inputDialog = gui.InputDialog('Input Dialog', 'Your name?',
                                           initial_value='type here',
                                           width=500, height=160)
        self.inputDialog.set_on_confirm_value_listener(
            self.on_input_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, widget, value):
        self.lbl.set_text('Hello ' + value)

    def open_fileselection_dialog(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders', False,
                                                           '.')
        self.fileselectionDialog.set_on_confirm_value_listener(
            self.on_fileselection_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def on_fileselection_dialog_confirm(self, widget, filelist):
        # a list() of filenames and folders is returned
        self.lbl.set_text('Selected files: %s' % ','.join(filelist))
        if len(filelist):
            f = filelist[0]
            # replace the last download link
            fdownloader = gui.FileDownloader("download selected", f, width=200, height=30)
            self.subContainerRight.append(fdownloader, key='file_downloader')

    def list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        self.lbl.set_text('List selection: ' + self.listView.children[selected_item_key].get_text())

    def drop_down_changed(self, widget, value):
        self.lbl.set_text('New Combo value: ' + value)

    def slider_changed(self, widget, value):
        self.lbl.set_text('New slider value: ' + str(value))

    def color_picker_changed(self, widget, value):
        self.lbl.set_text('New color value: ' + value)

    def date_changed(self, widget, value):
        self.lbl.set_text('New date value: ' + value)

    def menu_save_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save')

    def menu_saveas_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save As')

    def menu_open_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Open')

    def menu_view_clicked(self, widget):
        self.lbl.set_text('Menu clicked: View')

    def fileupload_on_success(self, widget, filename):
        self.lbl.set_text('File upload success: ' + filename)

    def fileupload_on_failed(self, widget, filename):
        self.lbl.set_text('File upload failed: ' + filename)


if __name__ == "__main__":
    start_app(MyApp)