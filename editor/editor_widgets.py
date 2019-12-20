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
import remi
import remi.gui as gui
import html_helper
import inspect
import re
import logging
import types
import traceback


class InstancesTree(gui.TreeView):
    def __init__(self, **kwargs):
        super(InstancesTree, self).__init__(**kwargs)

    def append_instance(self, instance, parent):
        item = gui.TreeItem(instance.identifier)
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
        if not (hasattr(node, 'attr_editor') and node.attr_editor):
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


class ToolBar(gui.Container):
    def __init__(self, **kwargs):
        super(ToolBar, self).__init__(**kwargs)
        self.set_layout_orientation(gui.Container.LAYOUT_HORIZONTAL)
        self.style['background-color'] = 'white'

    def add_command(self, imagePath, callback, title):
        icon = gui.Image(imagePath, height='90%', margin='0px 1px')
        icon.style['outline'] = '1px solid lightgray'
        icon.onclick.do(callback)
        icon.attributes['title'] = title
        self.append(icon)


class ClassEventConnectorEditor(gui.ClassEventConnector):
    """ This class allows to manage the events. Decorating a method with *decorate_event* decorator
        The method gets the __is_event flag. At runtime, the methods that has this flag gets replaced
        by a ClassEventConnector. This class overloads the __call__ method, where the event method is called,
        and after that the listener method is called too.
    """
    editor_listener_callback = None #this is the event listener setup by the editor that will receive the events first

    def __call__(self, *args, **kwargs):
        #here the event method gets called
        callback_params =  self.event_method_bound(*args, **kwargs)

        if not self.editor_listener_callback is None:
            self.editor_listener_callback(self.event_source_instance, *callback_params, **self.kwuserdata)

        if not self.callback:
            return callback_params
        if not callback_params:
            callback_params = self.userdata
        else:
            callback_params = callback_params + self.userdata

        #here the listener gets called, passing as parameters the return values of the event method
        # plus the userdata parameters
        return self.callback(self.event_source_instance, *callback_params, **self.kwuserdata)


