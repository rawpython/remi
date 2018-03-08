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
import html_helper


class ResizeHelper(gui.Widget):
    def __init__(self, project, **kwargs):
        super(ResizeHelper, self).__init__(**kwargs)

        self.style['float'] = 'none'
        self.style['background-image'] = "url('/res/resize.png')"
        self.style['background-color'] = "rgba(255,255,255,0.0)"
        self.style['position'] = 'absolute'
        self.style['left']='0px'
        self.style['top']='0px'
        self.project = project

        self.parent = None
        self.refWidget = None
        self.active = False
        self.set_on_mousedown_listener(self.start_drag)

        self.origin_x = -1
        self.origin_y = -1
        
    def setup(self, refWidget, newParent):
        #refWidget is the target widget that will be resized
        #newParent is the container
        if self.parent:
            try:
                self.parent.remove_child(self)
            except:
                #there was no ResizeHelper placed
                pass
        if newParent==None:
            return
        self.parent = newParent
        self.refWidget = refWidget
        
        self.static_positioning = False
        if 'position' in self.refWidget.style:
            if self.refWidget.style['position'] != 'absolute':
                self.static_positioning = True

        if self.static_positioning:
            return

        try:
            self.parent.append(self)
        except:
            #the selected widget's parent can't contain a ResizeHelper
            pass
        #self.refWidget.style['position'] = 'relative'
        self.update_position()
            
    def start_drag(self, emitter, x, y):
        self.active = True
        self.project.set_on_mousemove_listener(self.on_drag)
        self.project.set_on_mouseup_listener(self.stop_drag)
        self.project.set_on_mouseleave_listener(self.stop_drag, 0, 0)
        self.origin_x = -1
        self.origin_y = -1

    def stop_drag(self, emitter, x, y):
        self.active = False
        self.update_position()

    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = int(x)
                self.origin_y = int(y)
                self.refWidget_origin_w = gui.from_pix(self.refWidget.style['width'])
                self.refWidget_origin_h = gui.from_pix(self.refWidget.style['height'])
            else:
                self.refWidget.style['width'] = gui.to_pix(self.refWidget_origin_w + int(x) - self.origin_x )
                self.refWidget.style['height'] = gui.to_pix(self.refWidget_origin_h + int(y) - self.origin_y)
                self.update_position()

    def update_position(self):
        self.style['position']='absolute'
        if self.refWidget:
            if 'left' in self.refWidget.style and 'top' in self.refWidget.style:
                self.style['left']=gui.to_pix(gui.from_pix(self.refWidget.style['left']) + gui.from_pix(self.refWidget.style['width']) - gui.from_pix(self.style['width'])/2)
                self.style['top']=gui.to_pix(gui.from_pix(self.refWidget.style['top']) + gui.from_pix(self.refWidget.style['height']) - gui.from_pix(self.style['height'])/2)


class DragHelper(gui.Widget):
    def __init__(self, project, **kwargs):
        super(DragHelper, self).__init__(**kwargs)

        self.style['float'] = 'none'
        self.style['background-image'] = "url('/res/drag.png')"
        self.style['background-color'] = "rgba(255,255,255,0.0)"
        self.style['position'] = 'absolute'
        self.style['left']='0px'
        self.style['top']='0px'
        
        self.project = project

        self.parent = None
        self.refWidget = None
        self.active = False
        self.set_on_mousedown_listener(self.start_drag)

        self.origin_x = -1
        self.origin_y = -1
        
    def setup(self, refWidget, newParent):
        #refWidget is the target widget that will be resized
        #newParent is the container
        if self.parent:
            try:
                self.parent.remove_child(self)
            except:
                #there was no ResizeHelper placed
                pass
        if newParent==None:
            return
        self.parent = newParent
        self.refWidget = refWidget
        
        self.static_positioning = False
        if 'position' in self.refWidget.style:
            if self.refWidget.style['position'] != 'absolute':
                self.static_positioning = True

        if self.static_positioning:
            return

        try:
            self.parent.append(self)
        except:
            #the selected widget's parent can't contain a ResizeHelper
            pass
        #self.refWidget.style['position'] = 'relative'
        self.update_position()
            
    def start_drag(self, emitter, x, y):
        self.active = True
        self.project.set_on_mousemove_listener(self.on_drag)
        self.project.set_on_mouseup_listener(self.stop_drag)
        self.project.set_on_mouseleave_listener(self.stop_drag, 0, 0)
        self.origin_x = -1
        self.origin_y = -1
    
    def stop_drag(self, emitter, x, y):
        self.active = False
        self.update_position()

    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = int(x)
                self.origin_y = int(y)
                self.refWidget_origin_x = gui.from_pix(self.refWidget.style['left'])
                self.refWidget_origin_y = gui.from_pix(self.refWidget.style['top'])
            else:
                self.refWidget.style['left'] = gui.to_pix(self.refWidget_origin_x + int(x) - self.origin_x )
                self.refWidget.style['top'] = gui.to_pix(self.refWidget_origin_y + int(y) - self.origin_y)
                self.update_position()

    def update_position(self):
        self.style['position']='absolute'
        if self.refWidget:
            if 'left' in self.refWidget.style and 'top' in self.refWidget.style:
                self.style['left']=gui.to_pix(gui.from_pix(self.refWidget.style['left']))
                self.style['top']=gui.to_pix(gui.from_pix(self.refWidget.style['top']))


