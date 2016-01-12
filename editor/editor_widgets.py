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