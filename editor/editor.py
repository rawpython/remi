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
import inspect
import sys
import os  # for path handling
import prototypes
import editor_widgets
import threading
import traceback

if remi.server.pyLessThan3:
    import imp

    def load_source(filename):
        return imp.load_source('project', filename)
else:
    import importlib.machinery
    import importlib.util

    def load_source(filename):
        loader = importlib.machinery.SourceFileLoader('project', filename)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        _module = importlib.util.module_from_spec(spec)
        loader.exec_module(_module)
        return _module


class DraggableItem(gui.EventSource):
    def __init__(self, app_instance, **kwargs):
        gui.EventSource.__init__(self)
        self.app_instance = app_instance
        self.refWidget = None
        self.parent = None
        self.active = False
        self.origin_x = -1
        self.origin_y = -1
        self.snap_grid_size = 15

    def setup(self, refWidget, newParent):
        # refWidget is the target widget that will be resized
        # newParent is the container
        if self.parent:
            try:
                self.parent.remove_child(self)
            except:
                pass
        if newParent == None:
            return
        self.parent = newParent
        self.refWidget = refWidget

        try:
            self.parent.append(self)
        except:
            pass
        self.update_position()

    def start_drag(self, emitter, x, y):
        self.active = True
        self.app_instance.project.onmousemove.do(self.on_drag)
        self.app_instance.project.onmouseup.do(self.stop_drag)
        self.app_instance.project.onmouseleave.do(self.stop_drag, 0, 0)
        self.origin_x = -1
        self.origin_y = -1

    @gui.decorate_event
    def stop_drag(self, emitter, x, y):
        self.active = False
        self.update_position()
        return ()

    def on_drag(self, emitter, x, y):
        pass

    def update_position(self):
        pass

    def set_snap_grid_size(self, value):
        self.snap_grid_size = value

    def round_grid(self, value):
        return int(value/self.snap_grid_size)*self.snap_grid_size


class SvgDraggablePoint(gui.SvgRectangle, DraggableItem):
    def __init__(self, app_instance, name_coord_x, name_coord_y, compatibility_iterable, **kwargs):
        self.w = 15
        self.h = 15
        super(SvgDraggablePoint, self).__init__(0, 0, self.w, self.h, **kwargs)
        DraggableItem.__init__(self, app_instance, **kwargs)
        self.attributes['stroke-dasharray'] = "2,2"
        self.name_coord_x = name_coord_x
        self.name_coord_y = name_coord_y
        self.set_stroke(1, 'black')
        self.set_fill('#ffcc00')
        self.compatibility_iterable = compatibility_iterable
        self.onmousedown.do(self.start_drag)

    def setup(self, refWidget, newParent):
        if type(refWidget) in self.compatibility_iterable or refWidget == None:
            DraggableItem.setup(self, refWidget, newParent)

    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = float(x)
                self.origin_y = float(y)
                self.refWidget_origin_x = float(
                    self.refWidget.attributes[self.name_coord_x])
                self.refWidget_origin_y = float(
                    self.refWidget.attributes[self.name_coord_y])
            else:
                self.refWidget.attributes[self.name_coord_x] = self.round_grid(
                    self.refWidget_origin_x + float(x) - self.origin_x)
                self.refWidget.attributes[self.name_coord_y] = self.round_grid(
                    self.refWidget_origin_y + float(y) - self.origin_y)
                self.update_position()

    def update_position(self):
        if self.refWidget:
            self.set_position(float(self.refWidget.attributes[self.name_coord_x])-self.w/2, float(
                self.refWidget.attributes[self.name_coord_y])-self.h/2)


class SvgDraggableRectangleResizePoint(gui.SvgRectangle, DraggableItem):
    def __init__(self, app_instance, compatibility_iterable, **kwargs):
        self.w = 15
        self.h = 15
        super(SvgDraggableRectangleResizePoint, self).__init__(
            0, 0, self.w, self.h, **kwargs)
        DraggableItem.__init__(self, app_instance, **kwargs)
        self.attributes['stroke-dasharray'] = "2,2"
        self.set_stroke(1, 'black')
        self.set_fill('#ffcc00')
        self.compatibility_iterable = compatibility_iterable
        self.onmousedown.do(self.start_drag)

    def setup(self, refWidget, newParent):
        if type(refWidget) in self.compatibility_iterable or refWidget == None:
            DraggableItem.setup(self, refWidget, newParent)

    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = float(x)
                self.origin_y = float(y)
                self.refWidget_origin_w = float(
                    self.refWidget.attributes['width'])
                self.refWidget_origin_h = float(
                    self.refWidget.attributes['height'])
            else:
                self.refWidget.attributes['width'] = self.round_grid(
                    self.refWidget_origin_w + float(x) - self.origin_x)
                self.refWidget.attributes['height'] = self.round_grid(
                    self.refWidget_origin_h + float(y) - self.origin_y)
                self.update_position()

    def update_position(self):
        if self.refWidget:
            self.set_position(float(self.refWidget.attributes['x'])+float(self.refWidget.attributes['width'])-self.w/2, float(
                self.refWidget.attributes['y'])+float(self.refWidget.attributes['height'])-self.h/2)


