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

import os
import logging
from functools import cmp_to_key
import collections

from .server import runtimeInstances, update_event

log = logging.getLogger('remi.gui')


def decorate_set_on_listener(eventName, params):
    """ setup important informations for editor purpose """
    def add_annotation(function):
        function._event_listener = {}
        function._event_listener['eventName'] = eventName
        function._event_listener['prototype'] = params
        return function
    return add_annotation


def decorate_constructor_parameter_types(type_list):
    def add_annotation(function):
        function._constructor_types = type_list
        return function
    return add_annotation


def to_pix(x):
    return str(x) + 'px'


def from_pix(x):
    v = 0
    try:
        v = int(float(x.replace('px', '')))
    except ValueError:
        log.error('error parsing px', exc_info=True)
    return v


def jsonize(d):
    return ';'.join(map(lambda k, v: k + ':' + v + '', d.keys(), d.values()))


class EventManager(object):
    """Manages the event propagation to the listeners functions"""

    def __init__(self):
        self.listeners = {}

    def propagate(self, eventname, params):
        # if for an event there is a listener, it calls the listener passing the parameters
        if eventname not in self.listeners:
            return
        listener = self.listeners[eventname]
        return getattr(listener['instance'], listener['funcname'])(*params)

    def register_listener(self, eventname, instance, funcname):
        """register a listener for a specific event"""
        self.listeners[eventname] = {'instance':instance, 'funcname':funcname}


