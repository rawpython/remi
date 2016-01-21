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


class ProjectConfigurationDialog(gui.GenericDialog):
    def __init__(self, title='', message=''):
        super(ProjectConfigurationDialog, self).__init__('Project Configuration', 'Here are the configuration options of the project.')
        #standard configuration
        self.configuration['Project Name'] = 'untitled'
        self.configuration['IP address'] = '0.0.0.0'
        self.configuration['Listen port'] = 8081
        self.configuration['Use single App instance for multiple users'] = True
        self.configuration['Enable file caching'] = True
        self.configuration['Start browser automatically'] = True
        self.configuration['Additional resource path'] = "./res/"

        self.add_field_with_label( 'Project Name', 'Project Name', gui.TextInput() )
        self.add_field_with_label( 'IP address', 'IP address', gui.TextInput() )
        self.add_field_with_label( 'Listen port', 'Listen port', gui.SpinBox(0, 65536, 8081) )
        self.add_field_with_label( 'Use single App instance for multiple users', 'Use single App instance for multiple users', gui.CheckBox(True) )
        self.add_field_with_label( 'Enable file caching', 'Enable file caching', gui.CheckBox(True) )
        self.add_field_with_label( 'Start browser automatically', 'Start browser automatically', gui.CheckBox(True) )
        self.add_field_with_label( 'Additional resource path', 'Additional resource path', gui.TextInput() )
        self.from_dict_to_fields(self.configuration)
    
    def from_dict_to_fields(self, dictionary):
        for key in self.inputs.keys():
            if key in dictionary.keys():
                self.get_field(key).set_value(dictionary[key])
        
    def from_fields_to_dict(self):
        for key in self.inputs.keys():
            self.configuration[key] = self.get_field(key).get_value()
            

class EditorFileSelectionDialog(gui.FileSelectionDialog):
    def __init__(self, title='File dialog', message='Select files and folders', 
                multiple_selection=True, selection_folder='.', allow_file_selection=True, 
                allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSelectionDialog, self).__init__( title,
                 message, multiple_selection, selection_folder, 
                 allow_file_selection, allow_folder_selection)
        
        self.baseAppInstance = baseAppInstance
        
    def show(self):
        super(EditorFileSelectionDialog, self).show(self.baseAppInstance)


class EditorFileSaveDialog(gui.FileSelectionDialog):
    def __init__(self, title='File dialog', message='Select files and folders', 
                multiple_selection=True, selection_folder='.', 
                 allow_file_selection=True, allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSaveDialog, self).__init__( title, message, multiple_selection, selection_folder, 
                 allow_file_selection, allow_folder_selection)
        
        self.baseAppInstance = baseAppInstance
        
    def show(self):
        super(EditorFileSaveDialog, self).show(self.baseAppInstance)
        
    def add_fileinput_field(self, defaultname='untitled'):
        self.txtFilename = gui.TextInput()
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

        
class WidgetHelper(gui.ListItem):
    """ Allocates the Widget to which it refers, 
        interfacing to the user in order to obtain the necessary attribute values
        obtains the constructor parameters, asks for them in a dialog
        puts the values in an attribute called constructor
    """

    def __init__(self, widgetClass):
        self.widgetClass = widgetClass
        super(WidgetHelper, self).__init__(self.widgetClass.__name__)
            
    def prompt_new_widget(self, appInstance):
        self.appInstance = appInstance
        self.constructor_parameters_list = self.widgetClass.__init__.__code__.co_varnames[1:] #[1:] removes the self
        param_annotation_dict = ''#self.widgetClass.__init__.__annotations__
        self.dialog = gui.GenericDialog(title=self.widgetClass.__name__, message='Fill the following parameters list')
        self.dialog.add_field_with_label('name', 'Variable name', gui.TextInput())
        #for param in self.constructor_parameters_list:
        for index in range(0,len(self.constructor_parameters_list)):
            param = self.constructor_parameters_list[index]
            _typ = self.widgetClass.__init__._constructor_types[index]
            note = ' (%s)'%_typ.__name__
            editWidget = None
            if _typ==int:
                editWidget = gui.SpinBox('0',-65536,65535)
            elif _typ==bool:
                editWidget = gui.CheckBox()
            elif _typ==str:
                editWidget = gui.TextInput()
            else:
                editWidget = gui.TextInput()
            self.dialog.add_field_with_label(param, param + note, editWidget)
        self.dialog.add_field_with_label("editor_newclass", "Overload base class", gui.CheckBox())
        self.dialog.set_on_confirm_dialog_listener(self, "on_dialog_confirm")
        self.dialog.show(self.appInstance)
        
    def on_dialog_confirm(self):
        """ Here the widget is allocated
        """
        param_annotation_dict = ''#self.widgetClass.__init__.__annotations__
        param_values = []
        param_for_constructor = []
        for index in range(0,len(self.constructor_parameters_list)):
            param = self.constructor_parameters_list[index]
            _typ = self.widgetClass.__init__._constructor_types[index]
            if _typ==int:
                param_for_constructor.append(self.dialog.get_field(param).get_value())
            elif _typ==bool:
                param_for_constructor.append(self.dialog.get_field(param).get_value())
            elif _typ==str:
                param_for_constructor.append("""\'%s\'"""%self.dialog.get_field(param).get_value())
            else:
                param_for_constructor.append("""%s"""%self.dialog.get_field(param).get_value())
            param_values.append(self.dialog.get_field(param).get_value())
        print(self.constructor_parameters_list)
        print(param_values)
        #constructor = '%s(%s)'%(self.widgetClass.__name__, ','.join(map(lambda v: str(v), param_values)))
        constructor = '(%s)'%(','.join(map(lambda v: str(v), param_for_constructor)))
        #here we create and decorate the widget
        widget = self.widgetClass(*param_values)
        widget.attributes['editor_constructor'] = constructor
        widget.attributes['editor_varname'] = self.dialog.get_field('name').get_value()
        widget.attributes['editor_tag_type'] = 'widget'
        widget.attributes['editor_newclass'] = 'True' if self.dialog.get_field("editor_newclass").get_value() else 'False'
        #"this.style.cursor='default';this.style['left']=(event.screenX) + 'px'; this.style['top']=(event.screenY) + 'px'; event.preventDefault();return true;"  
        widget.style['position'] = 'absolute'
        widget.style['display'] = 'block'
        widget.set_size(100,100)
        self.appInstance.add_widget_to_editor(widget)