class SignalConnection(gui.HBox):
    def __init__(self, widget, listenersList, eventConnectionFuncName, eventConnectionFunc, **kwargs):
        super(SignalConnection, self).__init__(**kwargs)

        self.style.update({'overflow':'visible', 'height':'24px', 'outline':'1px solid lightgray'})
        self.label = gui.Label(eventConnectionFuncName, width='32%')
        self.label.style.update({'float':'left', 'font-size':'10px', 'overflow':'hidden', 'outline':'1px solid lightgray'})

        self.dropdownListeners = gui.DropDown(width='32%', height='100%')
        self.dropdownListeners.onchange.do(self.on_listener_selection)
        self.dropdownListeners.attributes['title'] = "The listener who will receive the event"

        self.dropdownMethods = gui.DropDown(width='32%', height='100%')
        self.dropdownMethods.onchange.do(self.on_connection)
        self.dropdownMethods.attributes['title'] = """The listener's method who will receive the event. \
        A custom method is selected by default. You can select another method, but you should check the method parameters."""


        self.eventConnectionFunc = eventConnectionFunc
        self.eventConnectionFuncName = eventConnectionFuncName
        self.refWidget = widget
        self.listenersList = listenersList
        self.dropdownListeners.append(gui.DropDownItem("None"))
        for w in listenersList:
            ddi = gui.DropDownItem(w.identifier)
            ddi.listenerInstance = w
            self.dropdownListeners.append(ddi)

        if not self.eventConnectionFunc.callback is None:
            try:
                connectedListenerName = ''
                connectedListenerFunction = None
                print(str(type(eventConnectionFunc.callback)))
                
                if issubclass(type(eventConnectionFunc.callback), gui.ClassEventConnector):
                    connectedListenerName = eventConnectionFunc.callback.event_method_bound.__self__.identifier
                    connectedListenerFunction = eventConnectionFunc.callback.event_method_bound
                else:
                    connectedListenerName = eventConnectionFunc.callback.__self__.identifier
                    connectedListenerFunction = eventConnectionFunc.callback
                
                self.dropdownListeners.select_by_value( connectedListenerName )
                #this to automatically populate the listener methods dropdown
                
                self.on_listener_selection(self.dropdownListeners, connectedListenerName)
                print("connected function name:"+connectedListenerFunction.__name__)
                self.dropdownMethods.select_by_value(connectedListenerFunction.__name__ )
                #force the connection
                self.on_connection(None, None)
            except:
                print(traceback.format_exc())
                print(dir(eventConnectionFunc.callback))
                self.disconnect()

        self.append([self.label, self.dropdownListeners, self.dropdownMethods])

    def on_listener_selection(self, widget, dropDownValue):
        self.dropdownMethods.empty()
        if self.dropdownListeners.get_value()=='None':
            self.disconnect()
        else:
            listener = self.dropdownListeners._selected_item.listenerInstance

            l = []
            func_members = inspect.getmembers(listener)#, inspect.ismethod)
            for (name, value) in func_members:
                #if issubclass(type(value), gui.ClassEventConnector):
                #    value = value.event_method_bound
                if name not in ['__init__', 'main', 'idle', 'construct_ui'] and type(value) == types.MethodType or issubclass(type(value), gui.ClassEventConnector):
                    ddi = gui.DropDownItem(name)
                    ddi.listenerInstance = listener
                    ddi.listenerFunction = value
                    l.append(ddi)
            
            #creating a none element
            ddi = gui.DropDownItem('None')
            self.dropdownMethods.append(ddi)

            #here I create a custom listener for the specific event and widgets, the user can select this or an existing method
            if listener.attr_editor_newclass:
                custom_listener_name = self.eventConnectionFuncName + "_" + self.refWidget.identifier
                setattr(listener, custom_listener_name, types.MethodType(copy_func(fakeListenerFunc), listener))
                getattr(listener, custom_listener_name).__func__.__name__ = custom_listener_name
                ddi = gui.DropDownItem(custom_listener_name)
                ddi.listenerInstance = listener
                ddi.listenerFunction = getattr(listener, custom_listener_name)
                ddi.style['color'] = "green"
                ddi.style['font-weight'] = "bolder"
                ddi.attributes['title'] = "automatically generated method"
                self.dropdownMethods.append(ddi)

            self.dropdownMethods.append(l)

    def disconnect(self):
        #the listener is canceled when the user selects None
        getattr(self.refWidget, self.eventConnectionFuncName).do(None)
        #getattr(self.refWidget, self.eventConnectionFuncName).editor_listener_callback = None

    def on_connection(self, widget, dropDownValue):
        if self.dropdownMethods.get_value()=='None':
            self.disconnect()
            return

        listener = self.dropdownMethods._selected_item.listenerInstance
        getattr(self.refWidget, self.eventConnectionFuncName).do(self.dropdownMethods._selected_item.listenerFunction)


def copy_func(f):
    """Based on https://stackoverflow.com/questions/13503079/how-to-create-a-copy-of-a-python-function"""
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    #g = functools.update_wrapper(g, f)
    if hasattr(f, "__kwdefaults__"):
        g.__kwdefaults__ = f.__kwdefaults__
    return g

def fakeListenerFunc(self,*args):
    print('event trap')

