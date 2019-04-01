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
import inspect
import re


class InstancesTree(gui.TreeView, gui.EventSource):
    def __init__(self, **kwargs):
        super(InstancesTree, self).__init__(**kwargs)
        gui.EventSource.__init__(self)

    def append_instance(self, instance, parent):
        item = gui.TreeItem(instance.attributes['editor_varname'])
        if parent==None:
            parent = self
        item.instance = instance
        item.onclick.do(self.on_tree_item_selected)
        parent.append(item)
        return item

    def item_by_instance(self, node, instance):
        if not hasattr(node, 'attributes'):
            return None
        if node.identifier!=self.identifier:
            if not hasattr(node,'instance'):
                return None

        for item in node.children.values():
            if self.item_by_instance(item, instance) == instance.identifier:
                return [node, item]
        return None

    def remove_instance(self, instance):
        node, item = self.item_by_instance(self, instance)
        node.remove_child(item)

    def select_instance(self, node, instance):
        if not hasattr(node, 'attributes'):
            return
        if node.identifier!=self.identifier:
            if hasattr(node,'instance'):
                if node.instance.identifier == instance.identifier:
                    node.style['background-color'] = 'lightblue'
                else: 
                    node.style['background-color'] = 'white'
                node.attributes['treeopen'] = 'true'
        for item in node.children.values():
            self.select_instance(item, instance)

    @gui.decorate_event
    def on_tree_item_selected(self, emitter):
        self.select_instance(self, emitter.instance)
        return (emitter.instance,)

    def append_instances_from_tree(self, node, parent=None):
        if not hasattr(node, 'attributes'):
            return
        if not 'editor_varname' in node.attributes.keys():
            return
        nodeTreeItem = self.append_instance(node, parent)
        for child in node.children.values():
            self.append_instances_from_tree(child, nodeTreeItem)


class InstancesWidget(gui.VBox):
    def __init__(self, **kwargs):
        super(InstancesWidget, self).__init__(**kwargs)
        self.titleLabel = gui.Label('Instances list', width='100%')
        self.titleLabel.add_class("DialogTitle")
        self.style['align-items'] = 'flex-start'
        self.treeView = InstancesTree()

        self.append([self.titleLabel, self.treeView])

        self.titleLabel.style['order'] = '-1'
        self.titleLabel.style['-webkit-order'] = '-1'
        self.treeView.style['order'] = '0'
        self.treeView.style['-webkit-order'] = '0'

    def update(self, editorProject, selectedNode):
        self.treeView.empty()
        if 'root' in editorProject.children.keys():
            self.treeView.append_instances_from_tree(editorProject.children['root'])
            self.treeView.select_instance(self.treeView, selectedNode)
    
    def select(self, selectedNode):
        self.treeView.select_instance(self.treeView, selectedNode)


class ToolBar(gui.Widget):
    def __init__(self, **kwargs):
        super(ToolBar, self).__init__(**kwargs)
        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style['background-color'] = 'white'

    def add_command(self, imagePath, callback, title):
        icon = gui.Image(imagePath, height='90%', margin='0px 1px')
        icon.style['outline'] = '1px solid lightgray'
        icon.onclick.do(callback)
        icon.attributes['title'] = title
        self.append(icon)


