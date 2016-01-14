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
import html_helper

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
        

class EditorAttributes(gui.Widget):
    """ Contains EditorAttributeInput each one of which notify a new value with an event
    """
    def __init__(self, w, h):
        super(EditorAttributes, self).__init__(w,h,gui.Widget.LAYOUT_VERTICAL,3)
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'
        self.style['overflow-y'] = 'scroll'
        #load attributes
        #dictionary {tagname:{attributename:{type:'',description:''}}}
        self.attributesDict = html_helper.getTagAttributesDictionary()
        for tagname in self.attributesDict.keys():
            for attributeName in self.attributesDict[tagname].keys():
                attributeEditor = EditorAttributeInput(w, 30, tagname, attributeName, self.attributesDict[tagname][attributeName])
                attributeEditor.set_on_attribute_change_listener(self,"onattribute_changed")
                self.append(attributeEditor)
    
    #this function is called by an EditorAttributeInput change event and propagates to the listeners 
    #adding as first parameter the tag to which it refers
    def onattribute_changed(self, attributeName, newValue):
        return self.eventManager.propagate(self.EVENT_ATTRIB_ONCHANGE, [attributeName, newValue])
        
    def set_on_attribute_change_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ATTRIB_ONCHANGE, listener, funcname)
        
    def set_tag(self, tag):
        #tag should be a BeautifulSoup
        self.targetTag = tag
        #filter the attributes checking if them applies to tag type
        #update the values of the editors checking if there is an actual value
        for child in self.children.values():
            if type(child) == EditorAttributeInput:
                child.hide_if_not_applies(tag.name)


#widget that allows to edit a specific html attribute
#   it has a descriptive label, an edit widget (TextInput, SpinBox) based on the 'type' and a title 
class EditorAttributeInput(gui.Widget):
    def __init__(self, w, h, tagname, attributeName, attributeDict, defaultValue=''):
        super(EditorAttributeInput, self).__init__(w,h,gui.Widget.LAYOUT_HORIZONTAL,3)
        self.tagname = tagname
        self.attributeName = attributeName
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'
        label = gui.Label(w/2-12, h-6, attributeName)
        self.append(label)
        self.inputWidget = None
        if len(attributeDict['type']) == 1:
            if attributeDict['type'][0] in ('bool','int'):
                if attributeDict['type'][0] == 'bool':
                    self.inputWidget = gui.CheckBox(w/2-12, h-6, defaultValue=='checked')
                if attributeDict['type'][0] == 'int':
                    self.inputWidget = gui.SpinBox(w/2-12, h-6, -65535, 65535, defaultValue)
            else: #default editor is string
                self.inputWidget = gui.TextInput(w/2-12, h-6)
        else:
            self.inputWidget = gui.DropDown(w/2-12, h-6)
            for typ in attributeDict['type']:
                item = gui.DropDownItem(-1, -1, typ)
                self.inputWidget.append(item)
        self.inputWidget.attributes['title'] = attributeDict['description']
        label.attributes['title'] = attributeDict['description']
        self.inputWidget.set_on_change_listener(self,"on_attribute_changed")
        self.append(self.inputWidget)
    
    def hide_if_not_applies(self, tagname):
        print("selected tag name: %s == %s"%(tagname,self.tagname))
        if tagname == self.tagname or self.tagname=='all':
            self.style['display'] = 'block'
        else:
            self.style['display'] = 'none'
    
    def set_value(self, value):
        self.inputWidget.set_value(value)
    
    def on_attribute_changed(self, value):
        return self.eventManager.propagate(self.EVENT_ATTRIB_ONCHANGE, [self.attributeName, value])
        
    def set_on_attribute_change_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ATTRIB_ONCHANGE, listener, funcname)