class WidgetCollection(gui.Widget):
    def __init__(self, appInstance):
        self.appInstance = appInstance
        super(WidgetCollection, self).__init__()
        
        self.lblTitle = gui.Label("Widgets Toolbox")
        self.listWidgets = gui.ListView()
        self.listWidgets.style['width'] = '100%'
        
        self.append(self.lblTitle)
        self.append(self.listWidgets)
        
        #load all widgets
        self.add_widget_to_collection(gui.Widget)
        self.add_widget_to_collection(gui.Button)
        self.add_widget_to_collection(gui.TextInput)
        self.add_widget_to_collection(gui.Label)
        self.add_widget_to_collection(gui.ListView)
        self.add_widget_to_collection(gui.ListItem)
        self.add_widget_to_collection(gui.DropDown)
        self.add_widget_to_collection(gui.DropDownItem)
        self.add_widget_to_collection(gui.Image)
        self.add_widget_to_collection(gui.CheckBoxLabel)
        self.add_widget_to_collection(gui.CheckBox)
        self.add_widget_to_collection(gui.SpinBox)
        self.add_widget_to_collection(gui.Slider)
        
    def add_widget_to_collection(self, widgetClass):
        #create an helper that will be created on click
        #the helper have to search for function that have 'return' annotation 'event_listener_setter'
        helper = WidgetHelper(widgetClass)
        helper.style['width'] = '100%'
        self.listWidgets.append( helper )
        helper.set_on_click_listener(self.appInstance, "widget_helper_clicked")


class EditorAttributes(gui.Widget):
    """ Contains EditorAttributeInput each one of which notify a new value with an event
    """
    def __init__(self):
        super(EditorAttributes, self).__init__()
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'
        self.style['overflow-y'] = 'scroll'
        #load attributes
        #dictionary {tagname:{attributename:{type:'',description:''}}}
        self.attributesDict = html_helper.getTagAttributesDictionary()
        for tagname in self.attributesDict.keys():
            for attributeName in self.attributesDict[tagname].keys():
                attributeEditor = EditorAttributeInput(tagname, attributeName, self.attributesDict[tagname][attributeName])
                attributeEditor.set_on_attribute_change_listener(self,"onattribute_changed")
                self.append(attributeEditor)
    
    #this function is called by an EditorAttributeInput change event and propagates to the listeners 
    #adding as first parameter the tag to which it refers
    def onattribute_changed(self, attributeName, newValue):
        return self.eventManager.propagate(self.EVENT_ATTRIB_ONCHANGE, [attributeName, newValue])
        
    def set_on_attribute_change_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ATTRIB_ONCHANGE, listener, funcname)
        
    def set_widget(self, widget):
        self.attributes['selected_widget_id'] = str(id(widget))
        self.targetWidget = widget
        #filter the attributes checking if them applies to tag type
        #update the values of the editors checking if there is an actual value
        for child in self.children.values():
            if type(child) == EditorAttributeInput:
                child.hide_if_not_applies(self.targetWidget.type)


#widget that allows to edit a specific html attribute
#   it has a descriptive label, an edit widget (TextInput, SpinBox) based on the 'type' and a title 
class EditorAttributeInput(gui.Widget):
    def __init__(self, tagname, attributeName, attributeDict, defaultValue=''):
        super(EditorAttributeInput, self).__init__()
        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style['display'] = 'block'
        self.style['overflow'] = 'auto'
        self.style['margin'] = '2px'
        self.tagname = tagname
        self.attributeName = attributeName
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'
        
        label = gui.Label(attributeName)
        label.style['height'] = '30px'
        label.style['margin'] = '0px 10px'
        self.append(label)
        self.inputWidget = None
        if len(attributeDict['type']) == 1:
            if attributeDict['type'][0] in ('bool','int'):
                if attributeDict['type'][0] == 'bool':
                    self.inputWidget = gui.CheckBox(defaultValue=='checked')
                if attributeDict['type'][0] == 'int':
                    self.inputWidget = gui.SpinBox(-65535, 65535, defaultValue)
            else: #default editor is string
                self.inputWidget = gui.TextInput()
        else:
            self.inputWidget = gui.DropDown()
            for typ in attributeDict['type']:
                item = gui.DropDownItem(typ)
                self.inputWidget.append(item)
        self.inputWidget.set_size('50%','30px')
        self.inputWidget.attributes['title'] = attributeDict['description']
        label.attributes['title'] = attributeDict['description']
        self.inputWidget.set_on_change_listener(self,"on_attribute_changed")
        self.append(self.inputWidget)
        self.inputWidget.style['float'] = 'right'
    
    def hide_if_not_applies(self, tagname):
        #print("selected tag name: %s == %s"%(tagname,self.tagname))
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