class Tag(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        # the runtime instances are processed every time a requests arrives, searching for the called method
        # if a class instance is not present in the runtimeInstances, it will
        # we not callable
        runtimeInstances.append(self)

        self._render_children_list = []

        self.children = {}
        self.attributes = {}  # properties as class id style

        self.type = ''
        self.attributes['id'] = str(id(self))
        self.attributes['class'] = self.__class__.__name__

    def repr(self, client, include_children=True):
        """it is used to automatically represent the object to HTML format
        packs all the attributes, children and so on."""

        self.attributes['children_list'] = ','.join(map(lambda k, v: str(
            id(v)), self.children.keys(), self.children.values())) 

        # concatenating innerHTML. in case of html object we use repr, in case
        # of string we use directly the content
        innerHTML = ''
        for s in self._render_children_list:
            if isinstance(s, type('')):
                innerHTML = innerHTML + s
            elif isinstance(s, type(u'')):
                innerHTML = innerHTML + s.encode('utf-8')
            elif include_children:
                innerHTML = innerHTML + s.repr(client)

        html = '<%s %s>%s</%s>' % (self.type,
                                   ' '.join('%s="%s"' % (k,v) if v is not None else k for k,v in self.attributes.items()),
                                   innerHTML,
                                   self.type)
        return html

    def add_child(self, key, child):
        """add a child to the widget

        The key can be everything you want. To retrieve the child call get_child
        """
        if hasattr(child, 'attributes'):
            child.attributes['parent_widget'] = str(id(self))

        if key in self.children:
            self._render_children_list.remove(self.children[key])
        self._render_children_list.append(child)

        self.children[key] = child

    def get_child(self, key):
        """return the child called 'key'"""
        return self.children[key]

    def empty(self):
        """remove all children from the widget"""
        for k in list(self.children.keys()):
            self.remove_child(self.children[k])

    def remove_child(self, child):
        """remove a child instance from the widget"""
        if child in self.children.values():
            self._render_children_list.remove(child)
            for k in self.children.keys():
                if str(id(self.children[k])) == str(id(child)):
                    if k in self._render_children_list:
                        self._render_children_list.remove(self.children[k])
                    self.children.pop(k)
                    # when the child is removed we stop the iteration
                    # this implies that a child replication should not be allowed
                    break


class Widget(Tag):

    """base class for gui widgets.

    In html, it is a DIV tag    
    the self.type attribute specifies the HTML tag representation    
    the self.attributes[] attribute specifies the HTML attributes like 'style' 'class' 'id' 
    the self.style[] attribute specifies the CSS style content like 'font' 'color'. 
    It will be packet togheter with 'self.attributes'

    """
    # constants
    LAYOUT_HORIZONTAL = True
    LAYOUT_VERTICAL = False

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        """w = numeric with
        h = numeric height
        layout_orientation = specifies the "float" css attribute
        widget_spacing = specifies the "margin" css attribute for the children"""
        super(Widget, self).__init__(**kwargs)

        self.style = {}

        self.type = 'div'

        # some constants for the events
        self.EVENT_ONCLICK = 'onclick'
        self.EVENT_ONDBLCLICK = 'ondblclick'
        self.EVENT_ONMOUSEDOWN = 'onmousedown'
        self.EVENT_ONMOUSEMOVE = 'onmousemove'
        self.EVENT_ONMOUSEOVER = 'onmouseover'
        self.EVENT_ONMOUSEOUT = 'onmouseout'
        self.EVENT_ONMOUSELEAVE = 'onmouseleave'
        self.EVENT_ONMOUSEUP = 'onmouseup'
        self.EVENT_ONTOUCHMOVE = 'ontouchmove'
        self.EVENT_ONTOUCHSTART = 'ontouchstart'
        self.EVENT_ONTOUCHEND = 'ontouchend'
        self.EVENT_ONTOUCHENTER = 'ontouchenter'
        self.EVENT_ONTOUCHLEAVE = 'ontouchleave'
        self.EVENT_ONTOUCHCANCEL = 'ontouchcancel'
        self.EVENT_ONKEYDOWN = 'onkeydown'
        self.EVENT_ONKEYPRESS = 'onkeypress'
        self.EVENT_ONKEYUP = 'onkeyup'
        self.EVENT_ONCHANGE = 'onchange'
        self.EVENT_ONFOCUS = 'onfocus'
        self.EVENT_ONBLUR = 'onblur'
        self.EVENT_ONCONTEXTMENU = "oncontextmenu"
        self.EVENT_ONUPDATE = 'onupdate'

        self.style['margin'] = '0px auto'

        self.layout_orientation = Widget.LAYOUT_VERTICAL

        self.oldRootWidget = None  # used when hiding the widget

        self.eventManager = EventManager()

        self.set_size(kwargs.get('width'), kwargs.get('height'))

    def set_size(self, width, height):
        if type(width) == int:
            width = to_pix(width)
        if type(height) == int:
            height = to_pix(height)
        if width is not None:
            self.style['width'] = width
        if height is not None:
            self.style['height'] = height

    def set_layout_orientation(self, layout_orientation):
        self.layout_orientation = layout_orientation

    def redraw(self):
        update_event.set()

    def repr(self, client, include_children=True):
        """it is used to automatically represent the widget to HTML format
        packs all the attributes, children and so on."""
        self.attributes['style'] = jsonize(self.style)
        return super(Widget, self).repr(client, include_children)

    def append(self, value, key=''):
        """it allows to add child widgets to this.

        The key can be everything you want, in order to access to the
        specific child in this way 'widget.children[key]'.

        """
        if not isinstance(value, Widget):
            raise ValueError('value should be a Widget (otherwise use add_child(key,other)')

        key = str(id(value)) if key == '' else key
        self.add_child(key, value)

        if self.layout_orientation == Widget.LAYOUT_HORIZONTAL:
            if 'float' in self.children[key].style.keys():
                if not (self.children[key].style['float'] == 'none'):
                    self.children[key].style['float'] = 'left'
            else:
                self.children[key].style['float'] = 'left'

        return key

    def onfocus(self):
        return self.eventManager.propagate(self.EVENT_ONFOCUS, [])

    @decorate_set_on_listener("onfocus", "(self)")
    def set_on_focus_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONFOCUS] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONFOCUS)
        self.eventManager.register_listener(self.EVENT_ONFOCUS, listener, funcname)

    def onblur(self):
        return self.eventManager.propagate(self.EVENT_ONBLUR, [])

    @decorate_set_on_listener("onblur", "(self)")
    def set_on_blur_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONBLUR] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONBLUR)
        self.eventManager.register_listener(self.EVENT_ONBLUR, listener, funcname)

    def show(self, baseAppInstance):
        """Allows to show the widget as root window"""
        self.baseAppInstance = baseAppInstance
        # here the widget is set up as root, in server.gui_updater is monitored
        # this change and the new window is send to the browser
        self.oldRootWidget = self.baseAppInstance.client.root
        self.baseAppInstance.client.root = self

    def hide(self):
        """The root window is restored after a show"""
        if hasattr(self, 'baseAppInstance'):
            self.baseAppInstance.client.root = self.oldRootWidget

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    @decorate_set_on_listener("onclick", "(self)")
    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)

    def oncontextmenu(self):
        return self.eventManager.propagate(self.EVENT_ONCONTEXTMENU, [])

    @decorate_set_on_listener("oncontextmenu", "(self)")
    def set_on_contextmenu_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCONTEXTMENU] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONCONTEXTMENU)
        self.eventManager.register_listener(self.EVENT_ONCONTEXTMENU, listener, funcname)

    def onmousedown(self, x, y):
        return self.eventManager.propagate(self.EVENT_ONMOUSEDOWN, [x, y])

    @decorate_set_on_listener("onmousedown", "(self,x,y)")
    def set_on_mousedown_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONMOUSEDOWN] = \
            "var params={};"\
            "params['x']=event.clientX-this.offsetLeft;params['y']=event.clientY-this.offsetTop;"\
            "sendCallbackParam('%s','%s',params);"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONMOUSEDOWN)
        self.eventManager.register_listener(self.EVENT_ONMOUSEDOWN, listener, funcname)

    def onmouseup(self, x, y):
        return self.eventManager.propagate(self.EVENT_ONMOUSEUP, [x, y])

    @decorate_set_on_listener("onmouseup", "(self,x,y)")
    def set_on_mouseup_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONMOUSEUP] = \
            "var params={};"\
            "params['x']=event.clientX-this.offsetLeft;params['y']=event.clientY-this.offsetTop;"\
            "sendCallbackParam('%s','%s',params);"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONMOUSEUP)
        self.eventManager.register_listener(self.EVENT_ONMOUSEUP, listener, funcname)

    def onmouseout(self):
        return self.eventManager.propagate(self.EVENT_ONMOUSEOUT, [])

    @decorate_set_on_listener("onmouseout", "(self)")
    def set_on_mouseout_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONMOUSEOUT] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONMOUSEOUT)
        self.eventManager.register_listener(self.EVENT_ONMOUSEOUT, listener, funcname)

    def onmouseleave(self):
        return self.eventManager.propagate(self.EVENT_ONMOUSELEAVE, [])

    @decorate_set_on_listener("onmouseleave", "(self)")
    def set_on_mouseleave_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONMOUSELEAVE] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONMOUSELEAVE)
        self.eventManager.register_listener(self.EVENT_ONMOUSELEAVE, listener, funcname)

    def onmousemove(self, x, y):
        return self.eventManager.propagate(self.EVENT_ONMOUSEMOVE, [x, y])

    @decorate_set_on_listener("onmousemove", "(self,x,y)")
    def set_on_mousemove_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONMOUSEMOVE] = \
            "var params={};"\
            "params['x']=event.clientX-this.offsetLeft;params['y']=event.clientY-this.offsetTop;"\
            "sendCallbackParam('%s','%s',params);"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONMOUSEMOVE)
        self.eventManager.register_listener(self.EVENT_ONMOUSEMOVE, listener, funcname)

    def ontouchmove(self, x, y):
        return self.eventManager.propagate(self.EVENT_ONTOUCHMOVE, [x, y])

    @decorate_set_on_listener("ontouchmove", "(self,x,y)")
    def set_on_touchmove_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONTOUCHMOVE] = \
            "var params={};"\
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;"\
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;"\
            "sendCallbackParam('%s','%s',params);"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONTOUCHMOVE)
        self.eventManager.register_listener(self.EVENT_ONTOUCHMOVE, listener, funcname)

    def ontouchstart(self, x, y):
        return self.eventManager.propagate(self.EVENT_ONTOUCHSTART, [x, y])

    @decorate_set_on_listener("ontouchstart", "(self,x,y)")
    def set_on_touchstart_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONTOUCHSTART] = \
            "var params={};"\
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;"\
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;"\
            "sendCallbackParam('%s','%s',params);"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONTOUCHSTART)
        self.eventManager.register_listener(self.EVENT_ONTOUCHSTART, listener, funcname)

    def ontouchend(self, x, y):
        return self.eventManager.propagate(self.EVENT_ONTOUCHEND, [x, y])

    @decorate_set_on_listener("ontouchend", "(self,x,y)")
    def set_on_touchend_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONTOUCHEND] = \
            "var params={};"\
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;"\
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;"\
            "sendCallbackParam('%s','%s',params);"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONTOUCHEND)
        self.eventManager.register_listener(self.EVENT_ONTOUCHEND, listener, funcname)

    def ontouchenter(self, x, y):
        return self.eventManager.propagate(self.EVENT_ONTOUCHENTER, [x, y])

    @decorate_set_on_listener("ontouchenter", "(self,x,y)")
    def set_on_touchenter_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONTOUCHENTER] = \
            "var params={};"\
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;"\
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;"\
            "sendCallbackParam('%s','%s',params);"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONTOUCHENTER)
        self.eventManager.register_listener(self.EVENT_ONTOUCHENTER, listener, funcname)

    def ontouchleave(self):
        return self.eventManager.propagate(self.EVENT_ONTOUCHLEAVE, [])

    @decorate_set_on_listener("ontouchleave", "(self)")
    def set_on_touchleave_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONTOUCHLEAVE] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONTOUCHLEAVE)
        self.eventManager.register_listener(self.EVENT_ONTOUCHLEAVE, listener, funcname)

    def ontouchcancel(self):
        return self.eventManager.propagate(self.EVENT_ONTOUCHCANCEL, [])

    @decorate_set_on_listener("ontouchcancel", "(self)")
    def set_on_touchcancel_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONTOUCHCANCEL] = \
            "sendCallback('%s','%s');"\
            "event.stopPropagation();event.preventDefault();"\
            "return false;" % (id(self), self.EVENT_ONTOUCHCANCEL)
        self.eventManager.register_listener(self.EVENT_ONTOUCHCANCEL, listener, funcname)