class SvgDraggableCircleResizeRadius(gui.SvgRectangle, DraggableItem):
    def __init__(self, app_instance, compatibility_iterable, **kwargs):
        self.w = 15
        self.h = 15
        super(SvgDraggableCircleResizeRadius, self).__init__(
            0, 0, self.w, self.h, **kwargs)
        DraggableItem.__init__(self, app_instance, **kwargs)
        self.attributes['stroke-dasharray'] = "2,2"
        self.set_stroke(1, 'black')
        self.set_fill('#ffcc00')
        self.compatibility_iterable = compatibility_iterable
        self.onmousedown.do(self.start_drag)

    def setup(self, refWidget, newParent):
        if type(refWidget) in self.compatibility_iterable or refWidget == None:
            DraggableItem.setup(self, refWidget, newParent)

    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = float(x)
                self.origin_y = float(y)
                self.refWidget_origin_r = float(self.refWidget.attributes['r'])
            else:
                r = self.round_grid(
                    self.refWidget_origin_r + float(x) - self.origin_x)
                self.refWidget.attributes['r'] = str(max(0, r))
                self.update_position()

    def update_position(self):
        if self.refWidget:
            self.set_position(float(self.refWidget.attributes['cx'])+float(
                self.refWidget.attributes['r'])-self.w/2, float(self.refWidget.attributes['cy'])-self.h/2)


class ResizeHelper(gui.Widget, DraggableItem):

    def __init__(self, app_instance, **kwargs):
        super(ResizeHelper, self).__init__(**kwargs)
        DraggableItem.__init__(self, app_instance, **kwargs)
        self.style['float'] = 'none'
        self.style['background-image'] = "url('/editor_resources:resize.png')"
        self.style['background-color'] = "rgba(255,255,255,0.0)"
        self.style['position'] = 'absolute'
        self.style['left'] = '0px'
        self.style['top'] = '0px'
        self.onmousedown.do(self.start_drag)

    def setup(self, refWidget, newParent):
        self.style['display'] = 'none'
        if issubclass(newParent.__class__, gui.TabBox):
            return
        if issubclass(refWidget.__class__, gui.Widget) and 'left' in refWidget.style and 'top' in refWidget.style and \
                'width' in refWidget.style and 'height' in refWidget.style and refWidget.css_position=='absolute':
            DraggableItem.setup(self, refWidget, newParent)
            self.style['display'] = 'block'

    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = float(x)
                self.origin_y = float(y)
                self.refWidget_origin_w = gui.from_pix(
                    self.refWidget.style['width'])
                self.refWidget_origin_h = gui.from_pix(
                    self.refWidget.style['height'])
            else:
                self.refWidget.style['width'] = gui.to_pix(self.round_grid(
                    self.refWidget_origin_w + float(x) - self.origin_x))
                self.refWidget.style['height'] = gui.to_pix(self.round_grid(
                    self.refWidget_origin_h + float(y) - self.origin_y))
                self.update_position()

    def update_position(self):
        self.style['position'] = 'absolute'
        if self.refWidget:
            if 'left' in self.refWidget.style and 'top' in self.refWidget.style:
                self.style['left'] = gui.to_pix(gui.from_pix(
                    self.refWidget.style['left']) + gui.from_pix(self.refWidget.style['width']))
                self.style['top'] = gui.to_pix(gui.from_pix(
                    self.refWidget.style['top']) + gui.from_pix(self.refWidget.style['height']))


class DragHelper(gui.Widget, DraggableItem):

    def __init__(self, app_instance, **kwargs):
        super(DragHelper, self).__init__(**kwargs)
        DraggableItem.__init__(self, app_instance, **kwargs)
        self.style['float'] = 'none'
        self.style['background-image'] = "url('/editor_resources:drag.png')"
        self.style['background-color'] = "rgba(255,255,255,0.0)"
        self.style['position'] = 'absolute'
        self.style['left'] = '0px'
        self.style['top'] = '0px'
        self.onmousedown.do(self.start_drag)

    def setup(self, refWidget, newParent):
        self.style['display'] = 'none'
        if issubclass(newParent.__class__, gui.TabBox):
            return
        if issubclass(refWidget.__class__, gui.Widget) and 'left' in refWidget.style and 'top' in refWidget.style and refWidget.css_position=='absolute':
            DraggableItem.setup(self, refWidget, newParent)
            self.style['display'] = 'block'

    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = float(x)
                self.origin_y = float(y)
                self.refWidget_origin_x = gui.from_pix(
                    self.refWidget.style['left'])
                self.refWidget_origin_y = gui.from_pix(
                    self.refWidget.style['top'])
            else:
                self.refWidget.style['left'] = gui.to_pix(self.round_grid(
                    self.refWidget_origin_x + float(x) - self.origin_x))
                self.refWidget.style['top'] = gui.to_pix(self.round_grid(
                    self.refWidget_origin_y + float(y) - self.origin_y))
                self.update_position()

    def update_position(self):
        self.style['position'] = 'absolute'
        if self.refWidget:
            if 'left' in self.refWidget.style and 'top' in self.refWidget.style:
                self.style['left'] = gui.to_pix(gui.from_pix(
                    self.refWidget.style['left'])-gui.from_pix(self.style['width']))
                self.style['top'] = gui.to_pix(gui.from_pix(
                    self.refWidget.style['top'])-gui.from_pix(self.style['width']))


