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
    def __init__(self, **kwargs):
        super(ResizeHelper, self).__init__(**kwargs)
        self.style['float'] = 'none'
        self.style['background-image'] = "url('res/resize.png')"
        self.style['background-color'] = "rgba(255,255,255,0.5)"
        self.style['position'] = 'absolute'
        self.style['left']='0px'
        self.style['top']='0px'
        self.attributes['draggable'] = 'true'
        self.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify(['resize',event.target.id,(event.clientX),(event.clientY)]));"
        self.attributes['ondragover'] = "event.preventDefault();"   
        self.attributes['ondrop'] = "event.preventDefault();return false;"
        self.parent = None
        self.refWidget = None
        
    def setup(self, refWidget, newParent):
        #refWidget is the target widget that will be resized
        #newParent is the container
        if self.parent:
            self.parent.remove_child(self)
        if newParent==None:
            return
        self.parent = newParent
        self.refWidget = refWidget
        self.parent.append(self)
        self.update_position()
            
    def on_dropped(self, left, top):
        try:
            self.refWidget.style['width'] = gui.to_pix(gui.from_pix(self.refWidget.style['width']) + gui.from_pix(left) - gui.from_pix(self.style['left']))
            self.refWidget.style['height'] = gui.to_pix(gui.from_pix(self.refWidget.style['height']) + gui.from_pix(top) - gui.from_pix(self.style['top']))
        except:
            pass
        self.update_position()
        
    def update_position(self):
        if self.refWidget == None:
            return
        if self.refWidget.style['position'] != 'absolute' or ('right' in self.refWidget.style) or ('bottom' in self.refWidget.style):
            self.style['display'] = 'none'
            return
        try:
            self.style['position'] = 'absolute'
            self.style['display'] = 'block'
            self.style['left'] = gui.to_pix(gui.from_pix(self.refWidget.style['width'])+gui.from_pix(self.refWidget.style['left'])-gui.from_pix(self.style['width'])/2)
            self.style['top'] = gui.to_pix(gui.from_pix(self.refWidget.style['height'])+gui.from_pix(self.refWidget.style['top'])-gui.from_pix(self.style['height'])/2)
        except:
            self.style['display'] = 'none'