class SignalConnection(gui.Widget):
    def __init__(self, widget, listenersList, eventConnectionFuncName, eventConnectionFunc, **kwargs):
        super(SignalConnection, self).__init__(**kwargs)

        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style.update({'overflow':'visible', 'height':'24px', 'display':'block', 'outline':'1px solid lightgray'})
        self.label = gui.Label(eventConnectionFuncName, width='49%')
        self.label.style.update({'float':'left', 'font-size':'10px', 'overflow':'hidden', 'outline':'1px solid lightgray'})

        self.dropdown = gui.DropDown(width='49%', height='100%')
        self.dropdown.onchange.do(self.on_connection)
        self.append([self.label, self.dropdown])
        self.dropdown.style['float'] = 'right'

        self.eventConnectionFunc = eventConnectionFunc
        self.eventConnectionFuncName = eventConnectionFuncName
        self.refWidget = widget
        self.listenersList = listenersList
        self.dropdown.append(gui.DropDownItem("None"))
        for w in listenersList:
            ddi = gui.DropDownItem(w.attributes['editor_varname'])
            ddi.listenerInstance = w
            self.dropdown.append(ddi)
        if hasattr(self.eventConnectionFunc, 'callback_copy'): #if the callback is not None, and so there is a listener
            connectedListenerName = eventConnectionFunc.callback_copy.__self__.attributes['editor_varname']
            self.dropdown.set_value( connectedListenerName )

    def on_connection(self, widget, dropDownValue):
        if self.dropdown.get_value()=='None':
            self.eventConnectionFunc.do(None)
        else:
            listener = self.dropdown._selected_item.listenerInstance
            listener.attributes['editor_newclass'] = "True"
            print("Event: " + self.eventConnectionFuncName + " signal connection to: " + listener.attributes['editor_varname'] + "   from:" + self.refWidget.attributes['editor_varname'])
            back_callback = getattr(self.refWidget, self.eventConnectionFuncName).callback
            listener.__class__.fakeListenerFunc = fakeListenerFunc
            getattr(self.refWidget, self.eventConnectionFuncName).do(listener.fakeListenerFunc)
            getattr(self.refWidget, self.eventConnectionFuncName).callback_copy = getattr(self.refWidget, self.eventConnectionFuncName).callback
            getattr(self.refWidget, self.eventConnectionFuncName).callback = back_callback


def fakeListenerFunc(self,*args):
    print('event trap')

class SignalConnectionManager(gui.Widget):
    """ This class allows to interconnect event signals """
    def __init__(self, **kwargs):
        super(SignalConnectionManager, self).__init__(**kwargs)
        self.label = gui.Label('Signal connections', width='100%')
        self.label.add_class("DialogTitle")
        self.append(self.label)
        self.container = gui.VBox(width='100%', height='90%')
        self.container.style['justify-content'] = 'flex-start'
        self.container.style['overflow-y'] = 'scroll'
        self.listeners_list = []

    def build_widget_list_from_tree(self, node):
        if not hasattr(node, 'attributes'):
            return
        if not 'editor_varname' in node.attributes.keys():
            return
        self.listeners_list.append(node)
        for child in node.children.values():
            self.build_widget_list_from_tree(child)

    def update(self, widget, widget_tree):
        """ for the selected widget are listed the relative signals
            for each signal there is a dropdown containing all the widgets
            the user will select the widget that have to listen a specific event
        """
        self.listeners_list = []
        self.build_widget_list_from_tree(widget_tree)

        self.label.set_text('Signal connections: ' + widget.attributes['editor_varname'])
        #del self.container
        self.container = gui.VBox(width='100%', height='90%')
        self.container.style['justify-content'] = 'flex-start'
        self.container.style['overflow-y'] = 'scroll'
        self.append(self.container, 'container')
        ##for all the events of this widget
        #isclass instead of ismethod because event methods are replaced with ClassEventConnector
        for (setOnEventListenerFuncname,setOnEventListenerFunc) in inspect.getmembers(widget):
            #if the member is decorated by decorate_set_on_listener and the function is referred to this event
            if hasattr(setOnEventListenerFunc, '_event_info'):
                self.container.append( SignalConnection(widget, 
                    self.listeners_list, 
                    setOnEventListenerFuncname, 
                    setOnEventListenerFunc, 
                    width='100%') )