class Project(gui.Container):
    """ The editor project is pure html with specific tag attributes
        This class loads and save the project file, 
        and also compiles a project in python code.
    """

    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)

        self.style.update({'position': 'relative',
                           'overflow': 'auto',
                           'background-color': 'rgb(250,248,240)',
                           'background-image': "url('/editor_resources:background.png')"})
        self.attr_editor = True
        self.attr_editor_newclass = True

    def load(self, ifile, configuration):
        self.ifile = ifile

        _module = load_source(self.ifile)

        configuration.configDict = _module.configuration

        # finding App class
        clsmembers = inspect.getmembers(_module, inspect.isclass)

        app_init_fnc = None
        for (name, value) in clsmembers:
            if issubclass(value, App) and name != 'App':
                app_init_fnc = value

        if app_init_fnc == None:
            return None

        members_list = app_init_fnc.__dict__.values()
        for m in members_list:
            if inspect.isfunction(m) and m.__name__ not in ['__init__', 'main', 'idle', 'construct_ui']:
                import types
                setattr(self, m.__name__, types.MethodType(m, self))
                print(m.__name__)
        root_widget = app_init_fnc.construct_ui(self)
        return root_widget

    def check_pending_listeners(self, widget, widgetVarName, force=False):
        code_nested_listener = ''
        # checking if pending listeners code production can be solved
        for event in self.pending_listener_registration:
            if force or (hasattr(event['eventsource'], 'path_to_this_widget') and hasattr(event['eventlistener'], 'path_to_this_widget')):
                if (force or (widget.identifier in event['eventsource'].path_to_this_widget and widget.identifier in event['eventlistener'].path_to_this_widget)) and event['done'] == False:
                    # this means that this is the root node from where the leafs(listener and source) departs, hre can be set the listener
                    event['done'] = True

                    # event source chain
                    sourcename = 'self'
                    source_filtered_path = event['eventsource'].path_to_this_widget[:]
                    listener_filtered_path = event['eventlistener'].path_to_this_widget[:]
                    for v in widget.path_to_this_widget:
                        source_filtered_path.remove(v)
                        listener_filtered_path.remove(v)

                    if len(source_filtered_path) == 0 and event['eventsource'].attr_editor_newclass == False:
                        sourcename = event['eventsource'].identifier

                    #    listenername = event['eventlistener'].identifier
                    if force or (self.children['root'] == widget and not (widget.attr_editor_newclass == True)):
                        sourcename = self.children['root'].identifier
                        if self.children['root'].identifier in source_filtered_path:
                            source_filtered_path.remove(
                                self.children['root'].identifier)

                    if len(source_filtered_path) > 0:
                        sourcename = (
                            "%s.children['" + "'].children['".join(source_filtered_path) + "']") % sourcename

                    # listener chain
                    listenername = "self"
                    if force or (self.children['root'] == widget and not (widget.attr_editor_newclass == True)):
                        if event['eventlistener'] != self:
                            listenername = self.children['root'].identifier
                    if len(listener_filtered_path) == 0 and event['eventlistener'].attr_editor_newclass == False:
                        listenername = event['eventlistener'].identifier
                    if len(listener_filtered_path) > 0:
                        listenername = (
                            "%s.children['" + "'].children['".join(listener_filtered_path) + "']") % listenername

                    code_nested_listener += prototypes.proto_set_listener % {'sourcename': sourcename,
                                                                             'register_function':  event['setoneventfuncname'],
                                                                             'listenername': listenername,
                                                                             'listener_function': event['listenerfuncname']}
                    if not event['eventlistener'].identifier in self.code_declared_classes:
                        self.code_declared_classes[event['eventlistener'].identifier] = ''

                    if (event['eventlistener'].attr_editor_newclass == True):
                        self.code_declared_classes[event['eventlistener']
                                                   .identifier] += event['listenerClassFunction']
        return code_nested_listener

    # widgetVarName is the name with which the parent calls this instance
    def repr_widget_for_editor(self, widget, first_node=False):
        if first_node:
            self.code_declared_classes = {}
            self.pending_listener_registration = list()
            # a list containing widgets that have been parsed and that are considered valid listeners
            self.known_project_children = [self, ]
            # a list containing dicts {listener, emitter, register_function, listener_function}
            self.pending_signals_to_connect = list()
            self.path_to_this_widget = []
            self.prepare_path_to_this_widget(self.children['root'])
        self.known_project_children.append(widget)

        widget.path_to_this_widget.append(widget.identifier)

        print(widget.identifier)

        code_nested = ''  # the code strings to return

        if not hasattr(widget, 'attributes'):
            return ''  # no nested code

        widgetVarName = widget.identifier
        classname = 'CLASS' + \
            widgetVarName if widget.attr_editor_newclass else widget.__class__.__name__

        code_nested = prototypes.proto_widget_allocation % {
            'varname': widgetVarName, 'classname': classname}

        #code_nested += prototypes.proto_attribute_setup%{'varname': widgetVarName, 'attr_dict': ','.join('"%s":"%s"'%(key,widget.attributes[key]) for key in widget.attributes.keys() if key not in html_helper.htmlInternallyUsedTags)}
        #code_nested += prototypes.proto_style_setup%{'varname': widgetVarName, 'style_dict': ','.join('"%s":"%s"'%(key,widget.style[key]) for key in widget.style.keys())}

        for x, y in inspect.getmembers(widget.__class__):
            if type(y) == property and not getattr(widget, x) is None:
                if hasattr(y.fget, "editor_attributes"): #if this property is visible for the editor
                    _value = getattr(widget, x)
                    if type(_value) == str:
                        _value = '"%s"' % _value
                    code_nested += prototypes.proto_property_setup % {
                        'varname': widgetVarName, 'property': x, 'value': _value}

        # for all the methods of this widget
        for (setOnEventListenerFuncname, setOnEventListenerFunc) in inspect.getmembers(widget):
            # if the member is decorated by decorate_set_on_listener
            if issubclass(type(setOnEventListenerFunc), gui.ClassEventConnector):
                # if there is a callback
                if not setOnEventListenerFunc.callback is None and hasattr(setOnEventListenerFunc.event_method_bound, '_event_info'):
                    listenerFunction = setOnEventListenerFunc.callback
                    if issubclass(type(listenerFunction), gui.ClassEventConnector):
                        listenerFunction = listenerFunction.event_method_bound

                    listenerPrototype = setOnEventListenerFunc.event_method_bound._event_info[
                        'prototype']
                    listener = listenerFunction.__self__

                    # setOnEventListenerFunc._event_info['name'] + "_" + widget.identifier
                    listenerFunctionName = listenerFunction.__name__

                    listenerClassFunction = prototypes.proto_code_function % {'funcname': listenerFunctionName,
                                                                              'parameters': listenerPrototype}

                    # override, if already implemented, we use this code, unless it is a fakeListenerFunction
                    if hasattr(listener, listenerFunctionName) and listenerFunction.__code__ != editor_widgets.fakeListenerFunc.__code__:
                        listenerClassFunction = inspect.getsource(
                            listenerFunction)

                    # if the listener is already in the dictionary, and so it already used by another event
                    # skip
                    skip = False
                    for pending in self.pending_listener_registration:
                        if pending['eventlistener'] == listener:
                            if pending['listenerfuncname'] == listenerFunctionName:
                                skip = True
                                break
                    if skip:
                        continue

                    self.pending_listener_registration.append({'done': False,
                                                               'eventsource': widget,
                                                               'eventlistener': listener,
                                                               'setoneventfuncname': setOnEventListenerFuncname,
                                                               'listenerfuncname': listenerFunctionName,
                                                               'listenerClassFunction': listenerClassFunction})

        if widget.attr_editor_newclass:
            widgetVarName = 'self'

        children_code_nested = ''
        for child_key in widget.children.keys():
            child = widget.children[child_key]
            if type(child) == str:
                #children_code_nested += prototypes.proto_layout_append%{'parentname':widgetVarName,'varname':"'%s'"%child}
                continue
            if not issubclass(child.__class__, gui.Widget):
                continue
            if not child.attr_editor:
                continue
            child.path_to_this_widget = widget.path_to_this_widget[:]
            children_code_nested += self.repr_widget_for_editor(child)
            children_code_nested += prototypes.proto_layout_append % {
                'parentname': widgetVarName, 'varname': "%s,'%s'" % (child.identifier, child.identifier)}

        children_code_nested += self.check_pending_listeners(
            widget, widgetVarName)

        # and not (classname in self.code_declared_classes.keys()):
        if widget.attr_editor_newclass:
            if not widget.identifier in self.code_declared_classes:
                self.code_declared_classes[widget.identifier] = ''
            self.code_declared_classes[widget.identifier] = prototypes.proto_code_class % {'classname': classname, 'superclassname': widget.__class__.__name__,
                                                                                           'nested_code': children_code_nested} + self.code_declared_classes[widget.identifier]
        else:
            code_nested = code_nested + children_code_nested

        return code_nested

    def prepare_path_to_this_widget(self, node):
        # here gets initiated to null list the path_to_this_widget chain
        node.path_to_this_widget = []
        for child in node.children.values():
            if type(child) == str:
                continue
            if not issubclass(child.__class__, gui.Widget):
                continue
            if not child.attr_editor:
                continue
            self.prepare_path_to_this_widget(child)

    def save(self, save_path_filename, configuration):
        compiled_code = ''
        code_classes = ''

        ret = self.repr_widget_for_editor(self.children['root'], True)
        # + self.code_listener_registration[str(id(self))]
        code_nested = ret + self.check_pending_listeners(self, 'self', True)

        main_code_class = prototypes.proto_code_main_class % {'classname': configuration.configDict[configuration.KEY_PRJ_NAME],
                                                              'config_resourcepath': configuration.configDict[configuration.KEY_RESOURCEPATH],
                                                              'code_nested': code_nested,
                                                              'mainwidgetname': self.children['root'].identifier}

        if self.identifier in self.code_declared_classes.keys():
            main_code_class += self.code_declared_classes[self.identifier]
            del self.code_declared_classes[self.identifier]

        for key in self.code_declared_classes.keys():
            code_class = self.code_declared_classes[key]
            code_listener_setting = ''
            code_classes += code_class

        modules_to_import = []
        for w in self.known_project_children:
            if not w.__module__ in modules_to_import and w.__module__ != "__main__" and w.__module__ != "project":
                modules_to_import.append(w.__module__)

        code_classes += main_code_class
        compiled_code = prototypes.proto_code_program % {'imports': '\n'.join(["from " + modulename + " import *" for modulename in modules_to_import]),
                                                         'code_classes': code_classes,
                                                         'classname': configuration.configDict[configuration.KEY_PRJ_NAME],
                                                         'configuration': configuration.configDict
                                                         }

        print(compiled_code)

        if save_path_filename != None:
            f = open(save_path_filename, "w")
            f.write(compiled_code)
            f.close()