class HBox(Widget):
    """ It contains widget automatically aligning them vertically. 
        Does not permit children abosulte positioning
    """
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(HBox, self).__init__(**kwargs)
        self.style['display'] = 'flex'
        self.style['-webkit-justify-content'] = 'space-around'
        self.style['justify-content'] = 'space-around'
        self.style['-webkit-align-items'] = 'center'
        self.style['align-items'] = 'center'
        self.style['flex-direction'] = 'row'

    def append(self, value, key=''):
        """it allows to add child widgets to this.

        The key allows to access the specific child in this way 'widget.children[key]'.
        The key have to be numeric and determines the child order in the layout.
        """
        key = str(key)
        if not isinstance(value, Widget):
            raise ValueError('value should be a Widget (otherwise use add_child(key,other)')

        if 'left' in value.style.keys():
            del value.style['left']
        if 'right' in value.style.keys():
            del value.style['right']

        value.style['position'] = 'static'

        value.style['-webkit-order'] = '-1'
        value.style['order'] = '-1'

        # weight of the widget in the layout
        # value.style['-webkit-flex'] =
        # value.style['-ms-flex'] =
        # value.style['flex'] =

        key = str(id(value)) if key=='' else key
        self.add_child(key, value)

        if self.layout_orientation == Widget.LAYOUT_HORIZONTAL:
            if 'float' in self.children[key].style.keys():
                if not (self.children[key].style['float'] == 'none'):
                    self.children[key].style['float'] = 'left'
            else:
                self.children[key].style['float'] = 'left'

        return key


class VBox(HBox):
    """ It contains widget automatically aligning them vertically. 
        Does not permit children abosulte positioning
    """
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(VBox, self).__init__(**kwargs)
        self.style['flex-direction'] = 'column'


class Button(Widget):
    @decorate_constructor_parameter_types([str])
    def __init__(self, text='', **kwargs):
        super(Button, self).__init__(**kwargs)
        self.type = 'button'
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.set_text(text)

    def set_text(self, t):
        self.add_child('text', t)

    def set_enabled(self, enabled):
        if enabled:
            try:
                del self.attributes['disabled']
            except KeyError:
                pass
        else:
            self.attributes['disabled'] = None


class TextInput(Widget):
    """Editable multiline/single_line text area widget"""
    @decorate_constructor_parameter_types([bool])
    def __init__(self, single_line=True, **kwargs):
        super(TextInput, self).__init__(**kwargs)
        self.type = 'textarea'

        self.EVENT_ONENTER = 'onenter'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['new_value']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self), 'evt':self.EVENT_ONCHANGE}
        self.set_text('')

        if single_line:
            self.style['resize'] = 'none'
            self.attributes['rows'] = '1'

    def set_text(self, t):
        """sets the text content."""
        self.add_child('text', t)

    def get_text(self):
        return self.get_child('text')

    def set_value(self, t):
        self.set_text(t)

    def get_value(self):
        return self.get_text()

    def onchange(self, new_value):
        """returns the new text value."""
        self.set_text(new_value)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [new_value])

    @decorate_set_on_listener("onchange", "(self,new_value)")
    def set_on_change_listener(self, listener, funcname):
        """register the listener for the onchange event."""
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)

    def onkeydown(self, new_value):
        """returns the new text value."""
        self.set_text(new_value)
        return self.eventManager.propagate(self.EVENT_ONKEYDOWN, [new_value])

    @decorate_set_on_listener("onkeydown", "(self,new_value)")
    def set_on_key_down_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONKEYDOWN] = \
            "var params={};params['new_value']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self), 'evt':self.EVENT_ONKEYDOWN}
        self.eventManager.register_listener(self.EVENT_ONKEYDOWN, listener, funcname)

    def onenter(self, new_value):
        """returns the new text value."""
        self.set_text(new_value)
        return self.eventManager.propagate(self.EVENT_ONENTER, [new_value])

    @decorate_set_on_listener("onenter", "(self,new_value)")
    def set_on_enter_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONKEYDOWN] = """
            if (event.keyCode == 13) {
                var params={};
                params['new_value']=document.getElementById('%(id)s').value;
                sendCallbackParam('%(id)s','%(evt)s',params);
                return false;
            }""" % {'id':id(self), 'evt':self.EVENT_ONENTER}
        self.eventManager.register_listener(self.EVENT_ONENTER, listener, funcname)


