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

class EditorFileSelectionDialog(gui.FileSelectionDialog):
    def __init__(self, width = 600, fileFolderNavigatorHeight=210, title='File dialog',
                 message='Select files and folders', multiple_selection=True, selection_folder='.', 
                 allow_file_selection=True, allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSelectionDialog, self).__init__( width, fileFolderNavigatorHeight, title,
                 message, multiple_selection, selection_folder, 
                 allow_file_selection, allow_folder_selection)
        
        self.baseAppInstance = baseAppInstance
        
    def show(self):
        super(EditorFileSelectionDialog, self).show(self.baseAppInstance)


class EditorFileSaveDialog(gui.FileSelectionDialog):
    def __init__(self, width = 600, fileFolderNavigatorHeight=210, title='File dialog',
                 message='Select files and folders', multiple_selection=True, selection_folder='.', 
                 allow_file_selection=True, allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSaveDialog, self).__init__( width, fileFolderNavigatorHeight, title,
                 message, multiple_selection, selection_folder, 
                 allow_file_selection, allow_folder_selection)
        
        self.baseAppInstance = baseAppInstance
        
    def show(self):
        super(EditorFileSaveDialog, self).show(self.baseAppInstance)
        
    def add_fileinput_field(self, defaultname='untitled'):
        self.txtFilename = gui.TextInput(450, 30)
        self.txtFilename.set_text(defaultname)
        
        self.add_field_with_label("filename","Filename",self.txtFilename)
        
    def get_fileinput_value(self):
        return self.get_field('filename').get_value()
        
    def confirm_value(self):
        """event called pressing on OK button.
           propagates the string content of the input field
        """
        self.hide()
        params = [self.fileFolderNavigator.pathEditor.get_text()]
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, params)
        
#widget that allows to edit a specific html attribute
#   it has a descriptive label, an edit widget (TextInput, SpinBox) based on the 'type' and a title 
class EditorAttributeInput(gui.Widget):
    def __init__(self, w, h, attributeDict, defaultValue=''):
        super(EditorAttributeInput, self).__init__(w,h,gui.Widget.LAYOUT_HORIZONTAL,3)
        label = gui.Label(w/2-12, h-6, attributename)
        self.append(label)
        self.inputWidget = None
        if len(attributedict.type) == 1:
            if attributedict.type[0] in ('bool','int'):
                if attributedict.type[0] == 'bool':
                    self.inputWidget = gui.CheckBox(w/2-12, h-6, defaultValue=='checked')
                if attributedict.type[0] == 'int':
                    self.inputWidget = gui.SpinBox(w/2-12, h-6, defaultValue=='checked')
            else: #default editor is string
                self.inputWidget = gui.TextInput(w/2-12, h-6)
        else:
            self.inputWidget = gui.DropDown(w/2-12, h-6)
        
        self.inputWidget.set_on_change_listener
        self.append(self.inputWidget)
        