class Editor(App):
    EVENT_ONDROPPPED = "on_dropped"

    selectedWidget = None

    def __init__(self, *args):
        editor_res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(Editor, self).__init__(
            *args, static_file_path={'editor_resources': editor_res_path})

    def idle(self):
        for drag_helper in self.drag_helpers:
            drag_helper.update_position()

    def main(self):
        self.mainContainer = gui.Container(width='100%', height='100%', layout_orientation=gui.Container.LAYOUT_VERTICAL, style={
                                           'background-color': 'white', 'border': 'none', 'overflow': 'hidden'})

        menubar = gui.MenuBar(height='4%')
        menu = gui.Menu(width='100%', height='100%')
        menu.style['z-index'] = '1'
        m1 = gui.MenuItem('File', width=150, height='100%')
        m10 = gui.MenuItem('New', width=150, height=30)
        m11 = gui.MenuItem('Open', width=150, height=30)
        m12 = gui.MenuItem('Save Your App', width=150, height=30)
        #m12.style['visibility'] = 'hidden'
        m121 = gui.MenuItem('Save', width=100, height=30)
        m122 = gui.MenuItem('Save as', width=100, height=30)
        m123 = gui.MenuItem('Export widget as', width=200, height=30)
        m1.append([m10, m11, m12])
        m12.append([m121, m122, m123])

        m2 = gui.MenuItem('Edit', width=100, height='100%')
        m21 = gui.MenuItem('Cut', width=100, height=30)
        m22 = gui.MenuItem('Paste', width=100, height=30)
        m2.append([m21, m22])

        m3 = gui.MenuItem('Project Config', width=200, height='100%')

        m4 = gui.MenuItem('Became a Patron', width=200,
                          height='100%', style={'font-weight': 'bold'})

        menu.append([m1, m2, m3, m4])

        menubar.append(menu)

        self.toolbar = editor_widgets.ToolBar(
            width='100%', height='30px', margin='0px 0px')
        self.toolbar.style['border-bottom'] = '1px solid rgba(0,0,0,.12)'
        self.toolbar.add_command(
            '/editor_resources:delete.png', self.toolbar_delete_clicked, 'Delete Widget')
        self.toolbar.add_command(
            '/editor_resources:cut.png', self.menu_cut_selection_clicked, 'Cut Widget')
        self.toolbar.add_command(
            '/editor_resources:paste.png', self.menu_paste_selection_clicked, 'Paste Widget')

        lbl = gui.Label("Snap grid", width=100)
        spin_grid_size = gui.SpinBox('15', '1', '100', width=50)
        spin_grid_size.set_on_change_listener(self.on_snap_grid_size_change)

        grid_size = gui.HBox(children=[lbl, spin_grid_size], style={
                             'outline': '1px solid gray', 'margin': '2px', 'margin-left': '10px'})
        self.toolbar.append(grid_size)

        self.fileOpenDialog = editor_widgets.EditorFileSelectionDialog(
            'Open Project', 'Select the project file.<br>It have to be a python program created with this editor.', False, '.', True, False, self)
        self.fileOpenDialog.confirm_value.do(self.on_open_dialog_confirm)

        self.fileSaveAsDialog = editor_widgets.EditorFileSaveDialog(
            'Project Save', 'Select the project folder and type a filename', False, '.', False, True, self)
        self.fileSaveAsDialog.add_fileinput_field('untitled.py')
        self.fileSaveAsDialog.confirm_value.do(self.menu_save_clicked)

        m10.onclick.do(self.menu_new_clicked)
        m11.onclick.do(self.fileOpenDialog.show)
        m121.onclick.do(self.menu_save_clicked)
        m122.onclick.do(self.fileSaveAsDialog.show)
        m123.onclick.do(self.menu_save_widget_clicked)
        m21.onclick.do(self.menu_cut_selection_clicked)
        m22.onclick.do(self.menu_paste_selection_clicked)

        m3.onclick.do(self.menu_project_config_clicked)
        m4.onclick.do(self.menu_became_a_patron)

        self.subContainer = gui.HBox(
            width='100%', height='96%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.subContainer.style.update({'position': 'relative',
                                        'overflow': 'hidden',
                                        'align-items': 'stretch'})

        # here are contained the widgets
        self.widgetsCollection = editor_widgets.WidgetCollection(
            self, width='100%', height='50%')

        self.projectConfiguration = editor_widgets.ProjectConfigurationDialog(
            'Project Configuration', 'Write here the configuration for your project.')

        self.attributeEditor = editor_widgets.EditorAttributes(
            self, width='100%')
        self.attributeEditor.style['overflow'] = 'hide'
        self.signalConnectionManager = editor_widgets.SignalConnectionManager(
            width='100%', height='50%', style={'order': '1'})

        self.mainContainer.append([menubar, self.subContainer])

        self.subContainerLeft = gui.VBox(width='20%', height='100%')
        self.subContainerLeft.style['position'] = 'relative'
        self.subContainerLeft.style['left'] = '0px'
        self.widgetsCollection.style['order'] = '0'
        self.subContainerLeft.append(
            {'widgets_collection': self.widgetsCollection, 'signal_manager': self.signalConnectionManager})
        self.subContainerLeft.add_class('RaisedFrame')

        self.centralContainer = gui.VBox(width='56%', height='100%')
        self.centralContainer.append(self.toolbar)

        self.subContainerRight = gui.Container(width='24%', height='100%')
        self.subContainerRight.style.update(
            {'position': 'absolute', 'right': '0px', 'overflow-y': 'auto', 'overflow-x': 'hidden'})
        self.subContainerRight.add_class('RaisedFrame')

        self.instancesWidget = editor_widgets.InstancesWidget(width='100%')
        self.instancesWidget.treeView.on_tree_item_selected.do(
            self.on_instances_widget_selection)

        self.subContainerRight.append(
            {'instances_widget': self.instancesWidget, 'attributes_editor': self.attributeEditor})

        self.subContainer.append(
            [self.subContainerLeft, self.centralContainer, self.subContainerRight])

        self.drag_helpers = [ResizeHelper(self, width=16, height=16),
                             DragHelper(self, width=15, height=15),
                             SvgDraggablePoint(
                                 self, 'cx', 'cy', [gui.SvgCircle]),
                             SvgDraggableCircleResizeRadius(
                                 self, [gui.SvgCircle]),
                             SvgDraggablePoint(
                                 self, 'x1', 'y1', [gui.SvgLine]),
                             SvgDraggablePoint(
                                 self, 'x2', 'y2', [gui.SvgLine]),
                             SvgDraggablePoint(
                                 self, 'x', 'y', [gui.SvgRectangle, gui.SvgText, gui.SvgImage]),
                             SvgDraggableRectangleResizePoint(self, [gui.SvgRectangle, gui.SvgImage])]
        for drag_helper in self.drag_helpers:
            drag_helper.stop_drag.do(self.on_drag_resize_end)

        self.menu_new_clicked(None)
        self.on_snap_grid_size_change(
            spin_grid_size, spin_grid_size.get_value())

        self.projectPathFilename = ''
        self.editCuttedWidget = None  # cut operation, contains the cutted tag

        # returning the root widget
        return self.mainContainer

    def on_snap_grid_size_change(self, emitter, value):
        value = float(value)
        for drag_helper in self.drag_helpers:
            drag_helper.set_snap_grid_size(value)

    def on_drag_resize_end(self, emitter):
        self.selectedWidget.__dict__[
            'attributes_editor'].set_widget(self.selectedWidget)

    def configure_widget_for_editing(self, widget):
        """ A widget have to be added to the editor, it is configured here in order to be conformant 
            to the editor
        """
        if not issubclass(widget.__class__, gui.Widget):
            return
        if not widget.attr_editor:
            return

        # for all the methods of this widget

        for (setOnEventListenerFuncname, setOnEventListenerFunc) in inspect.getmembers(widget):
            # if the member is decorated by decorate_set_on_listener
            if hasattr(setOnEventListenerFunc, '_event_info'):
                setOnEventListenerFunc.__class__ = editor_widgets.ClassEventConnectorEditor
                if setOnEventListenerFunc.callback:
                    getattr(widget, setOnEventListenerFuncname).do(
                        setOnEventListenerFunc.callback)

        # we force a connection, also if back_callback is None, to get the widget selectable
        back_callback = widget.onclick.callback
        widget.onclick.do(back_callback)
        widget.onclick.editor_listener_callback = self.on_widget_selection

        # setup of the on_dropped function of the widget in order to manage the dragNdrop
        widget.__class__.on_dropped = on_dropped

        # drag properties
        #widget.style['resize'] = 'both'
        #widget.style['overflow'] = 'auto'
        widget.attributes['draggable'] = 'true'

        widget.attributes['tabindex'] = str(self.tabindex)
        # if not 'position' in widget.style.keys():
        #    widget.style['position'] = 'absolute'
        # if not 'left' in widget.style.keys():
        #    widget.style['left'] = '1px'
        # if not 'top' in widget.style.keys():
        #    widget.style['top'] = '1px'
        self.tabindex += 1

    def add_widget_to_editor(self, widget, parent=None, root_tree_node=True):
        if parent == None:
            parent = self.selectedWidget

        self.configure_widget_for_editing(widget)
        #widget.identifier = widget.attributes.get('editor_varname', widget.identifier)
        key = "root" if parent == self.project else widget.identifier
        if root_tree_node:
            parent.append(widget, key)
            if self.selectedWidget == self.project:
                self.on_widget_selection(widget)
        #dcopy = widget.children.copy()
        for child in widget.children.values():
            if type(child) == str:
                continue
            self.add_widget_to_editor(child, widget, False)
        self.instancesWidget.update(self.project, self.selectedWidget)
        # if root_tree_node:
        #    self.on_widget_selection(widget)

    def on_instances_widget_selection(self, instancesWidgetItem, selectedWidget):
        self.on_widget_selection(selectedWidget)

    def on_widget_selection(self, widget):
        import time
        t = time.time()

        if issubclass(widget.__class__, gui.Container) or widget == None:
            self.subContainerLeft.append(
                self.widgetsCollection, 'widgets_collection')
        else:
            self.subContainerLeft.append(gui.Label("Cannot append widgets to %s class. It is not a container. Select a container" %
                                                   self.selectedWidget.__class__.__name__), 'widgets_collection')

        if self.selectedWidget == widget or widget == self.project:
            self.selectedWidget = widget
            return
        self.remove_box_shadow_selected_widget()
        self.selectedWidget = widget

        self.selectedWidget.style['box-shadow'] = '0 0 10px rgb(33,150,243)'
        # if self.selectedWidget.__dict__.get('signal_manager',None) is None:
        #    self.selectedWidget.__dict__['signal_manager'] = editor_widgets.SignalConnectionManager(width='100%', height='50%', style={'order':'1'})
        self.signalConnectionManager.update(self.selectedWidget, self.project)
        #self.subContainerLeft.append(self.selectedWidget.__dict__['signal_manager'], 'signal_manager')
        if self.selectedWidget.__dict__.get('attributes_editor', None) is None:
            self.selectedWidget.__dict__['attributes_editor'] = editor_widgets.EditorAttributes(
                self, width='100%', style={'overflow': 'hide'})
            self.selectedWidget.__dict__[
                'attributes_editor'].set_widget(self.selectedWidget)
        self.subContainerRight.append(self.selectedWidget.__dict__[
                                      'attributes_editor'], 'attributes_editor')

        parent = self.selectedWidget.get_parent()
        for drag_helper in self.drag_helpers:
            drag_helper.setup(widget, parent)
        # self.instancesWidget.select(self.selectedWidget)
        self.instancesWidget.update(self.project, self.selectedWidget)
        print("selected widget: " + widget.identifier)
        print("selected widget class: " + widget.__class__.__name__)
        print("is widget Container: " +
              str(issubclass(self.selectedWidget.__class__, gui.Container)))

        print(time.time()-t)

    def menu_new_clicked(self, widget):
        print('new project')
        # self.project.new()
        self.project = Project(width='100%', height='100%')
        self.project.style['min-height'] = '400px'
        self.project.attributes['ondragover'] = "event.preventDefault();"
        self.project.attributes['ondrop'] = """event.preventDefault();
                var data = JSON.parse(event.dataTransfer.getData('application/json'));
                var params={};
                if( data[0] == 'add'){
                    params['left']=event.clientX-event.currentTarget.getBoundingClientRect().left;
                    params['top']=event.clientY-event.currentTarget.getBoundingClientRect().top;
                }
                sendCallbackParam(data[1],'%(evt)s',params);
                
                return false;""" % {'evt': self.EVENT_ONDROPPPED}
        self.project.identifier = 'App'
        self.project.onkeydown.do(self.onkeydown)
        self.centralContainer.append(self.project, 'project')
        self.project.style['position'] = 'relative'
        self.tabindex = 0  # incremental number to allow widgets selection
        self.selectedWidget = None
        self.on_widget_selection(self.project)
        for drag_helper in self.drag_helpers:
            drag_helper.setup(None, None)
        if 'root' in self.project.children.keys():
            self.project.remove_child(self.project.children['root'])

    def on_open_dialog_confirm(self, widget, filelist):
        if len(filelist):
            self.menu_new_clicked(None)
            try:
                widgetTree = self.project.load(
                    filelist[0], self.projectConfiguration)
                if widgetTree != None:
                    self.add_widget_to_editor(widgetTree)
                self.projectPathFilename = filelist[0]
            except:
                self.show_error_dialog("ERROR: Unable to load the project",
                                       "There were an error during project load: %s" % traceback.format_exc())

    def menu_save_clicked(self, widget, path=""):
        # the dragHelper have to be removed
        for drag_helper in self.drag_helpers:
            drag_helper.setup(None, None)
        if len(path):
            self.projectPathFilename = path + '/' + \
                self.fileSaveAsDialog.get_fileinput_value()
        else:
            if not len(self.projectPathFilename):
                self.fileSaveAsDialog.confirm_value.do(self.menu_save_clicked)
                self.fileSaveAsDialog.show()
                return

        self.remove_box_shadow_selected_widget()
        self.project.save(self.projectPathFilename, self.projectConfiguration)

    def menu_save_widget_clicked(self, widget, path=""):
        """ This method allows to export the selected widget
        """
        if len(path):
            self.projectPathFilename = path + '/' + \
                self.fileSaveAsDialog.get_fileinput_value()
        else:
            self.fileSaveAsDialog.confirm_value.do(
                self.menu_save_widget_clicked)
            self.fileSaveAsDialog.show()
            return

        code = ""
        code = code + \
            self.project.repr_widget_for_editor(self.selectedWidget, True)
        for key in self.project.code_declared_classes.keys():
            code_class = self.project.code_declared_classes[key]
            code = code + code_class
        with open(self.projectPathFilename, "w") as f:
            f.write(code)

    def remove_box_shadow_selected_widget(self):
        if 'box-shadow' in self.selectedWidget.style.keys():
            del self.selectedWidget.style['box-shadow']

    '''
    def recursive_get_parent(self, widget, root=None):
        """ The ability to change the widget identifier at runtime causes 
            that it cannot be found directly in runtimeInstances. So a parent have to be found
        """
        if root==None:
            root = self.project
        if widget in root.children.values():
            return root
        for c in root.children.values():
            return self.recursive_get_parent(widget, c)
    '''

    def menu_cut_selection_clicked(self, widget):
        if self.selectedWidget == self.project:
            return
        for drag_helper in self.drag_helpers:
            drag_helper.setup(None, None)
        parent = self.selectedWidget.get_parent()
        self.editCuttedWidget = self.selectedWidget
        parent.remove_child(self.selectedWidget)
        print("tag cutted:" + self.editCuttedWidget.identifier)
        self.on_widget_selection(parent)

    def menu_paste_selection_clicked(self, widget):
        if self.editCuttedWidget != None:
            key = "root" if self.selectedWidget == self.project else self.editCuttedWidget.identifier
            self.selectedWidget.append(self.editCuttedWidget, key)
            self.editCuttedWidget = None
            self.instancesWidget.update(self.project, self.selectedWidget)

    def menu_became_a_patron(self, widget):
        dialog = gui.GenericDialog(
            "Became a Patron", "This editor is made for you with passion. \nIt would be fantastic if you give a contribution, also a little one. ;-)", width="50%")
        dialog.add_field("link", gui.Link("https://www.patreon.com/remigui",
                                          "Click this link to Donate", True, style={'font-weight': 'bolder'}))
        dialog.children["message"].style['white-space'] = 'pre'
        dialog.cancel.style['display'] = 'none'
        dialog.conf.set_text("Back")
        dialog.show(self)

    def menu_project_config_clicked(self, widget):
        self.projectConfiguration.show(self)

    def toolbar_delete_clicked(self, widget):
        if self.selectedWidget == self.project:
            return
        for drag_helper in self.drag_helpers:
            drag_helper.setup(None, None)
        parent = self.selectedWidget.get_parent()
        parent.remove_child(self.selectedWidget)
        todel = self.selectedWidget
        self.on_widget_selection(parent)
        del todel
        print("tag deleted")

    def onkeydown(self, emitter, key, keycode, ctrl, shift, alt):
        if str(keycode) == '46':  # 46 the delete keycode
            self.toolbar_delete_clicked(None)
        print("Key pressed: " + str(keycode))

    def show_error_dialog(self, title, message):
        error_dialog = gui.GenericDialog(title, message)
        error_dialog.children["title"].style['background-color'] = 'red'
        error_dialog.children["message"].style['white-space'] = 'pre'
        error_dialog.cancel.style['display'] = 'none'
        error_dialog.show(self)


def on_dropped(self, left, top):
    if len(left) < 1:
        left = '0px'
    if len(top) < 1:
        top = '0px'
    self.style['left'] = left
    self.style['top'] = top


if __name__ == "__main__":
    start(Editor, debug=False, address='0.0.0.0', port=8082,
          update_interval=0.05, multiple_instance=True)