class SignalConnectionManager(gui.Container):
    """ This class allows to interconnect event signals """
    def __init__(self, *args, **kwargs):
        super(SignalConnectionManager, self).__init__(*args, **kwargs)
        self.label = gui.Label('Signal connections', width='100%')
        self.label.add_class("DialogTitle")
        self.append(self.label)
        self.listeners_list = []

    def build_widget_list_from_tree(self, node):
        self.listeners_list.append(node)
        for child in node.children.values():
            if hasattr(child, 'attributes') and (hasattr(child, 'attr_editor') and child.attr_editor):
                self.build_widget_list_from_tree(child)

    def update(self, widget, widget_tree):
        """ for the selected widget are listed the relative signals
            for each signal there is a dropdown containing all the widgets
            the user will select the widget that have to listen a specific event
        """
        self.listeners_list = []
        self.build_widget_list_from_tree(widget_tree)

        self.label.set_text('Signal connections: ' + widget.identifier)
        #del self.container
        self.container = gui.VBox(width='100%', height='90%')
        self.container.style['justify-content'] = 'flex-start'
        self.container.style['overflow-y'] = 'scroll'
        
        ##for all the events of this widget
        #isclass instead of ismethod because event methods are replaced with ClassEventConnector
        for (setOnEventListenerFuncname,setOnEventListenerFunc) in inspect.getmembers(widget):
            #if the member is decorated by decorate_set_on_listener and the function is referred to this event
            if issubclass(type(setOnEventListenerFunc), gui.ClassEventConnector):
                self.container.append( SignalConnection(widget, 
                    self.listeners_list, 
                    setOnEventListenerFuncname, 
                    setOnEventListenerFunc, 
                    width='100%') )

        self.append(self.container, 'container')


class ProjectConfigurationDialog(gui.GenericDialog):
    KEY_PRJ_NAME = 'config_project_name'
    KEY_ADDRESS = 'config_address'
    KEY_PORT = 'config_port'
    KEY_MULTIPLE_INSTANCE = 'config_multiple_instance'
    KEY_ENABLE_CACHE = 'config_enable_file_cache'
    KEY_START_BROWSER = 'config_start_browser'
    KEY_RESOURCEPATH = 'config_resourcepath'

    def __init__(self, title='', message=''):
        super(ProjectConfigurationDialog, self).__init__('Project Configuration', 'Here are the configuration options of the project.', width=500)
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


class EditorFileSaveDialog(gui.FileSelectionDialog):
    def __init__(self, title='File dialog', message='Select files and folders',
                multiple_selection=True, selection_folder='.',
                 allow_file_selection=True, allow_folder_selection=True, baseAppInstance = None):
        super(EditorFileSaveDialog, self).__init__( title, message, multiple_selection, selection_folder,
                 allow_file_selection, allow_folder_selection)

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
        self.style.update({'background-color':'white', 'width':"60px", "height":"60px", "justify-content":"center", "align-items":"center"})
        if hasattr(widgetClass, "icon"):
            if type(widgetClass.icon)==gui.Svg:
                self.icon = widgetClass.icon
            else:
                icon_file = widgetClass.icon
                self.icon = gui.Image(icon_file, width='auto', margin='2px')
        else:
            icon_file = '/editor_resources:widget_%s.png'%self.widgetClass.__name__
            self.icon = gui.Image(icon_file, width='auto', margin='2px')
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

        self.onclick.do(self.create_instance)

    def build_widget_name_list_from_tree(self, node):
        if not hasattr(node, 'attributes'):
            return
        if not (hasattr(node, 'attr_editor') and node.attr_editor):
            return
        self.varname_list.append(node.identifier)
        for child in node.children.values():
            self.build_widget_name_list_from_tree(child)

    def on_dropped(self, left, top):
        self.optional_style_dict['left'] = gui.to_pix(left)
        self.optional_style_dict['top'] = gui.to_pix(top)
        self.create_instance(None)

    def create_instance(self, widget):
        """ Here the widget is allocated
        """
        self.varname_list = []
        self.build_widget_name_list_from_tree(self.appInstance.project)
        variableName = ''
        for i in range(0,1000): #reasonably no more than 1000 widget instances in a project
            variableName = self.widgetClass.__name__.lower() + str(i)
            if not variableName in self.varname_list:
                break
        
        """
        if re.match('(^[a-zA-Z][a-zA-Z0-9_]*)|(^[_][a-zA-Z0-9_]+)', variableName) == None:
            self.errorDialog = gui.GenericDialog("Error", "Please type a valid variable name.", width=350,height=120)
            self.errorDialog.show(self.appInstance)
            return

        if variableName in self.varname_list:
            self.errorDialog = gui.GenericDialog("Error", "The typed variable name is already used. Please specify a new name.", width=350,height=150)
            self.errorDialog.show(self.appInstance)
            return
        """
        #here we create and decorate the widget
        widget = self.widgetClass(**self.kwargs_to_widget)
        widget.attr_editor = True
        widget.attr_editor_newclass = False
        widget.identifier = variableName

        for key in self.optional_style_dict:
            widget.style[key] = self.optional_style_dict[key]
        self.optional_style_dict = {}

        self.appInstance.add_widget_to_editor(widget)