class ProjectConfigurationDialog(gui.GenericDialog, gui.EventSource):
    KEY_PRJ_NAME = 'config_project_name'
    KEY_ADDRESS = 'config_address'
    KEY_PORT = 'config_port'
    KEY_MULTIPLE_INSTANCE = 'config_multiple_instance'
    KEY_ENABLE_CACHE = 'config_enable_file_cache'
    KEY_START_BROWSER = 'config_start_browser'
    KEY_RESOURCEPATH = 'config_resourcepath'

    def __init__(self, title='', message=''):
        super(ProjectConfigurationDialog, self).__init__('Project Configuration', 'Here are the configuration options of the project.', width=500)
        gui.EventSource.__init__(self)
        #standard configuration
        self.configDict = {}

        self.configDict[self.KEY_PRJ_NAME] = 'untitled'
        self.configDict[self.KEY_ADDRESS] = '0.0.0.0'
        self.configDict[self.KEY_PORT] = 8081
        self.configDict[self.KEY_MULTIPLE_INSTANCE] = True
        self.configDict[self.KEY_ENABLE_CACHE] = True
        self.configDict[self.KEY_START_BROWSER] = True
        self.configDict[self.KEY_RESOURCEPATH] = "./res/"

        self.add_field_with_label( self.KEY_PRJ_NAME, 'Project Name', gui.TextInput() )
        self.add_field_with_label( self.KEY_ADDRESS, 'IP address', gui.TextInput() )
        self.add_field_with_label( self.KEY_PORT, 'Listen port', gui.SpinBox(8082, 1025, 65535) )
        self.add_field_with_label( self.KEY_MULTIPLE_INSTANCE, 'Use single App instance for multiple users', gui.CheckBox(True) )
        self.add_field_with_label( self.KEY_ENABLE_CACHE, 'Enable file caching', gui.CheckBox(True) )
        self.add_field_with_label( self.KEY_START_BROWSER, 'Start browser automatically', gui.CheckBox(True) )
        self.add_field_with_label( self.KEY_RESOURCEPATH, 'Additional resource path', gui.TextInput() )
        self.from_dict_to_fields(self.configDict)

    def from_dict_to_fields(self, dictionary):
        for key in self.inputs.keys():
            if key in dictionary.keys():
                self.get_field(key).set_value( str( dictionary[key] ) )

    def from_fields_to_dict(self):
        self.configDict[self.KEY_PRJ_NAME] = self.get_field(self.KEY_PRJ_NAME).get_value()
        self.configDict[self.KEY_ADDRESS] = self.get_field(self.KEY_ADDRESS).get_value()
        self.configDict[self.KEY_PORT] = int( self.get_field(self.KEY_PORT).get_value() )
        self.configDict[self.KEY_MULTIPLE_INSTANCE] = self.get_field(self.KEY_MULTIPLE_INSTANCE).get_value()
        self.configDict[self.KEY_ENABLE_CACHE] = self.get_field(self.KEY_ENABLE_CACHE).get_value()
        self.configDict[self.KEY_START_BROWSER] = self.get_field(self.KEY_START_BROWSER).get_value()
        self.configDict[self.KEY_RESOURCEPATH] = self.get_field(self.KEY_RESOURCEPATH).get_value()

    @gui.decorate_event
    def confirm_dialog(self, emitter):
        """event called pressing on OK button.
        """
        #here the user input is transferred to the dict, ready to use
        self.from_fields_to_dict()
        return super(ProjectConfigurationDialog,self).confirm_dialog(self)

    def show(self, baseAppInstance):
        """Allows to show the widget as root window"""
        self.from_dict_to_fields(self.configDict)
        super(ProjectConfigurationDialog, self).show(baseAppInstance)


class EditorFileSelectionDialog(gui.FileSelectionDialog):
    def __init__(self, title='File dialog', message='Select files and folders',
                multiple_selection=True, selection_folder='.', allow_file_selection=True,
                allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSelectionDialog, self).__init__( title,
                 message, multiple_selection, selection_folder,
                 allow_file_selection, allow_folder_selection)

        self.baseAppInstance = baseAppInstance

    def show(self, *args):
        super(EditorFileSelectionDialog, self).show(self.baseAppInstance)


class EditorFileSaveDialog(gui.FileSelectionDialog, gui.EventSource):
    def __init__(self, title='File dialog', message='Select files and folders',
                multiple_selection=True, selection_folder='.',
                 allow_file_selection=True, allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSaveDialog, self).__init__( title, message, multiple_selection, selection_folder,
                 allow_file_selection, allow_folder_selection)
        gui.EventSource.__init__(self)

        self.baseAppInstance = baseAppInstance

    def show(self, *args):
        super(EditorFileSaveDialog, self).show(self.baseAppInstance)

    def add_fileinput_field(self, defaultname='untitled'):
        self.txtFilename = gui.TextInput()
        self.txtFilename.onkeydown.do(self.on_enter_key_pressed)
        self.txtFilename.set_text(defaultname)

        self.add_field_with_label("filename","Filename",self.txtFilename)

    def get_fileinput_value(self):
        return self.get_field('filename').get_value()

    def on_enter_key_pressed(self, widget, value, keycode):
        if keycode=="13":
            self.confirm_value(None)

    @gui.decorate_event
    def confirm_value(self, widget):
        """event called pressing on OK button.
           propagates the string content of the input field
        """
        self.hide()
        params = (self.fileFolderNavigator.pathEditor.get_text(),)
        return params