class Project(gui.Widget):
    """ The editor project is pure html with specific tag attributes
        This class loads and save the project file, 
        and also compiles a project in python code.
    """
    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)
    
        self.style.update({'position':'relative',
            'overflow':'auto',
            'background-color':'rgb(250,248,240)',
            'background-image':"url('/res/background.png')"})
    
    def new(self):
        #remove the main widget
        pass
            
    def load(self, ifile, configuration):
        self.ifile = ifile
        
        _module = imp.load_source('project', self.ifile) #imp.load_source('module.name', '/path/to/file.py')
        
        configuration.configDict = _module.configuration
        
        #finding App class
        clsmembers = inspect.getmembers(_module, inspect.isclass)
        
        app_init_fnc = None
        for (name, value) in clsmembers:
            if issubclass(value,App) and name!='App':
                app_init_fnc = value
                
        if app_init_fnc==None:
            return None

        members_list = inspect.getmembers(app_init_fnc(editing_mode=True), inspect.ismethod)
        #print(members_list)
        for (name, member) in members_list:
            #print("SETTING MEMBER: " + name)
            setattr(self, name, self.fakeListenerFunc)
        return app_init_fnc.construct_ui(self)

    def fakeListenerFunc(*args):
        pass
        
    def check_pending_listeners(self, widget, widgetVarName, force=False):
        code_nested_listener = ''
        #checking if pending listeners code production can be solved
        for event in self.pending_listener_registration:
            #print("widget: %s   source:%s    listener:%s"%(str(id(widget)),event['eventsource'].path_to_this_widget,event['eventlistener'].path_to_this_widget))
            if force or (hasattr(event['eventsource'],'path_to_this_widget') and hasattr(event['eventlistener'],'path_to_this_widget')):
                if (force or (widget.attributes['editor_varname'] in event['eventsource'].path_to_this_widget and widget.attributes['editor_varname'] in event['eventlistener'].path_to_this_widget)) and event['done']==False:
                    #this means that this is the root node from where the leafs(listener and source) departs, hre can be set the listener
                    event['done'] = True
                    
                    if not hasattr(event['eventlistener'],'path_to_this_widget'):
                        event['eventlistener'].path_to_this_widget = []
                    
                    source_filtered_path=event['eventsource'].path_to_this_widget[:]
                    listener_filtered_path=event['eventlistener'].path_to_this_widget[:]
                    for v in widget.path_to_this_widget:
                        #if v in source_filtered_path:
                        source_filtered_path.remove(v)
                        listener_filtered_path.remove(v)
                    #event['eventsource'].path_to_this_widget = source_filtered_path
                    #event['eventlistener'].path_to_this_widget = listener_filtered_path

                    sourcename = widgetVarName
                    if len(source_filtered_path)>0:
                        if len(source_filtered_path)>1:
                            sourcename = "%s.children['"%self.children['root'].attributes['editor_varname'] + "'].children['".join(source_filtered_path) + "']"
                        else:
                            sourcename = event['eventsource'].attributes['editor_varname']
                    if force==True:
                        if self.children['root'].attributes['editor_varname'] in source_filtered_path:
                            source_filtered_path.remove(self.children['root'].attributes['editor_varname'])
                        sourcename = self.children['root'].attributes['editor_varname']
                        if len(source_filtered_path)>0:
                            sourcename = ("%s.children['" + "'].children['".join(source_filtered_path) + "']")%self.children['root'].attributes['editor_varname']

                    listenername = "self"
                    if len(listener_filtered_path)>0:
                        if len(listener_filtered_path)>1:
                            listenername = "%s.children['"%self.children['root'].attributes['editor_varname'] + "'].children['".join(listener_filtered_path) + "']"
                        else:
                            listenername = event['eventlistener'].attributes['editor_varname']
                    if force==True:
                        if self.children['root'].attributes['editor_varname'] in listener_filtered_path:
                            listener_filtered_path.remove(self.children['root'].attributes['editor_varname'])
                        listenername = self.children['root'].attributes['editor_varname']
                        if len(listener_filtered_path)>0:
                            listenername = ("%s.children['" + "'].children['".join(listener_filtered_path) + "']")%self.children['root'].attributes['editor_varname']
                    if event['eventlistener'] == widget:
                        listenername = widgetVarName
                    code_nested_listener += prototypes.proto_set_listener%{'sourcename':sourcename, 
                                                'register_function':  event['setoneventfuncname'],
                                                'listenername': listenername,
                                                'listener_function': event['listenerfuncname']}                
                    if not event['eventlistener'].identifier in self.code_declared_classes:
                        self.code_declared_classes[event['eventlistener'].identifier] = ''
                    self.code_declared_classes[event['eventlistener'].identifier] += event['listenerClassFunction']
        return code_nested_listener
    
    def repr_widget_for_editor(self, widget): #widgetVarName is the name with which the parent calls this instance
        if not widget in self.known_project_children:
            widget.path_to_this_widget = []
        self.known_project_children.append(widget)
        if hasattr(widget, 'path_to_this_widget'):
            widget.path_to_this_widget.append( widget.attributes['editor_varname'] )
        else:
            widget.path_to_this_widget = []
        
        print(widget.attributes['editor_varname'])
        
        code_nested = '' #the code strings to return
        
        if not hasattr( widget, 'attributes' ):
            return '' #no nested code
            
        widgetVarName = widget.attributes['editor_varname']
        newClass = widget.attributes['editor_newclass'] == 'True'
        classname =  'CLASS' + widgetVarName if newClass else widget.__class__.__name__
        
        code_nested = prototypes.proto_widget_allocation%{'varname': widgetVarName, 'classname': classname, 'editor_constructor': widget.attributes['editor_constructor'], 'editor_instance_id':widget.identifier}
        
        for key in widget.attributes.keys():
            if key not in html_helper.htmlInternallyUsedTags:
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
                    listener = widget.eventManager.listeners[registered_event_name]['callback'].__self__
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
                #children_code_nested += prototypes.proto_layout_append%{'parentname':widgetVarName,'varname':"'%s'"%child}
                continue
            if 'editor_varname' not in child.attributes.keys():
                continue
            child.path_to_this_widget = widget.path_to_this_widget[:]
            children_code_nested += self.repr_widget_for_editor(child)
            children_code_nested += prototypes.proto_layout_append%{'parentname':widgetVarName,'varname':"%s,'%s'"%(child.attributes['editor_varname'],child.attributes['editor_varname'])}
        
        children_code_nested += self.check_pending_listeners(widget, widgetVarName)        
                        
        if newClass:# and not (classname in self.code_declared_classes.keys()):
            if not widget.identifier in self.code_declared_classes:
                self.code_declared_classes[widget.identifier] = ''
            self.code_declared_classes[widget.identifier] = prototypes.proto_code_class%{'classname': classname, 'superclassname': widget.attributes['editor_baseclass'],
                                                        'nested_code': children_code_nested } + self.code_declared_classes[widget.identifier]
        else:
            code_nested = code_nested + children_code_nested
        
        return code_nested

    def save(self, save_path_filename, configuration): 
        self.code_declared_classes = {}
        self.pending_listener_registration = list()
        self.known_project_children = [self,] #a list containing widgets that have been parsed and that are considered valid listeners 
        self.pending_signals_to_connect = list() #a list containing dicts {listener, emitter, register_function, listener_function}
        compiled_code = ''
        code_classes = ''
        
        #self.children['root'].path_to_this_widget = []
        ret = self.repr_widget_for_editor( self.children['root'] )
        self.path_to_this_widget = []
        code_nested = ret + self.check_pending_listeners(self,'self',True)# + self.code_listener_registration[str(id(self))]
        main_code_class = prototypes.proto_code_main_class%{'classname':configuration.configDict[configuration.KEY_PRJ_NAME],
                                                        'config_resourcepath':configuration.configDict[configuration.KEY_RESOURCEPATH],
                                                        'code_nested':code_nested, 
                                                        'mainwidgetname':self.children['root'].attributes['editor_varname']}

        if self.identifier in self.code_declared_classes.keys():
            main_code_class += self.code_declared_classes[self.identifier]
            del self.code_declared_classes[self.identifier]
            
        for key in self.code_declared_classes.keys():
            code_class = self.code_declared_classes[key]
            code_listener_setting = ''
            code_classes += code_class
        
        code_classes += main_code_class
        compiled_code = prototypes.proto_code_program%{ 'code_classes':code_classes,
                                                        'classname':configuration.configDict[configuration.KEY_PRJ_NAME],
                                                        'configuration':configuration.configDict
                                                       }
        
        print(compiled_code)
        
        if save_path_filename!=None:
            f = open(save_path_filename, "w")
            f.write(compiled_code)
            f.close()
        
        