class WidgetCollection(gui.Container):
    def __init__(self, appInstance, **kwargs):
        self.appInstance = appInstance
        super(WidgetCollection, self).__init__(**kwargs)
        self.lblTitle = gui.Label("Widgets Toolbox")
        self.lblTitle.add_class("DialogTitle")
        self.widgetsContainer = gui.HBox(width='100%', height='85%')
        self.widgetsContainer.style.update({'overflow-y':'scroll',
            'overflow-x':'hidden',
            'align-items':'flex-start',
            'flex-wrap':'wrap',
            'background-color':'white'})

        self.append([self.lblTitle, self.widgetsContainer])

        #load all widgets
        self.add_widget_to_collection(gui.HBox, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.VBox, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Container, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        #self.add_widget_to_collection(gui.GridBox, width='250px', height='250px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Button, text="button", width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.TextInput, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Label, text="label", width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.ListView, width='100px', height='100px', style={'top':'20px', 'left':'20px', 'position':'absolute', 'border':'1px solid lightgray'})
        self.add_widget_to_collection(gui.ListItem, text='list item')
        self.add_widget_to_collection(gui.DropDown, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.DropDownItem, text='drop down item')
        self.add_widget_to_collection(gui.Image, width='100px', height='100px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.CheckBoxLabel, text='check box label', width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.CheckBox, width='30px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.SpinBox, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Slider, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.ColorPicker, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Date, width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Link, text='link', url='', width='100px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Progress, value=0, _max=100, width='130px', height='30px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.VideoPlayer, width='100px', height='100px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.TableWidget, width='100px', height='100px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.TabBox, width='200px', height='200px', style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.Svg, style={'top':'20px', 'left':'20px', 'position':'absolute'})
        self.add_widget_to_collection(gui.SvgLine, attributes={'stroke':'black', 'stroke-width':'1'})
        self.add_widget_to_collection(gui.SvgCircle)
        self.add_widget_to_collection(gui.SvgRectangle)
        self.add_widget_to_collection(gui.SvgText)
        self.add_widget_to_collection(gui.SvgPath, attributes={'stroke':'black', 'stroke-width':'1'})

        self.load_additional_widgets()

    def load_additional_widgets(self):
        try:
            import widgets
            classes = inspect.getmembers(widgets, inspect.isclass)
            for (classname, classvalue) in classes:
                if issubclass(classvalue,gui.Widget):
                    self.add_widget_to_collection(classvalue, classvalue.__module__)
            
        except:
            logging.getLogger('remi.editor').error('error loading external widgets', exc_info=True)

    def add_widget_to_collection(self, widgetClass, group='standard_tools', **kwargs_to_widget):
        #create an helper that will be created on click
        #the helper have to search for function that have 'return' annotation 'event_listener_setter'
        if group not in self.widgetsContainer.children.keys():
            self.widgetsContainer.append(EditorAttributesGroup(group), group)
            self.widgetsContainer.children[group].style['width'] = "100%"

        helper = WidgetHelper(self.appInstance, widgetClass, **kwargs_to_widget)
        helper.attributes['title'] = widgetClass.__doc__
        #self.widgetsContainer.append( helper )
        self.widgetsContainer.children[group].append( helper )


class EditorAttributesGroup(gui.VBox):
    """ Contains a title and widgets. When the title is clicked, the contained widgets are hidden.
        Its scope is to provide a foldable group
    """
    def __init__(self, title, **kwargs):
        super(EditorAttributesGroup, self).__init__(**kwargs)
        self.add_class('.RaisedFrame')
        #self.style['display'] = 'block'
        self.container = gui.HBox(width="100%", style={'overflow':'visible','justify-content':'flex-start','align-items':'flex-start','flex-wrap':'wrap'})
        self.container.css_justify_content = 'flex-start'
        self.opened = True
        self.title = gui.Label(title, width='100%')
        self.title.add_class("Title")
        self.title.style.update({'text-indent':'25px',
            'background-image':"url('/editor_resources:minus.png')",
            'background-repeat':'no-repeat',
            'background-position':'5px',
            'border-top':'3px solid lightgray'})
        self.title.onclick.do(self.openClose)
        super(EditorAttributesGroup, self).append(self.title)
        super(EditorAttributesGroup, self).append(self.container)

    def openClose(self, widget):
        self.opened = not self.opened
        backgroundImage = "url('/editor_resources:minus.png')" if self.opened else "url('/editor_resources:plus.png')"
        self.title.style['background-image'] = backgroundImage
        self.container.css_display = 'flex' if self.opened else 'none'
        
    def append(self, widget, key=''):
        return self.container.append(widget, key)
    
    def remove_child(self, widget):
        return self.container.remove_child(widget)


class EditorAttributes(gui.VBox):
    """ Contains EditorAttributeInput each one of which notify a new value with an event
    """
    def __init__(self, appInstance, **kwargs):
        super(EditorAttributes, self).__init__(**kwargs)
        self.appInstance = appInstance
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

        self.group_orders = {'Generic':'2', 'WidgetSpecific':'3', 'Geometry':'34', 'Background':'5' }

        self.attributesInputs = list()
        #load editable attributes
        self.append(self.titleLabel)
        self.attributeGroups = {}

    def set_widget(self, widget):
        self.infoLabel.set_text("Selected widget: %s"%widget.identifier)
        self.attributes['selected_widget_id'] = widget.identifier

        for w in self.attributeGroups.values():
            self.remove_child(w)

        for w in self.attributesInputs:
            if w.attributeDict['group'] in self.attributeGroups:
                self.attributeGroups[w.attributeDict['group']].remove_child(w)

        self.targetWidget = widget

        index = 100
        default_width = "100%"
        default_height = "22px"
        for x, y in inspect.getmembers(self.targetWidget.__class__):
            if type(y)==property:
                if hasattr(y,"fget"):
                    if hasattr(y.fget, "editor_attributes"):
                        group = y.fget.editor_attributes['group']

                        attributeEditor = None
                        attributeDict = y.fget.editor_attributes
                        #'background-repeat':{'type':str, 'description':'The repeat behaviour of an optional background image', ,'additional_data':{'possible_values':'repeat | repeat-x | repeat-y | no-repeat | inherit'}},
                        if attributeDict['type'] in (bool,int,float,gui.ColorPicker.__name__,gui.DropDown.__name__,'url_editor','css_size','base64_image','file'):
                            if attributeDict['type'] == bool:
                                chk = gui.CheckBox('checked', width=default_width, height=default_height)
                                attributeEditor = EditorAttributeInputGeneric(chk, self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == int:
                                spin = gui.SpinBox(attributeDict['additional_data']['default'], attributeDict['additional_data']['min'], attributeDict['additional_data']['max'], attributeDict['additional_data']['step'], width=default_width, height=default_height)
                                attributeEditor = EditorAttributeInputInt(spin, self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == float:
                                spin = gui.SpinBox(attributeDict['additional_data']['default'], attributeDict['additional_data']['min'], attributeDict['additional_data']['max'], attributeDict['additional_data']['step'], width=default_width, height=default_height)
                                attributeEditor = EditorAttributeInputFloat(spin, self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == gui.ColorPicker.__name__:
                                attributeEditor = EditorAttributeInputColor(self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == gui.DropDown.__name__:
                                drop = gui.DropDown(width=default_width, height=default_height)
                                for value in attributeDict['additional_data']['possible_values']:
                                    drop.append(gui.DropDownItem(value),value)
                                attributeEditor = EditorAttributeInputGeneric(drop, self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == 'url_editor':
                                attributeEditor = EditorAttributeInputUrl(self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == 'base64_image':
                                attributeEditor = EditorAttributeInputBase64Image(self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == 'css_size':
                                attributeEditor = EditorAttributeInputCssSize(self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)
                            elif attributeDict['type'] == 'file':
                                attributeEditor = EditorAttributeInputFile(self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)

                        else: #default editor is string
                            txt = gui.TextInput(width=default_width, height=default_height)
                            attributeEditor = EditorAttributeInputGeneric(txt, self.targetWidget, x, y, y.fget.editor_attributes, self.appInstance)

                        if not group in self.attributeGroups.keys():
                            groupContainer = EditorAttributesGroup(group, width='100%')
                            groupContainer.css_order = self.group_orders.get(group, str(index))
                            index = index + 1
                            self.attributeGroups[group] = groupContainer

                        if getattr(self.targetWidget, x) is None:
                            attributeEditor.set_valid(False)
                        else:
                            attributeEditor.set_value(getattr(self.targetWidget, x))
                        self.attributeGroups[group].append(attributeEditor)
                        self.attributesInputs.append(attributeEditor)

        for w in self.attributeGroups.values():
            self.append(w)


#widget that allows to edit a specific html and css attributes
#   it has a descriptive label, an edit widget (TextInput, SpinBox..) based on the 'type' and a title
class EditorAttributeInputBase(gui.GridBox):
    """ propertyDef is the property of the class
    """
    targetWidget = None     #wodget
    propertyDef = None      #property
    attributeName = ''
    attributeDict = {}
    appInstance = None
    removeAttribute = None  #widget
    label = None            #widget

    def __init__(self, widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs):
        _style = {'display':'block',
            'overflow':'hidden',
            'margin':'2px',
            'outline':'1px solid lightgray',
            'width':'100%'}
        if 'style' in kwargs.keys():
            kwargs['style'].update(_style)
        else:
            kwargs['style'] = _style
        
        super(EditorAttributeInputBase, self).__init__(*args, **kwargs)
        
        self.targetWidget = widget
        self.propertyDef = propertyDef
        self.attributeName = attributeName
        self.attributeDict = attributeDict
        self.appInstance = appInstance
        self.removeAttribute = gui.Image('/editor_resources:delete.png', width='10px')
        self.removeAttribute.attributes['title'] = 'Remove attribute from this widget.'
        self.removeAttribute.onclick.do(self.on_attribute_remove)

        self.label = gui.Label(attributeName, width='100%', height="100%", style={'overflow':'hidden', 'font-size':'13px', 'margin':'0px'})
        self.label.attributes['title'] = attributeDict['description']
        self.append({'del':self.removeAttribute, 'lbl':self.label})

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
        self.propertyDef.fset(self.targetWidget, None)
        return (self.targetWidget, self.attributeName)

    def set_value(self, value):
        self.set_valid(not value is None)
        self.inputWidget.set_value(value)

    def on_attribute_changed(self, widget, value):
        self.set_valid()
        setattr(self.targetWidget, self.attributeName, value)


class EditorAttributeInputGeneric(EditorAttributeInputBase):
    inputWidget = None

    def __init__(self, inputWidget, widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs):
        super(EditorAttributeInputGeneric, self).__init__(widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs)
        self.inputWidget = inputWidget
        self.inputWidget.onchange.do(self.on_attribute_changed)
        self.inputWidget.attributes['title'] = attributeDict['description']

        '''
        self.set_from_asciiart("""
            |del|lbl                   |input                  |
            """)
        '''
        self.style.update({'grid-template-columns':"6% 46% 48%", 'grid-template-rows':"100%", 'grid-template-areas':"'del lbl input'"})
        self.append({'del':self.removeAttribute, 'lbl':self.label, 'input':self.inputWidget})


class EditorAttributeInputFloat(EditorAttributeInputGeneric):
    def on_attribute_changed(self, emitter, value):
        super(EditorAttributeInputFloat, self).on_attribute_changed(self, float(value))


class EditorAttributeInputInt(EditorAttributeInputGeneric):
    def on_attribute_changed(self, emitter, value):
        super(EditorAttributeInputInt, self).on_attribute_changed(self, int(float(value)))


class EditorAttributeInputCssSize(EditorAttributeInputBase):
    def __init__(self, widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs):
        super(EditorAttributeInputCssSize, self).__init__(widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs)
        self.numInput = gui.SpinBox('0',-999999999, 999999999, 1, width='100%', height='100%')
        self.numInput.onchange.do(self.onchange)
        self.numInput.style['text-align'] = 'right'

        self.dropMeasureUnit = gui.DropDown(width='100%', height='100%')
        self.dropMeasureUnit.append( gui.DropDownItem('px'), 'px' )
        self.dropMeasureUnit.append( gui.DropDownItem('%'), '%' )
        self.dropMeasureUnit.select_by_key('px')
        self.dropMeasureUnit.onchange.do(self.onchange)
        '''
        self.set_from_asciiart("""
            |del|lbl                   |input           |meas   |
            """)
        '''
        self.style.update({'grid-template-columns':"6% 46% 33% 15%", 'grid-template-rows':"100%", 'grid-template-areas':"'del lbl input meas'"})
        self.append({'del':self.removeAttribute, 'lbl':self.label, 'input':self.numInput, 'meas':self.dropMeasureUnit})

    def onchange(self, widget, new_value):
        new_size = str(self.numInput.get_value()) + str(self.dropMeasureUnit.get_value())
        self.on_attribute_changed(self, new_size)

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
        self.set_valid(not value is None)


class EditorAttributeInputColor(EditorAttributeInputBase):
    def __init__(self, widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs):
        super(EditorAttributeInputColor, self).__init__(widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs)
        self.css_height = "60px"
        self.spin_red = gui.SpinBox(0, 0, 255, 1, width="100%", height="100%")
        self.spin_green = gui.SpinBox(0, 0, 255, 1, width="100%", height="100%")
        self.spin_blue = gui.SpinBox(0, 0, 255, 1, width="100%", height="100%")
        self.slide_red = gui.Slider(0, 0, 255, 1, width="100%", height="100%", style={'background-color':'pink'})
        self.slide_green = gui.Slider(0, 0, 255, 1, width="100%", height="100%", style={'background-color':'lightgreen'})
        self.slide_blue = gui.Slider(0, 0, 255, 1, width="100%", height="100%", style={'background-color':'lightblue'})
        '''
        self.set_from_asciiart("""
            |del|lbl                   |spin_r  |spin_g  |spin_b  |
            |del|lbl                   |slide_r |slide_g |slide_b |
            """)
        '''
        self.style.update({'grid-template-columns':"6% 46% 16% 16% 16%", 'grid-template-rows':"50% 50%", 'grid-template-areas':"'del lbl spin_r spin_g spin_b' 'del lbl slide_r slide_g slide_b'"})
        self.append({'del':self.removeAttribute, 'lbl':self.label, 'spin_r':self.spin_red, 'spin_g':self.spin_green, 'spin_b':self.spin_blue, 'slide_r':self.slide_red, 'slide_g':self.slide_green, 'slide_b':self.slide_blue})

        self.slide_red.onchange.do(self.onchange)
        self.slide_green.onchange.do(self.onchange)
        self.slide_blue.onchange.do(self.onchange)

        self.spin_red.onchange.do(self.onchange)
        self.spin_green.onchange.do(self.onchange)
        self.spin_blue.onchange.do(self.onchange)

    def to_str(self):
        return "rgb(%s,%s,%s)"%(self.slide_red.get_value(), self.slide_green.get_value(), self.slide_blue.get_value())

    def from_str(self, value_str):
        print("color:", value_str)
        components = []
        if value_str is None or '(' not in value_str or ')' not in value_str:
            components = [0,0,0]
        else:
            components = value_str[value_str.index('(')+1:value_str.index(')')].split(',')
        if len(components)<3:
            components = [0,0,0]
        self.slide_red.set_value(components[0])
        self.slide_green.set_value(components[1])
        self.slide_blue.set_value(components[2])
        
        self.spin_red.set_value(self.slide_red.get_value())
        self.spin_green.set_value(self.slide_green.get_value())
        self.spin_blue.set_value(self.slide_blue.get_value())

    @gui.decorate_event
    def onchange(self, widget, new_value):
        if type(widget) == gui.SpinBox:
            self.slide_red.set_value(self.spin_red.get_value())
            self.slide_green.set_value(self.spin_green.get_value())
            self.slide_blue.set_value(self.spin_blue.get_value())
        else:
            self.spin_red.set_value(self.slide_red.get_value())
            self.spin_green.set_value(self.slide_green.get_value())
            self.spin_blue.set_value(self.slide_blue.get_value())
        print("color changed")
        self.set_valid()
        setattr(self.targetWidget, self.attributeName, self.to_str())

    def set_value(self, value):
        self.from_str(value)
        self.set_valid(not value is None)


class EditorAttributeInputUrl(EditorAttributeInputBase):
    inputWidget = None

    def __init__(self, widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs):
        super(EditorAttributeInputUrl, self).__init__(widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs)
        self.inputWidget = gui.TextInput(width="100%", height="100%")
        self.inputWidget.onchange.do(self.on_attribute_changed)
        self.inputWidget.attributes['title'] = attributeDict['description']

        self.btFileFolderSelection = gui.Widget(width='100%', height='100%')
        self.btFileFolderSelection.style.update({'background-repeat':'no-repeat',
            'background-image':"url('/res:folder.png')",
            'background-color':'transparent'})
        self.btFileFolderSelection.onclick.do(self.on_file_selection_bt_pressed)
        '''
        self.set_from_asciiart("""
            |del|lbl                   |input                |bt|
            """)
        '''
        self.style.update({'grid-template-columns':"6% 46% 33% 15%", 'grid-template-rows':"100%", 'grid-template-areas':"'del lbl input bt'"})
        self.append({'del':self.removeAttribute, 'lbl':self.label, 'input':self.inputWidget, 'bt':self.btFileFolderSelection})

    def on_file_selection_bt_pressed(self, widget):
        self.selectionDialog = gui.FileSelectionDialog('Select a file', '', False, './', True, False)
        self.selectionDialog.confirm_value.do(self.file_dialog_confirmed)
        self.selectionDialog.show(self.appInstance)

    def file_dialog_confirmed(self, widget, fileList):
        if len(fileList)>0:
            self.inputWidget.set_value("url('/editor_resources:" + fileList[0].split('/')[-1].split('\\')[-1] + "')")
            return self.on_attribute_changed(None, self.inputWidget.get_value())

    def set_value(self, value):
        self.inputWidget.set_value(value)
        self.set_valid(not value is None)


class EditorAttributeInputBase64Image(EditorAttributeInputUrl):
    def __init__(self, widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs):
        super(EditorAttributeInputBase64Image, self).__init__(widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs)

    def file_dialog_confirmed(self, widget, fileList):
        if len(fileList)>0:
            self.inputWidget.set_value(gui.load_resource(fileList[0]))
            return self.on_attribute_changed(None, self.inputWidget.get_value())


class EditorAttributeInputFile(EditorAttributeInputUrl):
    def __init__(self, widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs):
        super(EditorAttributeInputFile, self).__init__(widget, attributeName, propertyDef, attributeDict, appInstance, *args, **kwargs)

    def file_dialog_confirmed(self, widget, fileList):
        if len(fileList)>0:
            self.inputWidget.set_value(fileList[0].replace("\\","/"))
            return self.on_attribute_changed(None, self.inputWidget.get_value())