class Label(Widget):
    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        super(Label, self).__init__(**kwargs)
        self.type = 'p'
        self.set_text(text)

    def set_text(self, t):
        self.add_child('text', t)

    def get_text(self):
        return self.get_child('text')


class GenericDialog(Widget):

    """input dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "confirm_value" and "cancel_dialog" events."""
    @decorate_constructor_parameter_types([str, str])
    def __init__(self, title='', message='', **kwargs):
        super(GenericDialog, self).__init__(**kwargs)
        self.set_layout_orientation(Widget.LAYOUT_VERTICAL)
        self.style['display'] = 'block'
        self.style['overflow'] = 'auto'

        self.EVENT_ONCONFIRM = 'confirm_dialog'
        self.EVENT_ONCANCEL = 'cancel_dialog'

        if len(title) > 0:
            t = Label(title)
            t.style['margin'] = '5px'
            self.append(t)

        if len(message) > 0:
            m = Label(message)
            m.style['margin'] = '5px'
            self.append(m)

        self.container = Widget()
        self.container.style['display'] = 'block'
        self.container.style['overflow'] = 'auto'
        self.container.style['margin'] = '5px'
        self.container.set_layout_orientation(Widget.LAYOUT_VERTICAL)
        self.conf = Button('Ok')
        self.conf.set_size(100, 30)
        self.cancel = Button('Cancel')
        self.cancel.set_size(100, 30)
        hlay = Widget()
        hlay.style['display'] = 'block'
        hlay.style['overflow'] = 'auto'
        hlay.style['margin'] = '3px'
        hlay.append(self.conf)
        hlay.append(self.cancel)
        self.conf.style['float'] = 'right'
        self.cancel.style['float'] = 'right'

        self.append(self.container)
        self.append(hlay)

        self.conf.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCONFIRM)
        self.cancel.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCANCEL)

        self.inputs = {}

        self.baseAppInstance = None

    def add_field_with_label(self, key, label_description, field):
        self.inputs[key] = field
        label = Label(label_description)
        label.style['margin'] = '0px 5px'
        container = Widget()
        container.style['display'] = 'block'
        container.style['overflow'] = 'auto'
        container.style['padding'] = '3px'
        container.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)
        container.append(label, key='lbl' + key)
        container.append(self.inputs[key], key=key)
        self.inputs[key].style['float'] = 'right'
        self.container.append(container, key=key)

    def add_field(self, key, field):
        self.inputs[key] = field
        container = Widget()
        container.style['display'] = 'block'
        container.style['overflow'] = 'auto'
        container.style['padding'] = '3px'
        container.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)
        container.append(self.inputs[key], key=key)
        self.container.append(container, key=key)

    def get_field(self, key):
        return self.inputs[key]

    def confirm_dialog(self):
        """event called pressing on OK button.
        """
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCONFIRM, [])

    @decorate_set_on_listener("confirm_dialog", "(self)")
    def set_on_confirm_dialog_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCONFIRM, listener, funcname)

    def cancel_dialog(self):
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCANCEL, [])

    @decorate_set_on_listener("cancel_dialog", "(self)")
    def set_on_cancel_dialog_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCANCEL, listener, funcname)


class InputDialog(GenericDialog):

    """input dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "confirm_value" and "cancel_dialog" events."""
    @decorate_constructor_parameter_types([str, str, str])
    def __init__(self, title='Title', message='Message', initial_value='', **kwargs):
        super(InputDialog, self).__init__(title, message, **kwargs)

        self.inputText = TextInput()
        self.inputText.set_on_enter_listener(self, 'on_text_enter_listener')
        self.add_field('textinput', self.inputText)
        self.inputText.set_text(initial_value)

        self.EVENT_ONCONFIRMVALUE = 'confirm_value'
        self.set_on_confirm_dialog_listener(self, 'confirm_value')

    def on_text_enter_listener(self, value):
        """event called pressing on ENTER key.
        propagates the string content of the input field
        """
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, [value])

    def confirm_value(self):
        """event called pressing on OK button.
        propagates the string content of the input field
        """
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, [self.inputText.get_text()])

    @decorate_set_on_listener("confirm_value", "(self,value)")
    def set_on_confirm_value_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCONFIRMVALUE, listener, funcname)


class ListView(Widget):

    """list widget it can contain ListItems."""
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        self.type = 'ul'
        self.EVENT_ONSELECTION = 'onselection'
        self.selected_item = None
        self.selected_key = None

    @classmethod
    def new_from_list(cls, items, **kwargs):
        """
            the items are appended with an string enumeration key
        """
        obj = cls(**kwargs)
        for key, item in enumerate(items):
            obj.append(item, str(key))
        return obj

    def append(self, item, key=''):
        if isinstance(item, type('')) or isinstance(item, type(u'')):
            item = ListItem(item)
        elif not isinstance(item, ListItem):
            raise ValueError("item must be text or a ListItem instance")
        # if an event listener is already set for the added item, it will not generate a selection event
        if item.attributes[self.EVENT_ONCLICK] == '':
            item.set_on_click_listener(self, self.EVENT_ONSELECTION)
        item.attributes['selected'] = False
        super(ListView, self).append(item, key=key)

    def empty(self):
        self.selected_item = None
        self.selected_key = None
        super(ListView, self).empty()

    def onselection(self, clicked_item):
        self.selected_key = None
        for k in self.children:
            if self.children[k] == clicked_item:
                self.selected_key = k
                log.debug('ListView - onselection. Selected item key: %s' % k)
                if self.selected_item is not None:
                    self.selected_item.attributes['selected'] = False
                self.selected_item = self.children[self.selected_key]
                self.selected_item.attributes['selected'] = True
                break
        return self.eventManager.propagate(self.EVENT_ONSELECTION, [self.selected_key])

    @decorate_set_on_listener("onselection", "(self,selectedKey)")
    def set_on_selection_listener(self, listener, funcname):
        """The listener will receive the key of the selected item.
        If you add the element from an array, use a numeric incremental key
        """
        self.eventManager.register_listener(self.EVENT_ONSELECTION, listener, funcname)

    def get_value(self):
        """Returns the value of the selected item or None
        """
        if self.selected_item is None:
            return None
        return self.selected_item.get_value()

    def get_key(self):
        """Returns the key of the selected item or None
        """
        return self.selected_key

    def select_by_key(self, key):
        """
        selects an item by its key
        """
        self.selected_key = None
        self.selected_item = None
        for item in self.children.values():
            item.attributes['selected'] = False

        if key in self.children:
            self.children[key].attributes['selected'] = True
            self.selected_key = key
            self.selected_item = self.children[key]

    def set_value(self, value):
        """
        selects an item by the value of a child
        """
        self.selected_key = None
        self.selected_item = None
        for k in self.children:
            item = self.children[k]
            item.attributes['selected'] = False
            if value == item.get_value():
                self.selected_key = k
                self.selected_item = item
                self.selected_item.attributes['selected'] = True