class Editor(App):
    def __init__(self, *args):
        editor_res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(Editor, self).__init__(*args, static_file_path=editor_res_path)

    def idle(self):
        self.resizeHelper.update_position()
        self.dragHelper.update_position()

    def main(self):
        self.mainContainer = gui.Widget(width='100%', height='100%', layout_orientation=gui.Widget.LAYOUT_VERTICAL)
        self.mainContainer.style['background-color'] = 'white'
        self.mainContainer.style['border'] = 'none'
        
        menubar = gui.MenuBar(height='4%')
        menu = gui.Menu(width='100%',height='100%')
        menu.style['z-index'] = '1'
        m1 = gui.MenuItem('File', width=150, height='100%')
        m10 = gui.MenuItem('New', width=150, height=30)
        m11 = gui.MenuItem('Open', width=150, height=30)
        m12 = gui.MenuItem('Save Your App', width=150, height=30)
        #m12.style['visibility'] = 'hidden'
        m121 = gui.MenuItem('Save', width=100, height=30)
        m122 = gui.MenuItem('Save as', width=100, height=30)
        m1.append([m10, m11, m12])
        m12.append([m121, m122])
        
        m2 = gui.MenuItem('Edit', width=100, height='100%')
        m21 = gui.MenuItem('Cut', width=100, height=30)
        m22 = gui.MenuItem('Paste', width=100, height=30)
        m2.append([m21, m22])
        
        m3 = gui.MenuItem('Project Config', width=200, height='100%')
        
        menu.append([m1, m2, m3])
        
        menubar.append(menu)
        
        self.toolbar = editor_widgets.ToolBar(width='100%', height='30px', margin='0px 0px')
        self.toolbar.style['border-bottom'] = '1px solid rgba(0,0,0,.12)'
        self.toolbar.add_command('/res/delete.png', self.toolbar_delete_clicked, 'Delete Widget')
        self.toolbar.add_command('/res/cut.png', self.menu_cut_selection_clicked, 'Cut Widget')
        self.toolbar.add_command('/res/paste.png', self.menu_paste_selection_clicked, 'Paste Widget')
        
        self.fileOpenDialog = editor_widgets.EditorFileSelectionDialog('Open Project', 'Select the project file.<br>It have to be a python program created with this editor.', False, '.', True, False, self)
        self.fileOpenDialog.set_on_confirm_value_listener(self.on_open_dialog_confirm)
        
        self.fileSaveAsDialog = editor_widgets.EditorFileSaveDialog('Project Save', 'Select the project folder and type a filename', False, '.', False, True, self)
        self.fileSaveAsDialog.add_fileinput_field('untitled.py')
        self.fileSaveAsDialog.set_on_confirm_value_listener(self.on_saveas_dialog_confirm)        

        m10.set_on_click_listener(self.menu_new_clicked)
        m11.set_on_click_listener(self.fileOpenDialog.show)
        m121.set_on_click_listener(self.menu_save_clicked)
        m122.set_on_click_listener(self.fileSaveAsDialog.show)
        m21.set_on_click_listener(self.menu_cut_selection_clicked)
        m22.set_on_click_listener(self.menu_paste_selection_clicked)
        
        m3.set_on_click_listener(self.menu_project_config_clicked)
        
        self.subContainer = gui.HBox(width='100%', height='96%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL)
        self.subContainer.style.update({'position':'relative',
            'overflow':'auto',
            'align-items':'stretch'})
                
        #here are contained the widgets
        self.widgetsCollection = editor_widgets.WidgetCollection(self, width='100%', height='50%')
        
        self.project = Project(width='100%', height='100%')
        self.project.style['min-height'] = '400px'
        
        self.project.attributes['ondragover'] = "event.preventDefault();"
        self.EVENT_ONDROPPPED = "on_dropped"
        self.project.attributes['ondrop'] = """event.preventDefault();
                var data = JSON.parse(event.dataTransfer.getData('application/json'));
                var params={};
                if( data[0] == 'resize'){
                    document.getElementById(data[1]).style.left = parseInt(document.getElementById(data[1]).style.left) + event.clientX - data[2] + 'px';
                    document.getElementById(data[1]).style.top = parseInt(document.getElementById(data[1]).style.top) + event.clientY - data[3] + 'px';
                    params['left']=document.getElementById(data[1]).style.left;
                    params['top']=document.getElementById(data[1]).style.top;
                }
                if( data[0] == 'add'){
                    params['left']=event.clientX-event.currentTarget.getBoundingClientRect().left;
                    params['top']=event.clientY-event.currentTarget.getBoundingClientRect().top;
                }
                if( data[0] == 'move'){
                    document.getElementById(data[1]).style.left = parseInt(document.getElementById(data[1]).style.left) + event.clientX - data[2] + 'px';
                    document.getElementById(data[1]).style.top = parseInt(document.getElementById(data[1]).style.top) + event.clientY - data[3] + 'px';
                    params['left']=document.getElementById(data[1]).style.left;
                    params['top']=document.getElementById(data[1]).style.top;
                }
                
                sendCallbackParam(data[1],'%(evt)s',params);
                
                return false;""" % {'evt':self.EVENT_ONDROPPPED}
        self.project.attributes['editor_varname'] = 'App'
        self.project.attributes[self.project.EVENT_ONKEYDOWN] = """
                var params={};
                params['keypressed']=event.keyCode;
                sendCallbackParam('%(id)s','%(evt)s',params);
                if(event.keyCode==46){
                    return false;
                }
            """ % {'id':str(id(self)), 'evt':self.project.EVENT_ONKEYDOWN}
        
        self.projectConfiguration = editor_widgets.ProjectConfigurationDialog('Project Configuration', 'Write here the configuration for your project.')
        
        self.attributeEditor = editor_widgets.EditorAttributes(self, width='100%')
        self.attributeEditor.style['overflow'] = 'hide'
        self.signalConnectionManager = editor_widgets.SignalConnectionManager(width='100%', height='50%')
        
        self.mainContainer.append([menubar, self.subContainer])
        
        self.subContainerLeft = gui.Widget(width='20%', height='100%')
        self.subContainerLeft.style['position'] = 'relative'
        self.subContainerLeft.style['left'] = '0px'
        self.subContainerLeft.append([self.widgetsCollection, self.signalConnectionManager])
        self.subContainerLeft.add_class('RaisedFrame')
        
        self.centralContainer = gui.VBox(width='56%', height='100%')
        self.centralContainer.append([self.toolbar, self.project])
        
        self.subContainerRight = gui.Widget(width='24%', height='100%')
        self.subContainerRight.style.update({'position':'absolute', 'right':'0px', 'overflow':'scroll'})
        self.subContainerRight.add_class('RaisedFrame')
        
        self.instancesWidget = editor_widgets.InstancesWidget(width='100%')
        self.instancesWidget.treeView.set_on_change_listener(self.on_instances_widget_selection)
        
        self.subContainerRight.append([self.instancesWidget, self.attributeEditor])
        
        self.subContainer.append([self.subContainerLeft, self.centralContainer, self.subContainerRight])
        self.project.style['position'] = 'relative'
        
        self.resizeHelper = ResizeHelper(self.project, width=16, height=16)
        self.dragHelper = DragHelper(self.project, width=15, height=15)
        self.menu_new_clicked(None)
        
        self.projectPathFilename = ''
        self.editCuttedWidget = None #cut operation, contains the cutted tag
        
        # returning the root widget
        return self.mainContainer
    
    def configure_widget_for_editing(self, widget):
        """ A widget have to be added to the editor, it is configured here in order to be conformant 
            to the editor
        """
        
        if not 'editor_varname' in widget.attributes:
            return
        
        #here, the standard onclick function of the widget is overridden with a custom function
        #this function redirect the onclick event to the editor App in order to manage the event
        #detecting the widget selection
        typefunc = type(widget.onclick)
        widget.onclick = typefunc(onclick_with_instance, widget)
        widget.attributes[widget.EVENT_ONCLICK] = "sendCallback('%s','%s');event.stopPropagation();event.preventDefault();" % (widget.identifier, widget.EVENT_ONCLICK)
        widget.editor = self
        
        #setup of the on_dropped function of the widget in order to manage the dragNdrop 
        widget.__class__.on_dropped = on_dropped

        #drag properties
        #widget.style['resize'] = 'both'
        widget.style['overflow'] = 'auto'
        widget.attributes['draggable'] = 'true'
        widget.attributes['ondragstart'] = """this.style.cursor='move'; event.dataTransfer.dropEffect = 'move'; event.dataTransfer.setData('application/json', JSON.stringify(['move',event.target.id,(event.clientX),(event.clientY)]));"""
        widget.attributes['ondragover'] = "event.preventDefault();"   
        widget.EVENT_ONDROPPPED = "on_dropped"
        widget.attributes['ondrop'] = """
                var data = JSON.parse(event.dataTransfer.getData('application/json'));
                var params={};
                if( data[0] == 'add'){
                    console.debug('addd---------------------------------------------');
                    sendCallback('%(id)s','%(event_click)s');
                    console.debug('dopo---------------------------------------------');
                    params['left']=event.clientX-event.currentTarget.getBoundingClientRect().left;
                    params['top']=event.clientY-event.currentTarget.getBoundingClientRect().top;
                    sendCallbackParam(data[1],'%(evt)s',params);
                    event.stopPropagation();
                    event.preventDefault();
                }
                
                
                return false;""" % {'evt':widget.EVENT_ONDROPPPED, 'id': widget.identifier, 'event_click': widget.EVENT_ONCLICK}
                
        widget.attributes['tabindex']=str(self.tabindex)
        if not 'position' in widget.style.keys():
            widget.style['position'] = 'absolute'
        if not 'left' in widget.style.keys():
            widget.style['left'] = '1px'
        if not 'top' in widget.style.keys():
            widget.style['top'] = '1px'
        self.tabindex += 1
        
    def add_widget_to_editor(self, widget, parent = None, root_tree_node = True):
        if parent == None:
            parent = self.selectedWidget
        self.configure_widget_for_editing(widget)
        key = "root" if parent==self.project else widget.identifier
        if root_tree_node:
            parent.append(widget,key)
            if self.selectedWidget == self.project:
                self.on_widget_selection( widget )
        #dcopy = widget.children.copy()
        for child in widget.children.values():
            if type(child) == str:
                continue
            self.add_widget_to_editor(child, widget, False)
        self.instancesWidget.update(self.project, self.selectedWidget)
    
    def on_instances_widget_selection(self, instancesWidgetItem, selectedWidget):
        self.on_widget_selection(selectedWidget)
    
    def on_widget_selection(self, widget):
        self.remove_box_shadow_selected_widget()
        self.selectedWidget = widget
        self.selectedWidget.style['box-shadow'] = '0 0 10px rgb(33,150,243)'
        self.signalConnectionManager.update(self.selectedWidget, self.project)
        self.attributeEditor.set_widget( self.selectedWidget )
        parent = remi.server.get_method_by_id(self.selectedWidget.attributes['data-parent-widget'])
        self.resizeHelper.setup(widget,parent)
        self.dragHelper.setup(widget,parent)
        self.instancesWidget.select(self.selectedWidget)
        print("selected widget: " + widget.identifier)
        
    def menu_new_clicked(self, widget):
        print('new project')
        self.project.new()
        self.tabindex = 0 #incremental number to allow widgets selection
        self.selectedWidget = self.project
        self.resizeHelper.setup(None, None)
        self.dragHelper.setup(None, None)
        if 'root' in self.project.children.keys():
            self.project.remove_child( self.project.children['root'] )

    def on_open_dialog_confirm(self, widget, filelist):
        if len(filelist):
            widgetTree = self.project.load(filelist[0], self.projectConfiguration)
            if widgetTree!=None:
                self.add_widget_to_editor( widgetTree )
            self.projectPathFilename = filelist[0]
        
    def menu_save_clicked(self, widget):
        #the dragHelper have to be removed
        self.resizeHelper.setup(None, None)
        self.dragHelper.setup(None, None)
        if self.projectPathFilename == '':
            self.fileSaveAsDialog.show()
        else:
            self.remove_box_shadow_selected_widget()
            self.project.save(self.projectPathFilename, self.projectConfiguration)
    
    def remove_box_shadow_selected_widget(self):
        if 'box-shadow' in self.selectedWidget.style.keys():
            del self.selectedWidget.style['box-shadow']
        
    def on_saveas_dialog_confirm(self, widget, path):
        #the resizeHelper have to be removed
        self.resizeHelper.setup(None, None)
        self.dragHelper.setup(None, None)
        if len(path):
            self.projectPathFilename = path + '/' + self.fileSaveAsDialog.get_fileinput_value()
            print("file:%s"%self.projectPathFilename)
            self.remove_box_shadow_selected_widget()
            self.project.save(self.projectPathFilename, self.projectConfiguration)
            
    def menu_cut_selection_clicked(self, widget):
        if self.selectedWidget==self.project:
            return
        self.resizeHelper.setup(None, None)
        self.dragHelper.setup(None, None)
        parent = remi.server.get_method_by_id(self.selectedWidget.attributes['data-parent-widget'])
        self.editCuttedWidget = self.selectedWidget
        parent.remove_child(self.selectedWidget)
        self.selectedWidget = parent
        self.instancesWidget.update(self.project, self.selectedWidget)
        print("tag cutted:" + self.editCuttedWidget.identifier)

    def menu_paste_selection_clicked(self, widget):
        if self.editCuttedWidget != None:
            key = "root" if self.selectedWidget==self.project else self.editCuttedWidget.identifier
            self.selectedWidget.append(self.editCuttedWidget, key)
            self.editCuttedWidget = None
            self.instancesWidget.update(self.project, self.selectedWidget)

    def menu_project_config_clicked(self, widget):
        self.projectConfiguration.show(self)

    def toolbar_delete_clicked(self, widget):
        if self.selectedWidget==self.project:
            return
        self.resizeHelper.setup(None, None)
        self.dragHelper.setup(None, None)
        parent = remi.server.get_method_by_id(self.selectedWidget.attributes['data-parent-widget'])
        parent.remove_child(self.selectedWidget)
        self.instancesWidget.update(self.project, self.selectedWidget)
        self.selectedWidget = parent
        print("tag deleted")
        
    def onkeydown(self, keypressed):
        if str(keypressed)=='46': #46 the delete keycode
            self.toolbar_delete_clicked(None)
        print("Key pressed: " + str(keypressed))

        
#function overload for widgets that have to be editable
#the normal onfocus function does not returns the widget instance
#def onfocus_with_instance(self):
#    return self.eventManager.propagate(self.EVENT_ONFOCUS, [self])
def onclick_with_instance(self):
    #return self.eventManager.propagate(self.EVENT_ON_WIDGET_SELECTION, [self])
    self.editor.on_widget_selection(self)
    
def on_dropped(self, left, top):
    if len(left)<1:
        left='0px'
    if len(top)<1:
        top='0px'
    self.style['left']=left
    self.style['top']=top

def main():
    #p = Project()
    #root = p.load('./example_project.py')
    #p.append(root, "root")
    #p.save(None)
    
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(Editor, debug=False, address='0.0.0.0', port=8082, update_interval=2.0)
    
if __name__ == "__main__":
    main()
