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
import remi.server
from remi import start, App
import imp
import inspect
import sys
import os #for path handling
import prototypes
import editor_widgets


class ResizeHelper(gui.Widget):
    def __init__(self, w, h):
        super(ResizeHelper, self).__init__(w, h)
        self.style['float'] = 'none'
        self.style['background-image'] = "url('res/resize.png')"
        self.style['position'] = 'absolute'
        self.style['left']='0px'
        self.style['top']='0px'
        self.attributes['draggable'] = 'true'
        self.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"
        self.attributes['ondragover'] = "event.preventDefault();"   
        self.attributes['ondrop'] = "event.preventDefault();return false;"
        self.parent = None
        self.refWidget = None
        
    def setup(self, refWidget, newParent):
        #refWidget is the target widget that will be resized
        #newParent is the container
        if self.parent:
            self.parent.remove_child(self)
        self.parent = newParent
        self.refWidget = refWidget
        self.parent.append(self)
        self.update_position()
            
    def on_dropped(self, left, top):
        self.refWidget.style['width'] = gui.to_pix(gui.from_pix(self.refWidget.style['width']) + gui.from_pix(left) - gui.from_pix(self.style['left']))
        self.refWidget.style['height'] = gui.to_pix(gui.from_pix(self.refWidget.style['height']) + gui.from_pix(top) - gui.from_pix(self.style['top']))
        self.update_position()
        
    def update_position(self):
        self.style['left'] = gui.to_pix(gui.from_pix(self.refWidget.style['width'])+gui.from_pix(self.refWidget.style['left'])-gui.from_pix(self.style['width']))
        self.style['top'] = gui.to_pix(gui.from_pix(self.refWidget.style['height'])+gui.from_pix(self.refWidget.style['top'])-gui.from_pix(self.style['height']))


class WidgetHelper(gui.ListItem):
    """ Allocates the Widget to which it refers, 
        interfacing to the user in order to obtain the necessary attribute values
        obtains the constructor parameters, asks for them in a dialog
        puts the values in an attribute called constructor
    """

    def __init__(self, w, h, widgetClass):
        self.widgetClass = widgetClass
        super(WidgetHelper, self).__init__(w, h, self.widgetClass.__name__)
            
    def allocate(self, appInstance):
        """ Here the widget is allocated and it is performed the setup to allow the
            selection and editing
            
            def func(a:'parameter A') -> 'return value':
            func.__annotations__ {'a': 'parameter A', 'return': 'return value'}
        """
        self.appInstance = appInstance
        self.constructor_parameters_list = self.widgetClass.__init__.__code__.co_varnames[1:] #[1:] removes the self
        param_annotation_dict = ''#self.widgetClass.__init__.__annotations__
        self.dialog = gui.GenericDialog(title=self.widgetClass.__name__, message='Fill the following parameters list')
        self.dialog.add_field_with_label('name', 'Variable name', gui.TextInput(200,30))
        for param in self.constructor_parameters_list:
            note = ''#" (%s)"%param_annotation_dict[param] if param in param_annotation_dict.keys() else ""
            self.dialog.add_field_with_label(param, param + note, gui.TextInput(200,30))
        self.dialog.add_field_with_label("editor_newclass", "Overload base class", gui.CheckBox(30,30))
        self.dialog.set_on_confirm_dialog_listener(self, "on_dialog_confirm")
        self.dialog.show(self.appInstance)
        
    def on_dialog_confirm(self):
        param_annotation_dict = ''#self.widgetClass.__init__.__annotations__
        param_values = []
        for param in self.constructor_parameters_list:
            param_values.append(self.dialog.get_field(param).get_value())
            
        print(self.constructor_parameters_list)
        print(param_values)
        #constructor = '%s(%s)'%(self.widgetClass.__name__, ','.join(map(lambda v: str(v), param_values)))
        constructor = '(%s)'%(','.join(map(lambda v: str(v), param_values)))
        #here we create and decorate the widget
        widget = self.widgetClass(*param_values)
        widget.attributes['editor_constructor'] = constructor
        widget.attributes['editor_varname'] = self.dialog.get_field('name').get_value()
        widget.attributes['editor_tag_type'] = 'widget'
        widget.attributes['editor_newclass'] = 'True' if self.dialog.get_field("editor_newclass").get_value() else 'False'
        
        #drag properties
        widget.style['position'] = 'absolute'
        widget.style['left'] = '0px'
        widget.style['top'] = '0px'
        #widget.style['resize'] = 'both'
        widget.style['overflow'] = 'auto'
        widget.attributes['draggable'] = 'true'
        widget.attributes['ondragstart'] = """this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"""
        widget.attributes['ondragover'] = "event.preventDefault();"   
        widget.attributes['ondrop'] = """event.preventDefault();return false;"""
        
        #"this.style.cursor='default';this.style['left']=(event.screenX) + 'px'; this.style['top']=(event.screenY) + 'px'; event.preventDefault();return true;"  
        
        self.appInstance.add_widget_to_editor(widget)
        