class ListItem(Widget):

    """item widget for the ListView"""
    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        super(ListItem, self).__init__(**kwargs)
        self.type = 'li'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)

    def set_text(self, text):
        self.add_child('text', text)

    def get_text(self):
        return self.get_child('text')

    def get_value(self):
        return self.get_text()

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [self])


class DropDown(Widget):

    """combo box widget implements the onchange event.
    """
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(DropDown, self).__init__(**kwargs)
        self.type = 'select'
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self),
                                                               'evt':self.EVENT_ONCHANGE}
        self.selected_item = None
        self.selected_key = None

    def select_by_key(self, key):
        """
        selects an item by its key
        """
        for item in self.children.values():
            if 'selected' in item.attributes:
                del item.attributes['selected']
        self.children[key].attributes['selected'] = 'selected'
        self.selected_key = key
        self.selected_item = self.children[key]

    def set_value(self, value):
        """
        selects the item by the contained text
        """
        self.selected_key = None
        self.selected_item = None
        for k in self.children:
            item = self.children[k]
            if item.attributes['value'] == value:
                item.attributes['selected'] = 'selected'
                self.selected_key = k
                self.selected_item = item
            else:
                if 'selected' in item.attributes:
                    del item.attributes['selected']

    def get_value(self):
        """Returns the value of the selected item or None
        """
        if self.selected_item is None:
            return None
        return self.selected_item.get_value()

    def get_key(self):
        """Returns the key of the selected item or None
        """
        return self.selected_key

    def onchange(self, value):
        log.debug('combo box. selected %s' % value)
        self.set_value(value)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [value])

    @decorate_set_on_listener("onchange", "(self,new_value)")
    def set_on_change_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)


class DropDownItem(Widget):

    """item widget for the DropDown"""
    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        super(DropDownItem, self).__init__(**kwargs)
        self.type = 'option'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)

    def set_text(self, text):
        self.attributes['value'] = text
        self.add_child('text', text)

    def get_text(self):
        return self.attributes['value']

    def set_value(self, text):
        return self.set_text(text)

    def get_value(self):
        return self.get_text()


class Image(Widget):

    """image widget."""
    @decorate_constructor_parameter_types([str])
    def __init__(self, filename, **kwargs):
        """filename should be an URL."""
        super(Image, self).__init__(**kwargs)
        self.type = 'img'
        self.attributes['src'] = filename


class Table(Widget):

    """
    table widget - it will contains TableRow
    """
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.type = 'table'
        self.style['float'] = 'none'

    def from_2d_matrix(self, _matrix, fill_title=True):
        """
        Fills the table with the data contained in the provided 2d _matrix
        The first row of the matrix is set as table title
        """
        for child_keys in list(self.children):
            self.remove_child(self.children[child_keys])
        first_row = True
        for row in _matrix:
            tr = TableRow()
            for item in row:
                if first_row and fill_title:
                    ti = TableTitle(item)
                else:
                    ti = TableItem(item)
                tr.append(ti)
            self.append(tr)
            first_row = False


class TableRow(Widget):

    """
    row widget for the Table - it will contains TableItem
    """
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(TableRow, self).__init__(**kwargs)
        self.type = 'tr'
        self.style['float'] = 'none'


class TableItem(Widget):

    """item widget for the TableRow."""
    @decorate_constructor_parameter_types([str])
    def __init__(self, text='', **kwargs):
        super(TableItem, self).__init__(**kwargs)
        self.type = 'td'
        self.style['float'] = 'none'
        self.add_child('text', text)


class TableTitle(Widget):

    """title widget for the table."""
    @decorate_constructor_parameter_types([str])
    def __init__(self, title='', **kwargs):
        super(TableTitle, self).__init__(**kwargs)
        self.type = 'th'
        self.style['float'] = 'none'
        self.add_child('text', title)


class Input(Widget):
    @decorate_constructor_parameter_types([str, str])
    def __init__(self, input_type='', default_value='', **kwargs):
        super(Input, self).__init__(**kwargs)
        self.type = 'input'
        self.attributes['class'] = input_type

        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self),
                                                               'evt':self.EVENT_ONCHANGE}
        self.attributes['value'] = str(default_value)
        self.attributes['type'] = input_type

    def set_value(self, value):
        self.attributes['value'] = str(value)

    def get_value(self):
        """returns the new text value."""
        return self.attributes['value']

    def onchange(self, value):
        self.attributes['value'] = value
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [value])

    @decorate_set_on_listener("onchange", "(self,new_value)")
    def set_on_change_listener(self, listener, funcname):
        """register the listener for the onchange event."""
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)


class CheckBoxLabel(Widget):
    @decorate_constructor_parameter_types([str, bool, str])
    def __init__(self, label='', checked=False, user_data='', **kwargs):

        super(CheckBoxLabel, self).__init__(**kwargs)
        self.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)
        self._checkbox = CheckBox(checked, user_data)
        self._label = Label(label)
        self.append(self._checkbox, key='checkbox')
        self.append(self._label, key='label')

        self.set_value = self._checkbox.set_value
        self.get_value = self._checkbox.get_value
        self.set_on_change_listener = self._checkbox.set_on_change_listener
        self.onchange = self._checkbox.onchange


class CheckBox(Input):

    """check box widget usefull as numeric input field implements the onchange
    event.
    """
    @decorate_constructor_parameter_types([bool, str])
    def __init__(self, checked=False, user_data='', **kwargs):
        super(CheckBox, self).__init__('checkbox', user_data, **kwargs)
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(id)s').checked;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self),
                                                               'evt':self.EVENT_ONCHANGE}
        self.set_value(checked)

    def onchange(self, value):
        self.set_value(value in ('True', 'true'))
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [value])

    def set_value(self, checked):
        if checked:
            self.attributes['checked'] = 'checked'
        else:
            if 'checked' in self.attributes:
                del self.attributes['checked']

    def get_value(self):
        """returns the boolean value."""
        return 'checked' in self.attributes