class WidgetHelper(gui.HBox):
    """ Allocates the Widget to which it refers,
        interfacing to the user in order to obtain the necessary attribute values
        obtains the constructor parameters, asks for them in a dialog
        puts the values in an attribute called constructor
    """

    def __init__(self, appInstance, widgetClass, **kwargs_to_widget):
        self.kwargs_to_widget = kwargs_to_widget
        self.appInstance = appInstance
        self.widgetClass = widgetClass
        super(WidgetHelper, self).__init__()
        self.style['display'] = 'block'
        self.style['background-color'] = 'white'
        self.icon = gui.Image('/editor_resources:widget_%s.png'%self.widgetClass.__name__, width='auto', margin='2px')
        self.icon.style['max-width'] = '100%'
        self.icon.style['image-rendering'] = 'auto'
        self.icon.attributes['draggable'] = 'false'
        self.icon.attributes['ondragstart'] = "event.preventDefault();"
        self.append(self.icon)

        self.attributes.update({'draggable':'true',
            'ondragstart':"this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify(['add',event.target.id,(event.clientX),(event.clientY)]));",
            'ondragover':"event.preventDefault();",
            'ondrop':"event.preventDefault();return false;"})

        self.optional_style_dict = {} #this dictionary will contain optional style attributes that have to be added to the widget once created

        self.onclick.do(self.prompt_new_widget)

    def build_widget_name_list_from_tree(self, node):
        if not hasattr(node, 'attributes'):
            return
        if not 'editor_varname' in node.attributes.keys():
            return
        self.varname_list.append(node.attributes['editor_varname'])
        for child in node.children.values():
            self.build_widget_name_list_from_tree(child)

    def prompt_new_widget(self, widget):
        self.varname_list = list()

        self.build_widget_name_list_from_tree(self.appInstance.project)

        self.constructor_parameters_list = self.widgetClass.__init__.__code__.co_varnames[1:] #[1:] removes the self
        param_annotation_dict = ''#self.widgetClass.__init__.__annotations__
        self.dialog = gui.GenericDialog(title=self.widgetClass.__name__, message='Fill the following parameters list', width='40%')
        varNameTextInput = gui.TextInput()
        varNameTextInput.attributes['tabindex'] = '1'
        varNameTextInput.attributes['autofocus'] = 'autofocus'
        self.dialog.add_field_with_label('name', 'Variable name', varNameTextInput)
        #for param in self.constructor_parameters_list:
        for index in range(0,len(self.widgetClass.__init__._constructor_types)):
            param = self.constructor_parameters_list[index]
            _typ = self.widgetClass.__init__._constructor_types[index]
            note = ' (%s)'%_typ.__name__
            editWidget = None
            if _typ==int:
                editWidget = gui.SpinBox('0',-65536,65535)
            elif _typ==bool:
                editWidget = gui.CheckBox()
            else:
                editWidget = gui.TextInput()
            editWidget.attributes['tabindex'] = str(index+2)
            self.dialog.add_field_with_label(param, param + note, editWidget)

        self.dialog.add_field_with_label("editor_newclass", "Overload base class", gui.CheckBox())
        self.dialog.confirm_dialog.do(self.on_dialog_confirm)
        self.dialog.show(self.appInstance)

    def on_dropped(self, left, top):
        self.optional_style_dict['left'] = gui.to_pix(left)
        self.optional_style_dict['top'] = gui.to_pix(top)
        self.prompt_new_widget(None)

    def on_dialog_confirm(self, widget):
        """ Here the widget is allocated
        """
        variableName = str(self.dialog.get_field("name").get_value())
        if re.match('(^[a-zA-Z][a-zA-Z0-9_]*)|(^[_][a-zA-Z0-9_]+)', variableName) == None:
            self.errorDialog = gui.GenericDialog("Error", "Please type a valid variable name.", width=350,height=120)
            self.errorDialog.show(self.appInstance)
            return

        if variableName in self.varname_list:
            self.errorDialog = gui.GenericDialog("Error", "The typed variable name is already used. Please specify a new name.", width=350,height=150)
            self.errorDialog.show(self.appInstance)
            return

        param_annotation_dict = ''#self.widgetClass.__init__.__annotations__
        param_values = []
        param_for_constructor = []
        for index in range(0,len(self.widgetClass.__init__._constructor_types)):
            param = self.constructor_parameters_list[index]
            _typ = self.widgetClass.__init__._constructor_types[index]
            if _typ==int:
                param_for_constructor.append(self.dialog.get_field(param).get_value())
                param_values.append(int(self.dialog.get_field(param).get_value()))
            elif _typ==bool:
                param_for_constructor.append(self.dialog.get_field(param).get_value())
                param_values.append(bool(self.dialog.get_field(param).get_value()))
            else:#if _typ==str:
                param_for_constructor.append("""\'%s\'"""%self.dialog.get_field(param).get_value())
                param_values.append(self.dialog.get_field(param).get_value())
            #else:
            #    param_for_constructor.append("""%s"""%self.dialog.get_field(param).get_value())

        print(self.constructor_parameters_list)
        print(param_values)
        #constructor = '%s(%s)'%(self.widgetClass.__name__, ','.join(map(lambda v: str(v), param_values)))
        constructor = '(%s)'%(','.join(map(lambda v: str(v), param_for_constructor)))
        #here we create and decorate the widget
        widget = self.widgetClass(*param_values, **self.kwargs_to_widget)
        widget.attributes.update({'editor_constructor':constructor,
            'editor_varname':variableName,
            'editor_tag_type':'widget',
            'editor_newclass':'True' if self.dialog.get_field("editor_newclass").get_value() else 'False',
            'editor_baseclass':widget.__class__.__name__}) #__class__.__bases__[0].__name__
        #"this.style.cursor='default';this.style['left']=(event.screenX) + 'px'; this.style['top']=(event.screenY) + 'px'; event.preventDefault();return true;"
        #if not 'position' in widget.style:
        #    widget.style['position'] = 'absolute'
        #if not 'display' in widget.style:
        #    widget.style['display'] = 'block'

        for key in self.optional_style_dict:
            widget.style[key] = self.optional_style_dict[key]
        self.optional_style_dict = {}

        self.appInstance.add_widget_to_editor(widget)