class Project(gui.Widget):
    """ The editor project is pure html with specific tag attributes
        This class loads and save the project file, 
        and also compiles a project in python code.
    """
    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)
    
        self.style['position'] = 'relative'    
        self.style['overflow'] = 'auto'
        self.style['background-color'] = 'rgb(250,248,240)'
    
    def new(self):
        #remove the main widget
        pass
            
    def load(self, ifile, configuration):
        self.ifile = ifile
        
        _module = imp.load_source('project', self.ifile) #imp.load_source('module.name', '/path/to/file.py')
        
        configuration.configDict = _module.configuration
        
        #finding App class
        clsmembers = inspect.getmembers(_module, inspect.isclass)
        for (name, value) in clsmembers:
            if issubclass(value,App) and name!='App':
                return value.construct_ui(self)
        return None                                           
            
    def check_pending_listeners(self, widget, widgetVarName, force=False):
        code_nested_listener = ''
        #checking if pending listeners code production can be solved
        for event in self.pending_listener_registration:
            #print("widget: %s   source:%s    listener:%s"%(str(id(widget)),event['eventsource'].path_to_this_widget,event['eventlistener'].path_to_this_widget))
            if force or (hasattr(event['eventsource'],'path_to_this_widget') and hasattr(event['eventlistener'],'path_to_this_widget')):
                if (force or (widget.attributes['editor_varname'] in event['eventsource'].path_to_this_widget and widget.attributes['editor_varname'] in event['eventlistener'].path_to_this_widget)) and event['done']==False:
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

                    sourcename = widgetVarName
                    if len(source_filtered_path)>0:
                        if len(source_filtered_path)>1:
                            sourcename = "self.children['" + "'].children['".join(source_filtered_path) + "']"
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
                            listenername = "self.children['" + "'].children['".join(listener_filtered_path) + "']"
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
                    if not str(id(event['eventlistener'])) in self.code_declared_classes:
                        self.code_declared_classes[str(id(event['eventlistener']))] = ''
                    self.code_declared_classes[str(id(event['eventlistener']))] += event['listenerClassFunction']
        return code_nested_listener
        
    def repr_widget_for_editor(self, widget): #widgetVarName is the name with which the parent calls this instance
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
        
        code_nested = prototypes.proto_widget_allocation%{'varname': widgetVarName, 'classname': classname, 'editor_constructor': widget.attributes['editor_constructor'], 'editor_instance_id':str(id(widget))}
        
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
                #children_code_nested += prototypes.proto_layout_append%{'parentname':widgetVarName,'varname':"'%s'"%child}
                continue
            child.path_to_this_widget = widget.path_to_this_widget[:]
            children_code_nested += self.repr_widget_for_editor(child)
            children_code_nested += prototypes.proto_layout_append%{'parentname':widgetVarName,'varname':"%s,'%s'"%(child.attributes['editor_varname'],child.attributes['editor_varname'])}
        
        children_code_nested += self.check_pending_listeners(widget, widgetVarName)        
                        
        if newClass:# and not (classname in self.code_declared_classes.keys()):
            if not str(id(widget)) in self.code_declared_classes:
                self.code_declared_classes[str(id(widget))] = ''
            self.code_declared_classes[str(id(widget))] = prototypes.proto_code_class%{'classname': classname, 'superclassname': widget.attributes['editor_baseclass'],
                                                        'nested_code': children_code_nested } + self.code_declared_classes[str(id(widget))]
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
        
        #the root widget have to appear at the center of the screen, regardless of the user positioning
        _position = self.children['root'].style['position']
        _left = self.children['root'].style['left']
        _top = self.children['root'].style['top']
		
        self.children['root'].style['position'] = 'relative'
        del self.children['root'].style['left']
        del self.children['root'].style['top']
        
        ret = self.repr_widget_for_editor( self.children['root'] )
        self.path_to_this_widget = []
        code_nested = ret + self.check_pending_listeners(self,'self',True)# + self.code_listener_registration[str(id(self))]
        main_code_class = prototypes.proto_code_main_class%{'classname':configuration.configDict[configuration.KEY_PRJ_NAME],
                                                        'config_resourcepath':configuration.configDict[configuration.KEY_RESOURCEPATH],
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
        compiled_code = prototypes.proto_code_program%{ 'code_classes':code_classes,
                                                        'classname':configuration.configDict[configuration.KEY_PRJ_NAME],
                                                        'configuration':configuration.configDict
                                                       }
        
        print(compiled_code)
        
        self.children['root'].style['position'] = _position
        self.children['root'].style['left'] = _left
        self.children['root'].style['top'] = _top
        
        if save_path_filename!=None:
            f = open(save_path_filename, "w")
            f.write(compiled_code)
            f.close()
        
        
class Editor(App):
    def __init__(self, *args):
        editor_res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(Editor, self).__init__(*args, static_paths=(editor_res_path,))

    def idle(self):
        self.resizeHelper.update_position()

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
        m1.append(m10)
        m1.append(m11)
        m1.append(m12)
        m12.append(m121)
        m12.append(m122)
        
        m2 = gui.MenuItem('Edit', width=100, height='100%')
        m21 = gui.MenuItem('Cut', width=100, height=30)
        m22 = gui.MenuItem('Paste', width=100, height=30)
        m2.append(m21)
        m2.append(m22)
        
        m3 = gui.MenuItem('Project Config', width=200, height='100%')
        
        menu.append(m1)
        menu.append(m2)
        menu.append(m3)
        
        menubar.append(menu)
        
        self.toolbar = editor_widgets.ToolBar(width='100%', height='30px', margin='0px 0px')
        self.toolbar.style['border-bottom'] = '1px solid rgba(0,0,0,.12)'
        self.toolbar.add_command('/res/delete.png', self, 'toolbar_delete_clicked', 'Delete Widget')
        self.toolbar.add_command('/res/cut.png', self, 'menu_cut_selection_clicked', 'Cut Widget')
        self.toolbar.add_command('/res/paste.png', self, 'menu_paste_selection_clicked', 'Paste Widget')
        
        self.fileOpenDialog = editor_widgets.EditorFileSelectionDialog('Open Project', 'Select the project file.<br>It have to be a python program created with this editor.', False, '.', True, False, self)
        self.fileOpenDialog.set_on_confirm_value_listener(self, 'on_open_dialog_confirm')
        
        self.fileSaveAsDialog = editor_widgets.EditorFileSaveDialog('Project Save', 'Select the project folder and type a filename', False, '.', False, True, self)
        self.fileSaveAsDialog.add_fileinput_field('untitled.py')
        self.fileSaveAsDialog.set_on_confirm_value_listener(self, 'on_saveas_dialog_confirm')        

        m10.set_on_click_listener(self, 'menu_new_clicked')
        m11.set_on_click_listener(self.fileOpenDialog, 'show')
        m121.set_on_click_listener(self, 'menu_save_clicked')
        m122.set_on_click_listener(self.fileSaveAsDialog, 'show')
        m21.set_on_click_listener(self, 'menu_cut_selection_clicked')
        m22.set_on_click_listener(self, 'menu_paste_selection_clicked')
        
        m3.set_on_click_listener(self, 'menu_project_config_clicked')
        
        self.subContainer = gui.HBox(width='100%', height='96%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL)
        self.subContainer.style['position'] = 'relative'
        self.subContainer.style['overflow']='auto'
        self.subContainer.style['align-items']='stretch'
                
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
            """ % {'id':id(self), 'evt':self.project.EVENT_ONKEYDOWN}
        
        self.projectConfiguration = editor_widgets.ProjectConfigurationDialog('Project Configuration', 'Write here the configuration for your project.')
        
        self.attributeEditor = editor_widgets.EditorAttributes(self, width='24%', height='100%')
        self.attributeEditor.style['position'] = 'absolute'
        self.attributeEditor.style['right'] = '0px'
        self.attributeEditor.add_class('RaisedFrame')
        
        self.signalConnectionManager = editor_widgets.SignalConnectionManager(width='100%', height='50%')
        
        self.mainContainer.append(menubar)
        self.mainContainer.append(self.subContainer)
        
        self.subContainerLeft = gui.Widget(width='20%', height='100%')
        self.subContainerLeft.style['position'] = 'relative'
        self.subContainerLeft.style['left'] = '0px'
        self.subContainerLeft.append(self.widgetsCollection)
        self.subContainerLeft.append(self.signalConnectionManager)
        self.subContainerLeft.add_class('RaisedFrame')
        
        self.subContainer.append(self.subContainerLeft)
        
        self.centralContainer = gui.VBox(width='56%', height='100%')
        self.centralContainer.append(self.toolbar)
        self.centralContainer.append(self.project)
        
        self.subContainer.append(self.centralContainer)
        self.subContainer.append(self.attributeEditor)
        self.project.style['position'] = 'relative'
        
        self.resizeHelper = ResizeHelper(width=16, height=16)
        self.menu_new_clicked()
        
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
        widget.attributes[widget.EVENT_ONCLICK] = "sendCallback('%s','%s');event.stopPropagation();event.preventDefault();" % (id(widget), widget.EVENT_ONCLICK)
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
                
                
                return false;""" % {'evt':widget.EVENT_ONDROPPPED, 'id': str(id(widget)), 'event_click': widget.EVENT_ONCLICK}
                
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
        key = "root" if parent==self.project else str(id(widget))
        if root_tree_node:
            parent.append(widget,key)
            if self.selectedWidget == self.project:
                self.on_widget_selection( widget )
        for child in widget.children.values():
            if type(child) == str:
                continue
            self.add_widget_to_editor(child, widget, False)
    
    def on_widget_selection(self, widget):
        self.remove_box_shadow_selected_widget()
        self.selectedWidget = widget
        self.selectedWidget.style['box-shadow'] = '0 0 10px rgb(33,150,243)'
        self.signalConnectionManager.update(self.selectedWidget, self.project)
        self.attributeEditor.set_widget( self.selectedWidget )
        parent = remi.server.get_method_by(self.mainContainer, self.selectedWidget.attributes['parent_widget'])
        self.resizeHelper.setup(widget,parent)
        print("selected widget: " + str(id(widget)))
        
    def menu_new_clicked(self):
        print('new project')
        self.project.new()
        self.tabindex = 0 #incremental number to allow widgets selection
        self.selectedWidget = self.project
        self.resizeHelper.setup(None, None)
        if 'root' in self.project.children.keys():
            self.project.remove_child( self.project.children['root'] )

    def on_open_dialog_confirm(self, filelist):
        if len(filelist):
            widgetTree = self.project.load(filelist[0], self.projectConfiguration)
            if widgetTree!=None:
                self.add_widget_to_editor( widgetTree )
            self.projectPathFilename = filelist[0]
        
    def menu_save_clicked(self):
        #the resizeHelper have to be removed
        self.resizeHelper.setup(None, None)
        if self.projectPathFilename == '':
            self.fileSaveAsDialog.show()
        else:
            self.remove_box_shadow_selected_widget()
            self.project.save(self.projectPathFilename, self.projectConfiguration)
    
    def remove_box_shadow_selected_widget(self):
        if 'box-shadow' in self.selectedWidget.style.keys():
            del self.selectedWidget.style['box-shadow']
        
    def on_saveas_dialog_confirm(self, path):
        #the resizeHelper have to be removed
        self.resizeHelper.setup(None, None)
        if len(path):
            self.projectPathFilename = path + '/' + self.fileSaveAsDialog.get_fileinput_value()
            print("file:%s"%self.projectPathFilename)
            self.remove_box_shadow_selected_widget()
            self.project.save(self.projectPathFilename, self.projectConfiguration)
            
    def menu_cut_selection_clicked(self):
        if self.selectedWidget==self.project:
            return
        self.resizeHelper.setup(None, None)
        parent = remi.server.get_method_by(self.mainContainer, self.selectedWidget.attributes['parent_widget'])
        self.editCuttedWidget = self.selectedWidget
        parent.remove_child(self.selectedWidget)
        self.selectedWidget = parent
        print("tag cutted:" + str(id(self.editCuttedWidget)))

    def menu_paste_selection_clicked(self):
        if self.editCuttedWidget != None:
            self.selectedWidget.append(self.editCuttedWidget)
            self.editCuttedWidget = None

    def menu_project_config_clicked(self):
        self.projectConfiguration.show(self)

    def toolbar_delete_clicked(self):
        if self.selectedWidget==self.project:
            return
        self.resizeHelper.setup(None, None)
        parent = remi.server.get_method_by(self.mainContainer, self.selectedWidget.attributes['parent_widget'])
        parent.remove_child(self.selectedWidget)
        self.selectedWidget = parent
        print("tag deleted")
        
    def onkeydown(self, keypressed):
        if keypressed==46: #46 the delete keycode
            self.toolbar_delete_clicked()
        print("Key pressed: " + str(keypressed))

        
#function overload for widgets that have to be editable
#the normal onfocus function does not returns the widget instance
#def onfocus_with_instance(self):
#    return self.eventManager.propagate(self.EVENT_ONFOCUS, [self])
def onclick_with_instance(self):
    #return self.eventManager.propagate(self.EVENT_ON_WIDGET_SELECTION, [self])
    self.editor.on_widget_selection(self)
    
def on_dropped(self, left, top):
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
    start(Editor, debug=False, address='0.0.0.0', port=8082)
    
if __name__ == "__main__":
    main()