class SpinBox(Input):

    """spin box widget usefull as numeric input field implements the onchange
    event.
    """
    @decorate_constructor_parameter_types([str, int, int, int])
    def __init__(self, default_value='100', min=100, max=5000, step=1, **kwargs):
        super(SpinBox, self).__init__('number', default_value, **kwargs)
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['step'] = str(step)
        self.attributes[self.EVENT_ONKEYPRESS] = \
            'return event.charCode >= 48 && event.charCode <= 57 || event.charCode == 46 || event.charCode == 13;'


class Slider(Input):
    @decorate_constructor_parameter_types([str, int, int, int])
    def __init__(self, default_value='', min=0, max=10000, step=1, **kwargs):
        super(Slider, self).__init__('range', default_value, **kwargs)
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['step'] = str(step)
        self.EVENT_ONINPUT = 'oninput'

    def oninput(self, value):
        return self.eventManager.propagate(self.EVENT_ONINPUT, [value])

    @decorate_set_on_listener("oninput", "(self,new_value)")
    def set_oninput_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONINPUT] = \
            "var params={};params['value']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self), 'evt':self.EVENT_ONINPUT}
        self.eventManager.register_listener(self.EVENT_ONINPUT, listener, funcname)


class ColorPicker(Input):
    @decorate_constructor_parameter_types([str])
    def __init__(self, default_value='#995500', **kwargs):
        super(ColorPicker, self).__init__('color', default_value, **kwargs)


class Date(Input):
    @decorate_constructor_parameter_types([str])
    def __init__(self, default_value='2015-04-13', **kwargs):
        super(Date, self).__init__('date', default_value, **kwargs)


class GenericObject(Widget):

    """
    GenericObject widget - allows to show embedded object like pdf,swf..
    """
    @decorate_constructor_parameter_types([str])
    def __init__(self, filename, **kwargs):
        """filename should be an URL."""
        super(GenericObject, self).__init__(**kwargs)
        self.type = 'object'
        self.attributes['data'] = filename


class FileFolderNavigator(Widget):

    """FileFolderNavigator widget."""
    @decorate_constructor_parameter_types([bool, str, bool, bool])
    def __init__(self, multiple_selection, selection_folder, allow_file_selection, allow_folder_selection, **kwargs):
        super(FileFolderNavigator, self).__init__(**kwargs)
        self.set_layout_orientation(Widget.LAYOUT_VERTICAL)

        self.multiple_selection = multiple_selection
        self.allow_file_selection = allow_file_selection 
        self.allow_folder_selection = allow_folder_selection
        self.selectionlist = []
        self.controlsContainer = Widget()
        self.controlsContainer.set_size('100%', '30px')
        self.controlsContainer.style['display'] = 'flex'
        self.controlsContainer.set_layout_orientation(Widget.LAYOUT_VERTICAL)
        self.controlBack = Button('Up')
        self.controlBack.set_size('10%', '100%')
        self.controlBack.set_on_click_listener(self, 'dir_go_back')
        self.controlGo = Button('Go >>')
        self.controlGo.set_size('10%', '100%')
        self.controlGo.set_on_click_listener(self, 'dir_go')
        self.pathEditor = TextInput()
        self.pathEditor.set_size('80%', '100%')
        self.pathEditor.style['resize'] = 'none'
        self.pathEditor.attributes['rows'] = '1'
        self.controlsContainer.append(self.controlBack)
        self.controlsContainer.append(self.pathEditor)
        self.controlsContainer.append(self.controlGo)

        self.itemContainer = Widget()

        self.append(self.controlsContainer)
        self.append(self.itemContainer, key='items')  # defined key as this is replaced later

        self.folderItems = list()

        # fixme: we should use full paths and not all this chdir stuff
        self.chdir(selection_folder)  # move to actual working directory

    def get_selection_list(self):
        return self.selectionlist

    def populate_folder_items(self, directory):
        def _sort_files(a, b):
            if os.path.isfile(a) and os.path.isdir(b):
                return 1
            elif os.path.isfile(b) and os.path.isdir(a):
                return -1
            else:
                try:
                    if a[0] == '.':
                        a = a[1:]
                    if b[0] == '.':
                        b = b[1:]
                    return a.lower() > b.lower()
                except (IndexError, ValueError):
                    return a > b

        log.debug("FileFolderNavigator - populate_folder_items")

        l = os.listdir(directory)
        l.sort(key=cmp_to_key(_sort_files))

        # used to restore a valid path after a wrong edit in the path editor
        self.lastValidPath = directory 
        # we remove the container avoiding graphic update adding items
        # this speeds up the navigation
        self.remove_child(self.itemContainer)
        # creation of a new instance of a itemContainer
        self.itemContainer = Widget()
        self.itemContainer.set_layout_orientation(Widget.LAYOUT_VERTICAL)
        self.itemContainer.style['overflow-y'] = 'scroll'
        self.itemContainer.style['overflow-x'] = 'hidden'
        self.itemContainer.style['height'] = '300px'
        self.itemContainer.style['display'] = 'block'

        for i in l:
            full_path = os.path.join(directory, i)
            is_folder = not os.path.isfile(full_path)
            if (not is_folder) and (not self.allow_file_selection):
                continue
            fi = FileFolderItem(i, is_folder)
            fi.style['display'] = 'block'
            fi.set_on_click_listener(self, 'on_folder_item_click')  # navigation purpose
            fi.set_on_selection_listener(self, 'on_folder_item_selected')  # selection purpose
            self.folderItems.append(fi)
            self.itemContainer.append(fi)
        self.append(self.itemContainer, key='items')  # replace the old widget

    def dir_go_back(self):
        curpath = os.getcwd()  # backup the path
        try:
            os.chdir(self.pathEditor.get_text())
            os.chdir('..')
            self.chdir(os.getcwd())
        except Exception as e:
            self.pathEditor.set_text(self.lastValidPath)
            log.error('error changing directory', exc_info=True)
        os.chdir(curpath)  # restore the path

    def dir_go(self):
        # when the GO button is pressed, it is supposed that the pathEditor is changed
        curpath = os.getcwd()  # backup the path
        try:
            os.chdir(self.pathEditor.get_text())
            self.chdir(os.getcwd())
        except Exception as e:
            log.error('error going to directory', exc_info=True)
            self.pathEditor.set_text(self.lastValidPath)
        os.chdir(curpath)  # restore the path

    def chdir(self, directory):
        curpath = os.getcwd()  # backup the path
        log.debug("FileFolderNavigator - chdir: %s" % directory)
        for c in self.folderItems:
            self.itemContainer.remove_child(c)  # remove the file and folders from the view
        self.folderItems = []
        self.selectionlist = []  # reset selected file list
        os.chdir(directory)
        directory = os.getcwd()
        self.populate_folder_items(directory)
        self.pathEditor.set_text(directory)
        os.chdir(curpath)  # restore the path

    def on_folder_item_selected(self, folderitem):
        if folderitem.isFolder and (not self.allow_folder_selection):
            folderitem.set_selected(False)
            return

        if not self.multiple_selection:
            self.selectionlist = []
            for c in self.folderItems:
                c.set_selected(False)
            folderitem.set_selected(True)
        log.debug("FileFolderNavigator - on_folder_item_click")
        # when an item is clicked it is added to the file selection list
        f = os.path.join(self.pathEditor.get_text(), folderitem.get_text())
        if f in self.selectionlist:
            self.selectionlist.remove(f)
        else:
            self.selectionlist.append(f)

    def on_folder_item_click(self, folderitem):
        log.debug("FileFolderNavigator - on_folder_item_dblclick")
        # when an item is clicked two time
        f = os.path.join(self.pathEditor.get_text(), folderitem.get_text())
        if not os.path.isfile(f):
            self.chdir(f)

    def get_selected_filefolders(self):
        return self.selectionlist