class WidgetCollection(gui.Widget):
    def __init__(self, w, h, appInstance):
        self.w = w
        self.h = h
        self.appInstance = appInstance
        super(WidgetCollection, self).__init__(w, h, gui.Widget.LAYOUT_VERTICAL, 0)
        
        self.lblTitle = gui.Label(self.w, 30, "Widgets Toolbox")
        self.listWidgets = gui.ListView(self.w, self.h-30)
        
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
        helper = WidgetHelper(self.w, 30, widgetClass)
        self.listWidgets.append( helper )
        helper.set_on_click_listener(self.appInstance, "widget_helper_clicked")


class Project(gui.Widget):
    """ The editor project is pure html with specific tag attributes
        This class loads and save the project file, 
        and also compiles a project in python code.
    """
    def __init__(self, w, h, project_name='untitled'):
        super(Project, self).__init__(w, h, True, 0)
        
        self.project_name = project_name
    
        self.style['position'] = 'relative'    
        self.style['overflow'] = 'scroll'
        self.style['background-color'] = 'gray'
        self.style['background-image'] = "url( '/res/bg.png' );"
    
    def new(self):
        #remove the main widget
        pass
            
    def load(self, ifile):
        self.ifile = ifile
        #print("project name:%s"%os.path.basename(self.ifile))
        self.project_name = os.path.basename(self.ifile).replace('.py','')
        
        _module = imp.load_source('project', self.ifile) #imp.load_source('module.name', '/path/to/file.py')
        
        #finding App class
        clsmembers = inspect.getmembers(_module, inspect.isclass)
        for (name, value) in clsmembers:
            #print(name + "    " + str(issubclass(value,App)) )
            if issubclass(value,App) and name!='App':
                #self.append( _module.load_project(), "root" )
                self.append(value.main(self), "root")
                break                                             
            
    def check_pending_listeners(self, widget, widgetVarName, force=False):
        code_nested_listener = ''
        #checking if pending listeners code production can be solved
        for event in self.pending_listener_registration:
            #print("widget: %s   source:%s    listener:%s"%(str(id(widget)),event['eventsource'].path_to_this_widget,event['eventlistener'].path_to_this_widget))
            if force or (hasattr(event['eventsource'],'path_to_this_widget') and hasattr(event['eventlistener'],'path_to_this_widget')):
                if (force or (str(id(widget)) in event['eventsource'].path_to_this_widget and str(id(widget)) in event['eventlistener'].path_to_this_widget)) and event['done']==False:
                    #this means that this is the root node from where the leafs(listener and source) departs, hre can be set the listener
                    if not event['eventsource'] in self.known_project_children or not event['eventlistener'] in self.known_project_children:
                        continue
                    event['done'] = True
                    
                    source_filtered_path=event['eventsource'].path_to_this_widget[:]
                    listener_filtered_path=event['eventlistener'].path_to_this_widget[:]
                    for v in widget.path_to_this_widget:
                        if v in source_filtered_path:
                            source_filtered_path.remove(v)
                            listener_filtered_path.remove(v)
                    event['eventsource'].path_to_this_widget = source_filtered_path
                    event['eventlistener'].path_to_this_widget = listener_filtered_path
                    
                    sourcename = "self.children['" + "'].children['".join(source_filtered_path) + "']"
                    listenername = "self.children['" + "'].children['".join(listener_filtered_path) + "']"
                    if event['eventlistener'] == widget:
                        listenername = widgetVarName
                    code_nested_listener += prototypes.proto_set_listener%{'sourcename':sourcename, 
                                                'register_function':  event['setoneventfuncname'],
                                                'listenername': listenername,
                                                'listener_function': event['listenerfuncname']}                
                    if not str(id(event['eventlistener'])) in self.code_declared_classes:
                        self.code_declared_classes[str(id(event['eventlistener']))] = ''
                    self.code_declared_classes[str(id(event['eventlistener']))] += event['listenerClassFunction']
        return code_nested_listener
        
    def repr_widget_for_editor(self, widget): #widgetVarName is the name with which the parent calls this instance
        self.known_project_children.append(widget)
        if hasattr(widget, 'path_to_this_widget'):
            widget.path_to_this_widget.append( str(id(widget)) )
        else:
            widget.path_to_this_widget = [str(id(widget)),]
        
        print(widget.attributes['editor_varname'])
        
        code_nested = '' #the code strings to return
        
        if not hasattr( widget, 'attributes' ):
            return '' #no nested code
            
        widgetVarName = widget.attributes['editor_varname']
        newClass = widget.attributes['editor_newclass'] == 'True'
        classname =  'CLASS' + widgetVarName if newClass else widget.__class__.__name__
        
        code_nested = prototypes.proto_widget_allocation%{'varname': widgetVarName, 'classname': classname, 'editor_constructor': widget.attributes['editor_constructor'], 'editor_instance_id':str(id(widget))}
        
        for key in widget.attributes.keys():
            code_nested += prototypes.proto_attribute_setup%{'varname': widgetVarName, 'attrname': key, 'attrvalue': widget.attributes[key]}
        for key in widget.style.keys():
            code_nested += prototypes.proto_style_setup%{'varname': widgetVarName, 'attrname': key, 'attrvalue': widget.style[key]}
        
        
        #for all the events of this widget
        for registered_event_name in widget.eventManager.listeners.keys():
            #for all the function of this widget
            for (setOnEventListenerFuncname,setOnEventListenerFunc) in inspect.getmembers(widget, predicate=inspect.ismethod):
                #if the member is decorated by decorate_set_on_listener and the function is referred to this event
                if hasattr(setOnEventListenerFunc, '_event_listener') and setOnEventListenerFunc._event_listener['eventName']==registered_event_name:
                    listenerPrototype = setOnEventListenerFunc._event_listener['prototype']
                    listener = widget.eventManager.listeners[registered_event_name]['instance']
                    listenerFunctionName = setOnEventListenerFunc._event_listener['eventName'] + "_" + widget.attributes['editor_varname']
                    
                    listenerClassFunction = prototypes.proto_code_function%{'funcname': listenerFunctionName,
                                                                            'parameters': listenerPrototype}
                    self.pending_listener_registration.append({'done':False,'eventsource':widget, 'eventlistener':listener,
                     'setoneventfuncname':setOnEventListenerFuncname,
                     'listenerfuncname': listenerFunctionName,
                     'listenerClassFunction':listenerClassFunction})
                    
        if newClass:
            widgetVarName = 'self'
                
        children_code_nested = ''
        for child_key in widget.children.keys():
            child = widget.children[child_key]
            if type(child)==str:
                children_code_nested += prototypes.proto_layout_append%{'parentname':widgetVarName,'varname':"'%s'"%child}
                continue
            child.path_to_this_widget = widget.path_to_this_widget[:]
            children_code_nested += self.repr_widget_for_editor(child)
            children_code_nested += prototypes.proto_layout_append%{'parentname':widgetVarName,'varname':"%s,'%s'"%(child.attributes['editor_varname'],str(id(child)))}
        
        children_code_nested += self.check_pending_listeners(widget, widgetVarName)        
                        
        if newClass:# and not (classname in self.code_declared_classes.keys()):
            if not str(id(widget)) in self.code_declared_classes:
                self.code_declared_classes[str(id(widget))] = ''
            self.code_declared_classes[str(id(widget))] = prototypes.proto_code_class%{'classname': classname, 'superclassname': widget.__class__.__name__,
                                                        'nested_code': children_code_nested } + self.code_declared_classes[str(id(widget))]
        else:
            code_nested = code_nested + children_code_nested
        
        return code_nested

    def save(self, save_path_filename): 
        self.code_resourcepath = "" #should be defined in the project configuration
        self.code_declared_classes = {}
        self.pending_listener_registration = list()
        self.known_project_children = [self,] #a list containing widgets that have been parsed and that are considered valid listeners 
        self.pending_signals_to_connect = list() #a list containing dicts {listener, emitter, register_function, listener_function}
        compiled_code = ''
        code_classes = ''
        
        ret = self.repr_widget_for_editor( self.children['root'] )
        self.path_to_this_widget = []
        code_nested = ret + self.check_pending_listeners(self,'self',True)# + self.code_listener_registration[str(id(self))]
        main_code_class = prototypes.proto_code_main_class%{'classname':self.project_name,
                                                        'code_resourcepath':self.code_resourcepath,
                                                        'code_nested':code_nested, 
                                                        'mainwidgetname':self.children['root'].attributes['editor_varname']}

        if str(id(self)) in self.code_declared_classes.keys():
            main_code_class += self.code_declared_classes[str(id(self))]
            del self.code_declared_classes[str(id(self))]
            
        for key in self.code_declared_classes.keys():
            code_class = self.code_declared_classes[key]
            code_listener_setting = ''
            code_classes += code_class
        
        code_classes += main_code_class
        compiled_code = prototypes.proto_code_program%{'code_classes':code_classes,
                                                       'classname':self.project_name}
        
        print(compiled_code)
        if save_path_filename!=None:
            f = open(save_path_filename, "w")
            f.write(compiled_code)
            f.close()
        
        