class WidgetCollection(gui.Widget):
    def __init__(self, appInstance, **kwargs):
        self.appInstance = appInstance
        super(WidgetCollection, self).__init__(**kwargs)
        self.lblTitle = gui.Label("Widgets Toolbox")
        self.lblTitle.add_class("DialogTitle")
        self.widgetsContainer = gui.HBox(width='100%', height='85%')
        self.widgetsContainer.style.update({'overflow-y':'scroll',
            'overflow-x':'hidden',
            'flex-wrap':'wrap',
            'background-color':'white'})

        self.append([self.lblTitle, self.widgetsContainer])

        #load all widgets
        self.add_widget_to_collection(gui.HBox, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.VBox, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Widget, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.GridBox, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Button, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.TextInput, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Label, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.ListView, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute', 'border':'1px solid lightgray'})
        self.add_widget_to_collection(gui.ListItem)
        self.add_widget_to_collection(gui.DropDown, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.DropDownItem)
        self.add_widget_to_collection(gui.Image, width='100px', height='100px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.CheckBoxLabel, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.CheckBox, width='30px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.SpinBox, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Slider, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.ColorPicker, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Date, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Link, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Progress, width='130px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.VideoPlayer, width='100px', height='100px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.TableWidget, width='100px', height='100px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Svg, style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.SvgLine, attributes={'stroke':'black', 'stroke-width':'1'})
        self.add_widget_to_collection(gui.SvgCircle)
        self.add_widget_to_collection(gui.SvgRectangle)
        self.add_widget_to_collection(gui.SvgText)
        self.add_widget_to_collection(gui.SvgPath, attributes={'stroke':'black', 'stroke-width':'1'})

    def add_widget_to_collection(self, widgetClass, **kwargs_to_widget):
        #create an helper that will be created on click
        #the helper have to search for function that have 'return' annotation 'event_listener_setter'
        helper = WidgetHelper(self.appInstance, widgetClass, **kwargs_to_widget)
        helper.attributes['title'] = widgetClass.__doc__
        self.widgetsContainer.append( helper )


class EditorAttributesGroup(gui.Widget):
    """ Contains a title and widgets. When the title is clicked, the contained widgets are hidden.
        Its scope is to provide a foldable group
    """
    def __init__(self, title, **kwargs):
        super(EditorAttributesGroup, self).__init__(**kwargs)
        self.add_class('.RaisedFrame')
        self.style['display'] = 'block'
        self.style['overflow'] = 'visible'
        self.opened = True
        self.title = gui.Label(title)
        self.title.add_class("Title")
        self.title.style.update({'padding-left':'32px',
            'background-image':"url('/editor_resources:minus.png')",
            'background-repeat':'no-repeat',
            'background-position':'5px',
            'border-top':'3px solid lightgray'})
        self.title.onclick.do(self.openClose)
        self.append(self.title, '0')

    def openClose(self, widget):
        self.opened = not self.opened
        backgroundImage = "url('/editor_resources:minus.png')" if self.opened else "url('/editor_resources:plus.png')"
        self.title.style['background-image'] = backgroundImage
        display = 'block' if self.opened else 'none'
        for widget in self.children.values():
            if widget!=self.title and type(widget)!=str:
                widget.style['display'] = display


class EditorAttributes(gui.VBox, gui.EventSource):
    """ Contains EditorAttributeInput each one of which notify a new value with an event
    """
    def __init__(self, appInstance, **kwargs):
        super(EditorAttributes, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'
        #self.style['overflow-y'] = 'scroll'
        self.style['justify-content'] = 'flex-start'
        self.style['-webkit-justify-content'] = 'flex-start'
        self.titleLabel = gui.Label('Attributes editor', width='100%')
        self.titleLabel.add_class("DialogTitle")
        self.infoLabel = gui.Label('Selected widget: None')
        self.infoLabel.style['font-weight'] = 'bold'
        self.append([self.titleLabel, self.infoLabel])

        self.titleLabel.style['order'] = '-1'
        self.titleLabel.style['-webkit-order'] = '-1'
        self.infoLabel.style['order'] = '0'
        self.infoLabel.style['-webkit-order'] = '0'

        self.attributesInputs = list()
        #load editable attributes
        self.append(self.titleLabel)
        self.attributeGroups = {}
        for attribute in html_helper.editorAttributeList:
            attributeName = attribute[0]
            attributeValue = attribute[1]
            attributeEditor = EditorAttributeInput(attributeName, attributeValue, appInstance)
            attributeEditor.on_attribute_changed.do(self.onattribute_changed)
            attributeEditor.on_attribute_remove.do(self.onattribute_remove)
            #attributeEditor.style['display'] = 'none'
            if not attributeValue['group'] in self.attributeGroups.keys():
                groupContainer = EditorAttributesGroup(attributeValue['group'], width='100%')
                self.attributeGroups[attributeValue['group']] = groupContainer
                self.append(groupContainer)
                groupContainer.style['order'] = str(html_helper.editorAttributesGroupOrdering[attributeValue['group']])
                groupContainer.style['-webkit-order'] = str(html_helper.editorAttributesGroupOrdering[attributeValue['group']])

            self.attributeGroups[attributeValue['group']].append(attributeEditor)
            self.attributesInputs.append(attributeEditor)

    #this function is called by an EditorAttributeInput change event and propagates to the listeners
    #adding as first parameter the tag to which it refers
    #widgetAttributeMember can be 'style' or 'attributes'
    @gui.decorate_event
    def onattribute_changed(self, widget, widgetAttributeMember, attributeName, newValue):
        print("setting attribute name: %s    value: %s    attributeMember: %s"%(attributeName, newValue, widgetAttributeMember))
        getattr(self.targetWidget, widgetAttributeMember)[attributeName] = str(newValue)
        return (widgetAttributeMember, attributeName, newValue)

    @gui.decorate_event
    def onattribute_remove(self, widget, widgetAttributeMember, attributeName):
        if attributeName in getattr(self.targetWidget, widgetAttributeMember):
            del getattr(self.targetWidget, widgetAttributeMember)[attributeName]
        return (widgetAttributeMember, attributeName)

    def set_widget(self, widget):
        self.infoLabel.set_text("Selected widget: %s"%widget.attributes['editor_varname'])
        self.attributes['selected_widget_id'] = widget.identifier
        self.targetWidget = widget
        for w in self.attributesInputs:
            w.style['display'] = 'block'
            #w.style['visibility'] = 'visible'
            if w.attributeDict['additional_data'].get('applies_to', None):
                if not type(widget) in w.attributeDict['additional_data'].get('applies_to', None):
                    w.style['display'] = 'none'
            w.set_from_dict(getattr(widget, w.attributeDict['affected_widget_attribute']))


class CssSizeInput(gui.Widget, gui.EventSource):
    def __init__(self, appInstance, **kwargs):
        super(CssSizeInput, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.appInstance = appInstance
        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style['display'] = 'block'
        self.style['overflow'] = 'hidden'

        self.numInput = gui.SpinBox('0',-999999999, 999999999, 1, width='60%', height='100%')
        self.numInput.onchange.do(self.onchange)
        self.numInput.style['text-align'] = 'right'
        self.append(self.numInput)

        self.dropMeasureUnit = gui.DropDown(width='40%', height='100%')
        self.dropMeasureUnit.append( gui.DropDownItem('px'), 'px' )
        self.dropMeasureUnit.append( gui.DropDownItem('%'), '%' )
        self.dropMeasureUnit.select_by_key('px')
        self.dropMeasureUnit.onchange.do(self.onchange)
        self.append(self.dropMeasureUnit)

    @gui.decorate_event
    def onchange(self, widget, new_value):
        new_size = str(self.numInput.get_value()) + str(self.dropMeasureUnit.get_value())
        return (new_size,)

    def set_value(self, value):
        """The value have to be in the form '10px' or '10%', so numeric value plus measure unit
        """
        v = 0
        measure_unit = 'px'
        try:
            v = int(float(value.replace('px', '')))
        except ValueError:
            try:
                v = int(float(value.replace('%', '')))
                measure_unit = '%'
            except ValueError:
                pass
        self.numInput.set_value(v)
        self.dropMeasureUnit.set_value(measure_unit)


class UrlPathInput(gui.Widget, gui.EventSource):
    def __init__(self, appInstance, **kwargs):
        super(UrlPathInput, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.appInstance = appInstance
        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style['display'] = 'block'
        self.style['overflow'] = 'hidden'

        self.txtInput = gui.TextInput(width='80%', height='100%')
        self.txtInput.style['float'] = 'left'
        self.txtInput.onchange.do(self.on_txt_changed)
        self.append(self.txtInput)

        self.btFileFolderSelection = gui.Widget(width='20%', height='100%')
        self.btFileFolderSelection.style.update({'background-repeat':'round',
            'background-image':"url('/res:folder.png')",
            'background-color':'transparent'})
        self.append(self.btFileFolderSelection)
        self.btFileFolderSelection.onclick.do(self.on_file_selection_bt_pressed)

        self.selectionDialog = gui.FileSelectionDialog('Select a file', '', False, './', True, False)
        self.selectionDialog.confirm_value.do(self.file_dialog_confirmed)

    @gui.decorate_event
    def onchange(self, widget, value):
        return (value,)
    
    def on_txt_changed(self, widget, value):
        return self.onchange(None, value)

    def on_file_selection_bt_pressed(self, widget):
        self.selectionDialog.show(self.appInstance)

    def file_dialog_confirmed(self, widget, fileList):
        if len(fileList)>0:
            self.txtInput.set_value("url('/editor_resources:" + fileList[0].split('/')[-1].split('\\')[-1] + "')")
            return self.onchange(None, self.txtInput.get_value())

    def set_value(self, value):
        self.txtInput.set_value(value)


#widget that allows to edit a specific html and css attributes
#   it has a descriptive label, an edit widget (TextInput, SpinBox..) based on the 'type' and a title
class EditorAttributeInput(gui.Widget, gui.EventSource):
    def __init__(self, attributeName, attributeDict, appInstance=None):
        super(EditorAttributeInput, self).__init__()
        gui.EventSource.__init__(self)
        self.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
        self.style.update({'display':'block',
            'overflow':'auto',
            'margin':'2px',
            'outline':'1px solid lightgray'})
        self.attributeName = attributeName
        self.attributeDict = attributeDict
        self.EVENT_ATTRIB_ONCHANGE = 'on_attribute_changed'

        self.EVENT_ATTRIB_ONREMOVE = 'onremove_attribute'
        self.removeAttribute = gui.Image('/editor_resources:delete.png', width='5%')
        self.removeAttribute.attributes['title'] = 'Remove attribute from this widget.'
        self.removeAttribute.onclick.do(self.on_attribute_remove)
        self.append(self.removeAttribute)

        self.label = gui.Label(attributeName, width='45%', height=22, margin='0px')
        self.label.style['overflow'] = 'hidden'
        self.label.style['font-size'] = '13px'
        self.label.style['outline'] = '1px solid lightgray'
        self.append(self.label)
        self.inputWidget = None

        #'background-repeat':{'type':str, 'description':'The repeat behaviour of an optional background image', ,'additional_data':{'affected_widget_attribute':'style', 'possible_values':'repeat | repeat-x | repeat-y | no-repeat | inherit'}},
        if attributeDict['type'] in (bool,int,float,gui.ColorPicker,gui.DropDown,'url_editor','css_size'):
            if attributeDict['type'] == bool:
                self.inputWidget = gui.CheckBox('checked')
            if attributeDict['type'] == int or attributeDict['type'] == float:
                self.inputWidget = gui.SpinBox(attributeDict['additional_data']['default'], attributeDict['additional_data']['min'], attributeDict['additional_data']['max'], attributeDict['additional_data']['step'])
            if attributeDict['type'] == gui.ColorPicker:
                self.inputWidget = gui.ColorPicker()
            if attributeDict['type'] == gui.DropDown:
                self.inputWidget = gui.DropDown()
                for value in attributeDict['additional_data']['possible_values']:
                    self.inputWidget.append(gui.DropDownItem(value),value)
            if attributeDict['type'] == 'url_editor':
                self.inputWidget = UrlPathInput(appInstance)
            if attributeDict['type'] == 'css_size':
                self.inputWidget = CssSizeInput(appInstance)

        else: #default editor is string
            self.inputWidget = gui.TextInput()

        self.inputWidget.onchange.do(self.on_attribute_changed)
        self.inputWidget.set_size('50%','22px')
        self.inputWidget.attributes['title'] = attributeDict['description']
        self.label.attributes['title'] = attributeDict['description']
        self.append(self.inputWidget)
        self.inputWidget.style['float'] = 'right'

        self.style['display'] = 'block'
        self.set_valid(False)

    def set_valid(self, valid=True):
        self.label.style['opacity'] = '1.0'
        if 'display' in self.removeAttribute.style:
            del self.removeAttribute.style['display']
        if not valid:
            self.label.style['opacity'] = '0.5'
            self.removeAttribute.style['display'] = 'none'

    @gui.decorate_event
    def on_attribute_remove(self, widget):
        self.set_valid(False)
        return (self.attributeDict['affected_widget_attribute'], self.attributeName)

    def set_from_dict(self, dictionary):
        self.inputWidget.set_value('')
        self.set_valid(False)
        if self.attributeName in dictionary:
            self.set_valid()
            self.inputWidget.set_value(dictionary[self.attributeName])

    def set_value(self, value):
        self.set_valid()
        self.inputWidget.set_value(value)

    @gui.decorate_event
    def on_attribute_changed(self, widget, value):
        self.set_valid()
        return (self.attributeDict['affected_widget_attribute'], self.attributeName, value)