class FileFolderItem(Widget):

    """FileFolderItem widget for the FileFolderNavigator"""
    @decorate_constructor_parameter_types([str, bool])
    def __init__(self, text, is_folder=False, **kwargs):
        super(FileFolderItem, self).__init__(**kwargs)
        super(FileFolderItem, self).set_layout_orientation(Widget.LAYOUT_HORIZONTAL)
        self.style['margin'] = '3px'
        self.isFolder = is_folder
        self.EVENT_ONSELECTION = 'onselection'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.icon = Widget()
        self.icon.set_size(30, 30)
        # the icon click activates the onselection event, that is propagates to registered listener
        if is_folder:
            self.icon.set_on_click_listener(self, self.EVENT_ONCLICK)
        self.icon.attributes['class'] = 'FileFolderItemIcon'
        icon_file = 'res/folder.png' if is_folder else 'res/file.png'
        self.icon.style['background-image'] = "url('%s')" % icon_file
        self.label = Label(text)
        self.label.set_size(400, 30)
        self.label.set_on_click_listener(self, self.EVENT_ONSELECTION)
        self.append(self.icon, key='icon')
        self.append(self.label, key='text')
        self.selected = False

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [self])

    @decorate_set_on_listener("onclick", "(self,folderItemInstance)")
    def set_on_click_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)

    def set_selected(self, selected):
        self.selected = selected
        self.style['color'] = 'red' if self.selected else 'black'

    def onselection(self):
        self.set_selected(not self.selected)
        return self.eventManager.propagate(self.EVENT_ONSELECTION, [self])

    @decorate_set_on_listener("onselection", "(self,folderItemInstance)")
    def set_on_selection_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONSELECTION, listener, funcname)

    def set_text(self, t):
        """sets the text content."""
        self.children['text'].set_text(t)

    def get_text(self):
        return self.children['text'].get_text()


class FileSelectionDialog(GenericDialog):

    """file selection dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "confirm_value" and "cancel_dialog" events."""
    @decorate_constructor_parameter_types([str, str, bool, str, bool, bool])
    def __init__(self, title='File dialog', message='Select files and folders', 
                 multiple_selection=True, selection_folder='.', 
                 allow_file_selection=True, allow_folder_selection=True, **kwargs):
        super(FileSelectionDialog, self).__init__(title, message, **kwargs)

        self.style['width'] = '475px'
        self.fileFolderNavigator = FileFolderNavigator(multiple_selection, selection_folder,
                                                       allow_file_selection, 
                                                       allow_folder_selection)
        self.add_field('fileFolderNavigator', self.fileFolderNavigator)
        self.EVENT_ONCONFIRMVALUE = 'confirm_value'
        self.set_on_confirm_dialog_listener(self, 'confirm_value')

    def confirm_value(self):
        """event called pressing on OK button.
           propagates the string content of the input field
        """
        self.hide()
        params = [self.fileFolderNavigator.get_selection_list()]
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, params)

    @decorate_set_on_listener("confirm_value", "(self,fileList)")
    def set_on_confirm_value_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCONFIRMVALUE, listener, funcname)


class MenuBar(Widget):
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        self.type = 'nav'
        self.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)


class Menu(Widget):

    """Menu widget can contain MenuItem."""
    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.type = 'ul'
        self.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)


class MenuItem(Widget):

    """MenuItem widget can contain other MenuItem."""
    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        super(MenuItem, self).__init__(**kwargs)
        self.sub_container = None
        self.type = 'li'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)

    def append(self, value, key=''):
        if self.sub_container is None:
            self.sub_container = Menu()
            super(MenuItem, self).append(self.sub_container, key='subcontainer')
        self.sub_container.append(value, key=key)

    def set_text(self, text):
        self.add_child('text', text)

    def get_text(self):
        return self.get_child('text')