class Editor(App):
    def __init__(self, *args):
        super(Editor, self).__init__(*args,static_paths=('./res/',))

    def main(self):
        self.mainContainer = gui.Widget(970, 700, gui.Widget.LAYOUT_VERTICAL, 0)
        self.mainContainer.style['background-color'] = 'white'
        self.mainContainer.style['border'] = 'none'
        
        menu = gui.Menu(950, 30)
        m1 = gui.MenuItem(100, 30, 'File')
        m10 = gui.MenuItem(100, 30, 'New')
        m11 = gui.MenuItem(100, 30, 'Open')
        m12 = gui.MenuItem(100, 30, 'Save')
        #m12.style['visibility'] = 'hidden'
        m121 = gui.MenuItem(100, 30, 'Save')
        m122 = gui.MenuItem(100, 30, 'Save as')
        m1.append(m10)
        m1.append(m11)
        m1.append(m12)
        m12.append(m121)
        m12.append(m122)
        
        m2 = gui.MenuItem(100, 30, 'Edit')
        m21 = gui.MenuItem(100, 30, 'Cut')
        m22 = gui.MenuItem(100, 30, 'Paste')
        m2.append(m21)
        m2.append(m22)
        
        menu.append(m1)
        menu.append(m2)
        
        self.fileOpenDialog = editor_widgets.EditorFileSelectionDialog(600, 310, 'Open Project', 'Select the project file', False, '.', True, False, self)
        self.fileOpenDialog.set_on_confirm_value_listener(self, 'on_open_dialog_confirm')
        
        self.fileSaveAsDialog = editor_widgets.EditorFileSaveDialog(600, 310, 'Project Save', 'Select the project folder and type a filename', False, '.', False, True, self)
        self.fileSaveAsDialog.add_fileinput_field('untitled.py')
        self.fileSaveAsDialog.set_on_confirm_value_listener(self, 'on_saveas_dialog_confirm')        

        m10.set_on_click_listener(self, 'menu_new_clicked')
        m11.set_on_click_listener(self.fileOpenDialog, 'show')
        m121.set_on_click_listener(self, 'menu_save_clicked')
        m122.set_on_click_listener(self.fileSaveAsDialog, 'show')
        m21.set_on_click_listener(self, 'menu_cut_selection_clicked')
        m22.set_on_click_listener(self, 'menu_paste_selection_clicked')
        
        self.subContainer = gui.Widget(970, 700, gui.Widget.LAYOUT_HORIZONTAL, 5)
        self.subContainer.style['background-color'] = 'transparent'
        
        #here are contained the widgets
        self.widgetsCollection = WidgetCollection(180, 600, self)
        self.project = Project(580, 600)
        self.project.attributes['ondragover'] = "event.preventDefault();"
        
        self.EVENT_ONDROPPPED = "on_dropped"
        self.project.attributes['ondrop'] = """event.preventDefault();
                var data = JSON.parse(event.dataTransfer.getData('application/json'));
                document.getElementById(data[0]).style.left = parseInt(document.getElementById(data[0]).style.left) + event.clientX - data[1] + 'px';
                document.getElementById(data[0]).style.top = parseInt(document.getElementById(data[0]).style.top) + event.clientY - data[2] + 'px';
                
                var params={};params['left']=document.getElementById(data[0]).style.left;
                params['top']=document.getElementById(data[0]).style.top;
                sendCallbackParam(data[0],'%(evt)s',params);
                
                return false;""" % {'evt':self.EVENT_ONDROPPPED}
                
        #javascript_code = gui.Tag()
        #javascript_code.type = 'script'
        #javascript_code.attributes['type'] = 'text/javascript'
        #javascript_code.add_child('code', """
        #    var MutationObsertver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
        #    var target = document;
        #    var config = { attributes: true, childList: true, subtree: true, characterData: true };
        #    var observer = new MutationObserver(function(mutations) {
        #        var obj = document.getElementById("%(id)s");
        #        obj.scrollTop = obj.scrollHeight;
        #    });
        #    observer.observe(target, config);
        #    """ % {'id': id(self.txt),})
        ## appending a widget to another, the first argument is a string key
        #self.mainContainer.add_child('javascript',javascript_code)
        
        self.attributeEditor = editor_widgets.EditorAttributes(180, 600)
        self.attributeEditor.set_on_attribute_change_listener(self, "on_attribute_change")
        self.mainContainer.append(menu)
        self.mainContainer.append(self.subContainer)
        
        self.subContainer.append(self.widgetsCollection)
        self.subContainer.append(self.project)
        self.subContainer.append(self.attributeEditor)
        
        self.tabindex = 0 #incremental number to allow widgets selection
        
        self.selectedWidget = self.project
        
        self.resizeHelper = ResizeHelper(24, 24)
        
        self.project.new()
        
        self.projectPathFilename = ''
        self.editCuttedWidget = None #cut operation, contains the cutted tag
        
        # returning the root widget
        return self.mainContainer

    # listener function
    def widget_helper_clicked(self, helperInstance):
        helperInstance.allocate(self)
    
    def configure_widget_for_editing(self, widget):
        typefunc = type(widget.onfocus)
        #widget.onfocus = typefunc(onfocus_with_instance, widget)
        #widget.set_on_focus_listener(self, "on_widget_selection")
        widget.onclick = typefunc(onclick_with_instance, widget)
        widget.set_on_click_listener(self, "on_widget_selection")
        
        widget.__class__.on_dropped = on_dropped

        #widget.attributes['contentEditable']='true';
        widget.attributes['tabindex']=str(self.tabindex)
        self.tabindex += 1
    
    def add_widget_to_editor(self, widget):
        self.configure_widget_for_editing(widget)
        key = "root" if self.selectedWidget==self.project else str(id(widget))
        self.selectedWidget.append(widget,key)
        
    def on_attribute_change(self, attributeName, value):
        self.selectedWidget.attributes[attributeName] = value
    
    def on_widget_selection(self, widget):
        self.selectedWidget = widget
        self.attributeEditor.set_widget( self.selectedWidget )
        parent = remi.server.get_method_by(self.mainContainer, self.selectedWidget.attributes['parent_widget'])
        self.resizeHelper.setup(widget,parent)
        
    def menu_new_clicked(self):
        self.project.new()

    def on_open_dialog_confirm(self, filelist):
        if len(filelist):
            self.project.load(filelist[0])
            self.projectPathFilename = filelist[0]
        
    def menu_save_clicked(self):
        if self.projectPathFilename == '':
            self.fileSaveAsDialog.show()
        else:
            self.project.save(self.projectPathFilename)
        
    def on_saveas_dialog_confirm(self, path):
        if len(path):
            self.projectPathFilename = path + '/' + self.fileSaveAsDialog.get_fileinput_value()
            print("file:%s"%self.projectPathFilename)
            self.project.save(self.projectPathFilename)
            
    def menu_cut_selection_clicked(self):
        if self.selectedWidget==self.project:
            return
        parent = remi.server.get_method_by(self.mainContainer, self.selectedWidget.attributes['parent_widget'])
        self.editCuttedWidget = self.selectedWidget
        self.selectedWidget = parent
        parent.remove_child(self.selectedWidget)
        print("tag cutted:" + str(id(self.editCuttedWidget)))

    def menu_paste_selection_clicked(self):
        if self.editCuttedWidget != None:
            self.selectedWidget.append(self.editCuttedWidget)
            self.editCuttedWidget = None


#function overload for widgets that have to be editable
#the normal onfocus function does not returns the widget instance
#def onfocus_with_instance(self):
#    return self.eventManager.propagate(self.EVENT_ONFOCUS, [self])
def onclick_with_instance(self):
    return self.eventManager.propagate(self.EVENT_ONCLICK, [self])
    
def on_dropped(self, left, top):
    self.style['left']=left
    self.style['top']=top

if __name__ == "__main__":
    p = Project(0,0)
    p.load('./example_project.py')
    p.save(None)
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(Editor, debug=False)