class FileUploader(Widget):

    """
    FileUploader widget:
        allows to upload multiple files to a specified folder.
        implements the onsuccess and onfailed events.
    """
    @decorate_constructor_parameter_types([str, bool])
    def __init__(self, savepath='./', multiple_selection_allowed=False, **kwargs):
        super(FileUploader, self).__init__(**kwargs)
        self._savepath = savepath
        self._multiple_selection_allowed = multiple_selection_allowed
        self.type = 'input'
        self.attributes['type'] = 'file'
        if multiple_selection_allowed:
            self.attributes['multiple'] = 'multiple'
        self.attributes['accept'] = '*.*'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.EVENT_ON_SUCCESS = 'onsuccess'
        self.EVENT_ON_FAILED = 'onfailed'

        self.attributes[self.EVENT_ONCHANGE] = \
            "var files = this.files;"\
            "for(var i=0; i<files.length; i++){"\
            "uploadFile('%(id)s','%(evt_success)s','%(evt_failed)s','%(savepath)s',files[i]);}" % {
                'id':id(self), 'evt_success':self.EVENT_ON_SUCCESS, 'evt_failed':self.EVENT_ON_FAILED,
                'savepath':self._savepath}

    def onsuccess(self, filename):
        return self.eventManager.propagate(self.EVENT_ON_SUCCESS, [filename])

    @decorate_set_on_listener("onsuccess", "(self,filename)")
    def set_on_success_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ON_SUCCESS, listener, funcname)

    def onfailed(self, filename):
        return self.eventManager.propagate(self.EVENT_ON_FAILED, [filename])

    @decorate_set_on_listener("onfailed", "(self,filename)")
    def set_on_failed_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ON_FAILED, listener, funcname)


class FileDownloader(Widget):

    """FileDownloader widget. Allows to start a file download."""
    @decorate_constructor_parameter_types([str, str, str])
    def __init__(self, text, filename, path_separator='/', **kwargs):
        super(FileDownloader, self).__init__(**kwargs)
        self.type = 'a'
        self.attributes['download'] = os.path.basename(filename)
        self.attributes['href'] = "/%s/download" % id(self)
        self.set_text(text)
        self._filename = filename
        self._path_separator = path_separator

    def set_text(self, t):
        self.add_child('text', t)

    def download(self):
        with open(self._filename, 'r+b') as f:
            content = f.read()
        headers = {'Content-type':'application/octet-stream',
                   'Content-Disposition':'attachment; filename=%s' % os.path.basename(self._filename)}
        return [content, headers]


class Link(Widget):
    @decorate_constructor_parameter_types([str, str, bool])
    def __init__(self, url, text, open_new_window=True, **kwargs):
        super(Link, self).__init__(**kwargs)
        self.type = 'a'
        self.attributes['href'] = url
        if open_new_window:
            self.attributes['target'] = "_blank"
        self.set_text(text)

    def set_text(self, t):
        self.add_child('text', t)

    def get_text(self):
        return self.get_child('text')

    def get_url(self):
        return self.attributes['href']


class VideoPlayer(Widget):
    @decorate_constructor_parameter_types([str, str])
    def __init__(self, video, poster=None, **kwargs):
        super(VideoPlayer, self).__init__(**kwargs)
        self.type = 'video'
        self.attributes['src'] = video
        self.attributes['preload'] = 'auto'
        self.attributes['controls'] = None
        self.attributes['poster'] = poster


class Svg(Widget):
    @decorate_constructor_parameter_types([int, int])
    def __init__(self, width, height, **kwargs):
        super(Svg, self).__init__(**kwargs)
        self.set_size(width, height)
        self.attributes['width'] = width
        self.attributes['height'] = height
        self.type = 'svg'

    def set_viewbox(self, x, y, w, h):
        self.attributes['viewBox'] = "%s %s %s %s" % (x, y, w, h)
        self.attributes['preserveAspectRatio'] = 'none'


class SvgCircle(Widget):
    @decorate_constructor_parameter_types([int, int, int])
    def __init__(self, x, y, radix, **kwargs):
        super(SvgCircle, self).__init__(**kwargs)
        self.set_position(x, y)
        self.set_radix(radix)
        self.set_stroke()
        self.type = 'circle'

    def set_position(self, x, y):
        self.attributes['cx'] = x
        self.attributes['cy'] = y

    def set_radix(self, radix):
        self.attributes['r'] = radix

    def set_stroke(self, width=1, color='black'):
        self.attributes['stroke'] = color
        self.attributes['stroke-width'] = str(width)

    def set_fill(self, color):
        self.attributes['fill'] = color


class SvgLine(Widget):
    @decorate_constructor_parameter_types([int, int, int, int])
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super(SvgLine, self).__init__(**kwargs)
        self.set_coords(x1, y1, x2, y2)
        self.set_stroke()
        self.type = 'line'

    def set_coords(self, x1, y1, x2, y2):
        self.set_p1(x1, y1)
        self.set_p2(x2, y2)

    def set_p1(self, x1, y1):
        self.attributes['x1'] = x1
        self.attributes['y1'] = y1

    def set_p2(self, x2, y2):
        self.attributes['x2'] = x2
        self.attributes['y2'] = y2

    def set_stroke(self, width=1, color='black'):
        self.style['stroke'] = color
        self.style['stroke-width'] = str(width)


class SvgPolyline(Widget):
    @decorate_constructor_parameter_types([int])
    def __init__(self, _maxlen=None, **kwargs):
        super(SvgPolyline, self).__init__(**kwargs)
        self.set_stroke()
        self.style['fill'] = 'none'
        self.type = 'polyline'
        self.coordsX = collections.deque(maxlen=_maxlen)
        self.coordsY = collections.deque(maxlen=_maxlen)
        self.maxlen = _maxlen  # no limit
        self.attributes['points'] = ''
        self.attributes['vector-effect'] = 'non-scaling-stroke'

    def add_coord(self, x, y):
        if len(self.coordsX) == self.maxlen:
            spacepos = self.attributes['points'].find(' ')
            if spacepos > 0:
                self.attributes['points'] = self.attributes['points'][spacepos + 1:]
        self.coordsX.append(x)
        self.coordsY.append(y)
        self.attributes['points'] += "%s,%s " % (x, y)

    def set_stroke(self, width=1, color='black'):
        self.style['stroke'] = color
        self.style['stroke-width'] = str(width)


class SvgText(Widget):
    @decorate_constructor_parameter_types([int, int, str])
    def __init__(self, x, y, text, **kwargs):
        super(SvgText, self).__init__(**kwargs)
        self.type = 'text'
        self.set_position(x, y)
        self.set_fill()
        self.set_text(text)

    def set_text(self, text):
        self.add_child('text', text)

    def set_position(self, x, y):
        self.attributes['x'] = str(x)
        self.attributes['y'] = str(y)

    def set_fill(self, color='black'):
        self.attributes['fill'] = color
