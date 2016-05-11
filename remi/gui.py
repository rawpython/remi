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


def decorate_set_on_listener(event_name, params):
    """ private decorator for use in the editor

    Args:
        event_name (str): Name of the event to which it refers (es. For set_on_click_listener the event_name is "onclick"
        params (str): The list of parameters for the listener function (es. "(self, new_value)")
    """

    def add_annotation(function):
        function._event_listener = {}
        function._event_listener['eventName'] = event_name
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


class _VersionedDictionary(dict):
    """This dictionary allows to check if its content is changed.
       It has an attribute __version__ of type int that increments every change
    """
    def __init__(self, *args, **kwargs):
        self.__version__ = 0
        super(_VersionedDictionary, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value, version_increment=1):
        if key in self:
            if self[key] == value:
                return
        self.__version__ += version_increment
        return super(_VersionedDictionary, self).__setitem__(key, value)

    def __delitem__(self, key, version_increment=1):
        if not key in self:
            return
        self.__version__ += version_increment
        return super(_VersionedDictionary, self).__delitem__(key)
    
    def pop(self, key, d=None, version_increment=1):
        if not key in self:
            return
        self.__version__ += version_increment
        return super(_VersionedDictionary, self).pop(key, d)
        
    def clear(self, version_increment=1):
        self.__version__ += version_increment
        return super(_VersionedDictionary, self).clear()


class _EventManager(object):
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
        """register a listener for a specific event

        Args:
            eventname (str): The event identifier, like Widget.EVENT_ONCLICK that is 'onclick'.
            instance (Widget or App): The widget or app instance that will listen for an event.
            funcname (str): The literal function name, member of *instance* that will be called on event.
        """
        self.listeners[eventname] = {'instance': instance, 'funcname': funcname}


class Tag(object):
    """
    Tag is the base class of the framework. It represents an element that can be added to the GUI,
    but it is not necessarily graphically representable.
    You can use this class for sending javascript code to the clients.
    """
    def __init__(self, **kwargs):
        """
        Args:
           _type (str): HTML element type or ''
           _class (str): CSS class or '' (defaults to Class.__name__)
        """
        self.kwargs = kwargs
        # the runtime instances are processed every time a requests arrives, searching for the called method
        # if a class instance is not present in the runtimeInstances, it will
        # we not callable
        runtimeInstances[str(id(self))] = self

        self._render_children_list = []

        self.children = _VersionedDictionary()
        self.attributes = _VersionedDictionary()  # properties as class id style
        self.style = _VersionedDictionary()  # used by Widget, but instantiated here to make gui_updater simpler

        self.type = kwargs.get('_type', '')
        self.attributes['id'] = str(id(self))

        cls = kwargs.get('_class', self.__class__.__name__)
        if cls:
            self._classes = [cls]
        else:
            self._classes = []

    @property
    def identifier(self):
        return self.attributes['id']

    def repr(self, client, include_children=True):
        """It is used to automatically represent the object to HTML format
        packs all the attributes, children and so on.

        Args:
            client (App): The client instance.
            include_children (bool): Specifies if the children have to be represented too.
        """

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

        html = '<%s %s %s>%s</%s>' % (self.type,
                                   ' '.join('%s="%s"' % (k, v) if v is not None else k for k, v in
                                            self.attributes.items()),
                                   ('class="%s"' % ' '.join(self._classes)) if self._classes else '',
                                   innerHTML,
                                   self.type)
        return html

    def add_class(self, cls):
        self._classes.append(cls)

    def remove_class(self, cls):
        try:
            self._classes.remove(cls)
        except ValueError:
            pass

    def add_child(self, key, child):
        """Adds a child to the Tag

        To retrieve the child call get_child or access to the Tag.children[key] dictionary.

        Args:
            key (str):  Unique child's identifier
            child (Tag, str):
        """
        if hasattr(child, 'attributes'):
            child.attributes['parent_widget'] = str(id(self))

        if key in self.children:
            self._render_children_list.remove(self.children[key])
        self._render_children_list.append(child)

        self.children[key] = child

    def get_child(self, key):
        """Returns the child identified by 'key'

        Args:
            key (str): Unique identifier of the child.
        """
        return self.children[key]

    def empty(self):
        """remove all children from the widget"""
        for k in list(self.children.keys()):
            self.remove_child(self.children[k])

    def remove_child(self, child):
        """Removes a child instance from the Tag's children.

        Args:
            child (Tag): The child to be removed.
        """
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
    """Base class for gui widgets.

    Widget can be used as generic container. You can add children by the append(value, key) function.
    Widget can be arranged in absolute positioning (assigning style['top'] and style['left'] attributes to the children
    or in a simple auto-alignment.
    You can decide the horizontal or vertical arrangement by the function set_layout_horientation(layout_orientation)
    passing as parameter Widget.LAYOUT_HORIZONTAL or Widget.LAYOUT_VERTICAL.

    Tips:
    In html, it is a DIV tag    
    The self.type attribute specifies the HTML tag representation
    The self.attributes[] attribute specifies the HTML attributes like 'style' 'class' 'id'
    The self.style[] attribute specifies the CSS style content like 'font' 'color'. It will be packed together with
    'self.attributes'.
    """

    # constants
    LAYOUT_HORIZONTAL = True
    LAYOUT_VERTICAL = False

    # some constants for the events
    EVENT_ONCLICK = 'onclick'
    EVENT_ONDBLCLICK = 'ondblclick'
    EVENT_ONMOUSEDOWN = 'onmousedown'
    EVENT_ONMOUSEMOVE = 'onmousemove'
    EVENT_ONMOUSEOVER = 'onmouseover'
    EVENT_ONMOUSEOUT = 'onmouseout'
    EVENT_ONMOUSELEAVE = 'onmouseleave'
    EVENT_ONMOUSEUP = 'onmouseup'
    EVENT_ONTOUCHMOVE = 'ontouchmove'
    EVENT_ONTOUCHSTART = 'ontouchstart'
    EVENT_ONTOUCHEND = 'ontouchend'
    EVENT_ONTOUCHENTER = 'ontouchenter'
    EVENT_ONTOUCHLEAVE = 'ontouchleave'
    EVENT_ONTOUCHCANCEL = 'ontouchcancel'
    EVENT_ONKEYDOWN = 'onkeydown'
    EVENT_ONKEYPRESS = 'onkeypress'
    EVENT_ONKEYUP = 'onkeyup'
    EVENT_ONCHANGE = 'onchange'
    EVENT_ONFOCUS = 'onfocus'
    EVENT_ONBLUR = 'onblur'
    EVENT_ONCONTEXTMENU = "oncontextmenu"
    EVENT_ONUPDATE = 'onupdate'

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        """
        Args:
            width (int, str): An optional width for the widget (es. width=10 or width='10px' or width='10%').
            height (int, str): An optional height for the widget (es. height=10 or height='10px' or height='10%').
            margin (str): CSS margin specifier
            layout_orientation (Widget.LAYOUT_VERTICAL, Widget.LAYOUT_HORIZONTAL): Widget layout, only honoured for
                some widget types
        """
        if '_type' not in kwargs:
            kwargs['_type'] = 'div'

        super(Widget, self).__init__(**kwargs)

        self.eventManager = _EventManager()
        self.oldRootWidget = None  # used when hiding the widget

        self.style['margin'] = kwargs.get('margin', '0px auto')  # centers the div
        self.set_layout_orientation(kwargs.get('layout_orientation', Widget.LAYOUT_VERTICAL))
        self.set_size(kwargs.get('width'), kwargs.get('height'))

    def set_size(self, width, height):
        """Set the widget size.

        Args:
            width (int or str): An optional width for the widget (es. width=10 or width='10px' or width='10%').
            height (int or str): An optional height for the widget (es. height=10 or height='10px' or height='10%').
        """
        if width is not None:
            try:
                width = to_pix(int(width))
            except ValueError:
                # now we know w has 'px or % in it'
                pass
            self.style['width'] = width

        if height is not None:
            try:
                height = to_pix(int(height))
            except ValueError:
                # now we know w has 'px or % in it'
                pass
            self.style['height'] = height

    def set_layout_orientation(self, layout_orientation):
        """For the generic Widget, this function allows to setup the children arrangement.

        Args:
            layout_orientation (Widget.LAYOUT_HORIZONTAL or Widget.LAYOUT_VERTICAL):
        """
        self.layout_orientation = layout_orientation

    def redraw(self):
        """Forces a graphic update of the widget"""
        update_event.set()

    def repr(self, client, include_children=True):
        """Represents the widget as HTML format, packs all the attributes, children and so on.

        Args:
            client (App): Client instance.
            include_children (bool): Determines if the children have to be represented together with this Widget.
        """
        self.attributes['style'] = jsonize(self.style)
        return super(Widget, self).repr(client, include_children)

    def append(self, value, key=''):
        """Adds a child widget, generating and returning a key if not provided

        In order to access to the specific child in this way widget.children[key].

        Args:
            value (Tag or Widget): The child to be appended.
            key (str): The unique string identifier for the child or ''

        Returns:
            str: a key used to refer to the child for all future interaction
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
        """Called when the Widget gets focus."""
        return self.eventManager.propagate(self.EVENT_ONFOCUS, [])

    @decorate_set_on_listener("onfocus", "(self)")
    def set_on_focus_listener(self, listener, funcname):
        """Registers the listener for the Widget.onfocus event.

        Args:
            listener (App, Widget): Instance of the listener
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONFOCUS] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONFOCUS)
        self.eventManager.register_listener(self.EVENT_ONFOCUS, listener, funcname)

    def onblur(self):
        """Called when the Widget loses focus"""
        return self.eventManager.propagate(self.EVENT_ONBLUR, [])

    @decorate_set_on_listener("onblur", "(self)")
    def set_on_blur_listener(self, listener, funcname):
        """Registers the listener for the Widget.onblur event.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONBLUR] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONBLUR)
        self.eventManager.register_listener(self.EVENT_ONBLUR, listener, funcname)

    def show(self, baseAppInstance):
        """Sets this widget as the root widget on the supplied app instance

        Args:
            baseAppInstance (App):
        """
        self.baseAppInstance = baseAppInstance
        # here the widget is set up as root, in server.gui_updater is monitored
        # this change and the new window is send to the browser
        self.oldRootWidget = self.baseAppInstance.client.root
        self.baseAppInstance.client.root = self

    def hide(self):
        """Hide the widget. The root window is shown."""
        if hasattr(self, 'baseAppInstance'):
            self.baseAppInstance.client.root = self.oldRootWidget

    def onclick(self):
        """Called when the Widget gets clicked by the user with the left mouse button."""
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    @decorate_set_on_listener("onclick", "(self)")
    def set_on_click_listener(self, listener, funcname):
        """Registers the listener for the Widget.onclick event.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONCLICK] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)

    def oncontextmenu(self):
        """Called when the Widget gets clicked by the user with the right mouse button.
        """
        return self.eventManager.propagate(self.EVENT_ONCONTEXTMENU, [])

    @decorate_set_on_listener("oncontextmenu", "(self)")
    def set_on_contextmenu_listener(self, listener, funcname):
        """Registers the listener for the Widget.oncontextmenu event.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONCONTEXTMENU] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONCONTEXTMENU)
        self.eventManager.register_listener(self.EVENT_ONCONTEXTMENU, listener, funcname)

    def onmousedown(self, x, y):
        """Called when the user presses left or right mouse button over a Widget.
        """
        return self.eventManager.propagate(self.EVENT_ONMOUSEDOWN, [x, y])

    @decorate_set_on_listener("onmousedown", "(self,x,y)")
    def set_on_mousedown_listener(self, listener, funcname):
        """Registers the listener for the Widget.onmousedown event.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONMOUSEDOWN] = \
            "var params={};" \
            "params['x']=event.clientX-this.offsetLeft;" \
            "params['y']=event.clientY-this.offsetTop;" \
            "sendCallbackParam('%s','%s',params);" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONMOUSEDOWN)
        self.eventManager.register_listener(self.EVENT_ONMOUSEDOWN, listener, funcname)

    def onmouseup(self, x, y):
        """Called when the user releases left or right mouse button over a Widget.
        """
        return self.eventManager.propagate(self.EVENT_ONMOUSEUP, [x, y])

    @decorate_set_on_listener("onmouseup", "(self,x,y)")
    def set_on_mouseup_listener(self, listener, funcname):
        """Registers the listener for the Widget.onmouseup event.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONMOUSEUP] = \
            "var params={};" \
            "params['x']=event.clientX-this.offsetLeft;" \
            "params['y']=event.clientY-this.offsetTop;" \
            "sendCallbackParam('%s','%s',params);" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONMOUSEUP)
        self.eventManager.register_listener(self.EVENT_ONMOUSEUP, listener, funcname)

    def onmouseout(self):
        """Called when the mouse cursor moves outside a Widget.

        Note: This event is often used together with the Widget.onmouseover event, which occurs when the pointer is
            moved onto a Widget, or onto one of its children.
        """
        return self.eventManager.propagate(self.EVENT_ONMOUSEOUT, [])

    @decorate_set_on_listener("onmouseout", "(self)")
    def set_on_mouseout_listener(self, listener, funcname):
        """Registers the listener for the Widget.onmouseout event.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONMOUSEOUT] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONMOUSEOUT)
        self.eventManager.register_listener(self.EVENT_ONMOUSEOUT, listener, funcname)

    def onmouseleave(self):
        """Called when the mouse cursor moves outside a Widget.

        Note: This event is often used together with the Widget.onmouseenter event, which occurs when the mouse pointer
            is moved onto a Widget.

        Note: The Widget.onmouseleave event is similar to the Widget.onmouseout event. The only difference is that the
            onmouseleave event does not bubble (does not propagate up the Widgets tree).
        """
        return self.eventManager.propagate(self.EVENT_ONMOUSELEAVE, [])

    @decorate_set_on_listener("onmouseleave", "(self)")
    def set_on_mouseleave_listener(self, listener, funcname):
        """Registers the listener for the Widget.onmouseleave event.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONMOUSELEAVE] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONMOUSELEAVE)
        self.eventManager.register_listener(self.EVENT_ONMOUSELEAVE, listener, funcname)

    def onmousemove(self, x, y):
        """Called when the mouse cursor moves inside the Widget.

        Args:
            x (int): position of the mouse inside the widget
            y (int): position of the mouse inside the widget
        """
        return self.eventManager.propagate(self.EVENT_ONMOUSEMOVE, [x, y])

    @decorate_set_on_listener("onmousemove", "(self,x,y)")
    def set_on_mousemove_listener(self, listener, funcname):
        """Registers the listener for the Widget.onmousemove event.
        Note: the listener prototype have to be in the form on_widget_mousemove(self, x, y)

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONMOUSEMOVE] = \
            "var params={};" \
            "params['x']=event.clientX-this.offsetLeft;" \
            "params['y']=event.clientY-this.offsetTop;" \
            "sendCallbackParam('%s','%s',params);" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONMOUSEMOVE)
        self.eventManager.register_listener(self.EVENT_ONMOUSEMOVE, listener, funcname)

    def ontouchmove(self, x, y):
        """Called continuously while a finger is dragged across the screen, over a Widget.

        Args:
            x (int): position of the finger inside the widget
            y (int): position of the finger inside the widget
        """
        return self.eventManager.propagate(self.EVENT_ONTOUCHMOVE, [x, y])

    @decorate_set_on_listener("ontouchmove", "(self,x,y)")
    def set_on_touchmove_listener(self, listener, funcname):
        """Registers the listener for the Widget.ontouchmove event.
        Note: the listener prototype have to be in the form on_widget_touchmove(self, x, y)

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONTOUCHMOVE] = \
            "var params={};" \
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;" \
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;" \
            "sendCallbackParam('%s','%s',params);" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONTOUCHMOVE)
        self.eventManager.register_listener(self.EVENT_ONTOUCHMOVE, listener, funcname)

    def ontouchstart(self, x, y):
        """Called when a finger touches the widget.

        Args:
            x (int): position of the finger inside the widget
            y (int): position of the finger inside the widget
        """
        return self.eventManager.propagate(self.EVENT_ONTOUCHSTART, [x, y])

    @decorate_set_on_listener("ontouchstart", "(self,x,y)")
    def set_on_touchstart_listener(self, listener, funcname):
        """Registers the listener for the Widget.ontouchstart event.
        Note: the listener prototype have to be in the form on_widget_touchstart(self, x, y)

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONTOUCHSTART] = \
            "var params={};" \
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;" \
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;" \
            "sendCallbackParam('%s','%s',params);" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONTOUCHSTART)
        self.eventManager.register_listener(self.EVENT_ONTOUCHSTART, listener, funcname)

    def ontouchend(self, x, y):
        """Called when a finger is released from the widget.

        Args:
            x (int): position of the finger inside the widget
            y (int): position of the finger inside the widget
        """
        return self.eventManager.propagate(self.EVENT_ONTOUCHEND, [x, y])

    @decorate_set_on_listener("ontouchend", "(self,x,y)")
    def set_on_touchend_listener(self, listener, funcname):
        """Registers the listener for the Widget.ontouchend event.
        Note: the listener prototype have to be in the form on_widget_touchend(self, x, y)

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONTOUCHEND] = \
            "var params={};" \
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;" \
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;" \
            "sendCallbackParam('%s','%s',params);" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONTOUCHEND)
        self.eventManager.register_listener(self.EVENT_ONTOUCHEND, listener, funcname)

    def ontouchenter(self, x, y):
        """Called when a finger touches from outside to inside the widget.

        Args:
            x (int): position of the finger inside the widget
            y (int): position of the finger inside the widget
        """
        return self.eventManager.propagate(self.EVENT_ONTOUCHENTER, [x, y])

    @decorate_set_on_listener("ontouchenter", "(self,x,y)")
    def set_on_touchenter_listener(self, listener, funcname):
        """Registers the listener for the Widget.ontouchenter event.

        Note: the listener prototype have to be in the form on_widget_touchenter(self, x, y)

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONTOUCHENTER] = \
            "var params={};" \
            "params['x']=parseInt(event.changedTouches[0].clientX)-this.offsetLeft;" \
            "params['y']=parseInt(event.changedTouches[0].clientY)-this.offsetTop;" \
            "sendCallbackParam('%s','%s',params);" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONTOUCHENTER)
        self.eventManager.register_listener(self.EVENT_ONTOUCHENTER, listener, funcname)

    def ontouchleave(self):
        """Called when a finger touches from inside to outside the widget.
        """
        return self.eventManager.propagate(self.EVENT_ONTOUCHLEAVE, [])

    @decorate_set_on_listener("ontouchleave", "(self)")
    def set_on_touchleave_listener(self, listener, funcname):
        """Registers the listener for the Widget.ontouchleave event.
        Note: the listener prototype have to be in the form on_widget_touchleave(self)

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONTOUCHLEAVE] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONTOUCHLEAVE)
        self.eventManager.register_listener(self.EVENT_ONTOUCHLEAVE, listener, funcname)

    def ontouchcancel(self):
        """Called when a touch point has been disrupted in an implementation-specific manner
        (for example, too many touch points are created).
        """
        return self.eventManager.propagate(self.EVENT_ONTOUCHCANCEL, [])

    @decorate_set_on_listener("ontouchcancel", "(self)")
    def set_on_touchcancel_listener(self, listener, funcname):
        """Registers the listener for the Widget.ontouchcancel event.

        Note: the listener prototype have to be in the form on_widget_touchcancel(self)

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONTOUCHCANCEL] = \
            "sendCallback('%s','%s');" \
            "event.stopPropagation();event.preventDefault();" \
            "return false;" % (id(self), self.EVENT_ONTOUCHCANCEL)
        self.eventManager.register_listener(self.EVENT_ONTOUCHCANCEL, listener, funcname)


class HBox(Widget):
    """It contains widget automatically aligning them horizontally.
    Does not permit children absolute positioning.

    In order to add children to this container, use the append(child, key) function.
    The key have to be numeric and determines the children order in the layout.

    Note: If you would absolute positioning, use the Widget container instead.
    """

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(HBox, self).__init__(**kwargs)

        # fixme: support old browsers
        # http://stackoverflow.com/a/19031640
        self.style['display'] = 'flex'
        self.style['justify-content'] = 'space-around'
        self.style['align-items'] = 'center'
        self.style['flex-direction'] = 'row'

    def append(self, value, key=''):
        """It allows to add child widgets to this.
        The key allows to access the specific child in this way widget.children[key].
        The key have to be numeric and determines the children order in the layout.

        Args:
            value (Widget): Child instance to be appended.
            key (int): Unique identifier for the child. It have to be integer, and the value determines the order in the layout
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

        key = str(id(value)) if key == '' else key
        self.add_child(key, value)

        if self.layout_orientation == Widget.LAYOUT_HORIZONTAL:
            if 'float' in self.children[key].style.keys():
                if not (self.children[key].style['float'] == 'none'):
                    self.children[key].style['float'] = 'left'
            else:
                self.children[key].style['float'] = 'left'

        return key


class VBox(HBox):
    """It contains widget automatically aligning them vertically.
    Does not permit children absolute positioning.

    In order to add children to this container, use the append(child, key) function.
    The key have to be numeric and determines the children order in the layout.

    Note: If you would absolute positioning, use the Widget container instead.
    """

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        super(VBox, self).__init__(**kwargs)
        self.style['flex-direction'] = 'column'


class Button(Widget):
    """The Button widget. Have to be used in conjunction with its event onclick.
    Use Widget.set_on_click_listener in order to register the listener.
    """
    @decorate_constructor_parameter_types([str])
    def __init__(self, text='', **kwargs):
        """
        Args:
            text (str): The text that will be displayed on the button.
            kwargs: See Widget.__init__()
        """
        super(Button, self).__init__(**kwargs)
        self.type = 'button'
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.set_text(text)

    def set_text(self, text):
        """
        Sets the text label for the button.

        Args:
            text (str): The string label of the button.
        """
        self.add_child('text', text)

    def set_enabled(self, enabled):
        """
        Enables or disables the Button.

        Args:
            enabled (bool): If true te button is enabled and so the user can press it.
        """
        if enabled:
            try:
                del self.attributes['disabled']
            except KeyError:
                pass
        else:
            self.attributes['disabled'] = None


class TextInput(Widget):
    """Editable multiline/single_line text area widget. You can set the content by means of the function set_text or
     retrieve its content with get_text.
    """

    EVENT_ONENTER = 'onenter'

    @decorate_constructor_parameter_types([bool])
    def __init__(self, single_line=True, **kwargs):
        """
        Args:
            single_line (bool): Determines if the TextInput have to be single_line. A multiline TextInput have a gripper
                                that allows the resize.
            kwargs: See Widget.__init__()
        """
        super(TextInput, self).__init__(**kwargs)
        self.type = 'textarea'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['new_value']=document.getElementById('%(id)s').value;" \
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id': id(self), 'evt': self.EVENT_ONCHANGE}
        self.set_text('')

        if single_line:
            self.style['resize'] = 'none'
            self.attributes['rows'] = '1'

    def set_text(self, text):
        """Sets the text content.

        Args:
            text (str): The string content that have to be appended as standard child identified by the key 'text'
        """
        self.add_child('text', str(text))

    def get_text(self):
        """
        Returns:
            str: The text content of the TextInput. You can set the text content with set_text(text).
        """
        return self.get_child('text')

    def set_value(self, text):
        """Sets the text content.

        Args:
            text (str): The string content that have to be appended as standard child identified by the key 'text'
        """
        self.set_text(text)

    def get_value(self):
        """
        Returns:
            str: The text content of the TextInput. You can set the text content with set_text(text).
        """
        return self.get_text()

    def onchange(self, new_value):
        """Called when the user finishes to edit the TextInput content.

        Args:
            new_value (str): the new string content of the TextInput.
        """
        self.set_text(new_value)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [new_value])

    @decorate_set_on_listener("onchange", "(self,new_value)")
    def set_on_change_listener(self, listener, funcname):
        """Registers the listener for the Widget.onchange event.

        Note: the listener prototype have to be in the form on_textinput_change(self, new_value) where new_value is the
            new text content of the TextInput.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)

    def onkeydown(self, new_value):
        """Called when the user types a key into the TextInput.

        Note: This event can't be registered together with Widget.onenter.

        Args:
            new_value (str): the new string content of the TextInput.
        """
        self.set_text(new_value)
        return self.eventManager.propagate(self.EVENT_ONKEYDOWN, [new_value])

    @decorate_set_on_listener("onkeydown", "(self,new_value)")
    def set_on_key_down_listener(self, listener, funcname):
        """Registers the listener for the Widget.onkeydown event.

        Note: the listener prototype have to be in the form on_textinput_key_down(self, new_value) where new_value is
            the new text content of the TextInput.

        Note: Overwrites Widget.onenter.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONKEYDOWN] = \
            "var params={};params['new_value']=document.getElementById('%(id)s').value;" \
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id': id(self), 'evt': self.EVENT_ONKEYDOWN}
        self.eventManager.register_listener(self.EVENT_ONKEYDOWN, listener, funcname)

    def onenter(self, new_value):
        """Called when the user types an ENTER into the TextInput.
        Note: This event can't be registered together with Widget.onkeydown.

        Args:
            new_value (str): the new string content of the TextInput.
        """
        self.set_text(new_value)
        return self.eventManager.propagate(self.EVENT_ONENTER, [new_value])

    @decorate_set_on_listener("onenter", "(self,new_value)")
    def set_on_enter_listener(self, listener, funcname):
        """Registers the listener for the Widget.onenter event.

        Note: the listener prototype have to be in the form on_textinput_enter(self, new_value) where new_value is
            the new text content of the TextInput.

        Note: Overwrites Widget.onkeydown.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.attributes[self.EVENT_ONKEYDOWN] = """
            if (event.keyCode == 13) {
                var params={};
                params['new_value']=document.getElementById('%(id)s').value;
                document.getElementById('%(id)s').value = '';
                document.getElementById('%(id)s').onchange = '';
                sendCallbackParam('%(id)s','%(evt)s',params);
                return false;
            }""" % {'id': id(self), 'evt': self.EVENT_ONENTER}
        self.eventManager.register_listener(self.EVENT_ONENTER, listener, funcname)


class Label(Widget):
    """Non editable text label widget. Set its content by means of set_text function, and retrieve its content with the
    function get_text.
    """
    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        """
        Args:
            text (str): The string content that have to be displayed in the Label.
            kwargs: See Widget.__init__()
        """
        super(Label, self).__init__(**kwargs)
        self.type = 'p'
        self.set_text(text)

    def set_text(self, text):
        """Sets the text content.

        Args:
            text (str): The string content that have to be appended as standard child identified by the key 'text'
        """
        self.add_child('text', text)

    def get_text(self):
        """
        Returns:
            str: The text content of the label. You can set the text content with set_text(text).
        """
        return self.get_child('text')


class GenericDialog(Widget):
    """Generic Dialog widget. It can be customized to create personalized dialog windows.
    You can setup the content adding content widgets with the functions add_field or add_field_with_label.
    The user can confirm or dismiss the dialog with the common buttons Cancel/Ok.
    Each field added to the dialog can be retrieved by its key, in order to get back the edited value. Use the function
    get_field(key) to retrieve the field.
    The Ok button emits the 'confirm_dialog' event. Register the listener to it with set_on_confirm_dialog_listener.
    The Cancel button emits the 'cancel_dialog' event. Register the listener to it with set_on_cancel_dialog_listener.
    """

    EVENT_ONCONFIRM = 'confirm_dialog'
    EVENT_ONCANCEL = 'cancel_dialog'

    @decorate_constructor_parameter_types([str, str])
    def __init__(self, title='', message='', **kwargs):
        """
        Args:
            title (str): The title of the dialog.
            message (str): The message description.
            kwargs: See Widget.__init__()
        """
        super(GenericDialog, self).__init__(**kwargs)
        self.set_layout_orientation(Widget.LAYOUT_VERTICAL)
        self.style['display'] = 'block'
        self.style['overflow'] = 'auto'

        if len(title) > 0:
            t = Label(title)
            t.add_class('DialogTitle')
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
        self.conf.style['margin'] = '3px'
        self.cancel = Button('Cancel')
        self.cancel.set_size(100, 30)
        self.cancel.style['margin'] = '3px'
        hlay = Widget(height=35)
        hlay.style['display'] = 'block'
        hlay.style['overflow'] = 'visible'
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
        """
        Adds a field to the dialog together with a descriptive label and a unique identifier.

        Note: You can access to the fields content calling the function GenericDialog.get_field(key).

        Args:
            key (str): The unique identifier for the field.
            label_description (str): The string content of the description label.
            field (Widget): The instance of the field Widget. It can be for example a TextInput or maybe a custom widget.
        """
        self.inputs[key] = field
        label = Label(label_description)
        label.style['margin'] = '0px 5px'
        label.style['min-width'] = '30%'
        container = HBox()
        container.style['overflow'] = 'auto'
        container.style['padding'] = '3px'
        container.append(label, key='lbl' + key)
        container.append(self.inputs[key], key=key)
        self.container.append(container, key=key)

    def add_field(self, key, field):
        """
        Adds a field to the dialog with a unique identifier.

        Note: You can access to the fields content calling the function GenericDialog.get_field(key).

        Args:
            key (str): The unique identifier for the field.
            field (Widget): The widget to be added to the dialog, TextInput or any Widget for example.
        """
        self.inputs[key] = field
        container = Widget()
        container.style['display'] = 'block'
        container.style['overflow'] = 'auto'
        container.style['padding'] = '3px'
        container.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)
        container.append(self.inputs[key], key=key)
        self.container.append(container, key=key)

    def get_field(self, key):
        """
        Args:
            key (str): The unique string identifier of the required field.

        Returns:
            Widget field instance added previously with methods GenericDialog.add_field or
            GenericDialog.add_field_with_label.
        """
        return self.inputs[key]

    def confirm_dialog(self):
        """Event generated by the OK button click.
        """
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCONFIRM, [])

    @decorate_set_on_listener("confirm_dialog", "(self)")
    def set_on_confirm_dialog_listener(self, listener, funcname):
        """Registers the listener for the GenericDialog.confirm_dialog event.

        Note: The prototype of the listener have to be like my_on_confirm_dialog(self).

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.eventManager.register_listener(self.EVENT_ONCONFIRM, listener, funcname)

    def cancel_dialog(self):
        """Event generated by the Cancel button click."""
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCANCEL, [])

    @decorate_set_on_listener("cancel_dialog", "(self)")
    def set_on_cancel_dialog_listener(self, listener, funcname):
        """Registers the listener for the GenericDialog.cancel_dialog event.

        Note: The prototype of the listener have to be like my_on_cancel_dialog(self).

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.eventManager.register_listener(self.EVENT_ONCANCEL, listener, funcname)


class InputDialog(GenericDialog):
    """Input Dialog widget. It can be used to query simple and short textual input to the user.
    The user can confirm or dismiss the dialog with the common buttons Cancel/Ok.
    The Ok button click or the ENTER key pression emits the 'confirm_dialog' event. Register the listener to it
    with set_on_confirm_dialog_listener.
    The Cancel button emits the 'cancel_dialog' event. Register the listener to it with set_on_cancel_dialog_listener.
    """

    EVENT_ONCONFIRMVALUE = 'confirm_value'

    @decorate_constructor_parameter_types([str, str, str])
    def __init__(self, title='Title', message='Message', initial_value='', **kwargs):
        """
        Args:
            title (str): The title of the dialog.
            message (str): The message description.
            initial_value (str): The default content for the TextInput field.
            kwargs: See Widget.__init__()
        """
        super(InputDialog, self).__init__(title, message, **kwargs)

        self.inputText = TextInput()
        self.inputText.set_on_enter_listener(self, 'on_text_enter_listener')
        self.add_field('textinput', self.inputText)
        self.inputText.set_text(initial_value)

        self.set_on_confirm_dialog_listener(self, 'confirm_value')

    def on_text_enter_listener(self, value):
        """event called pressing on ENTER key.

        propagates the string content of the input field
        """
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, [value])

    def confirm_value(self):
        """Event called pressing on OK button."""
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, [self.inputText.get_text()])

    @decorate_set_on_listener("confirm_value", "(self,value)")
    def set_on_confirm_value_listener(self, listener, funcname):
        """Registers the listener for the InputDialog.confirm_value event.

        Note: The prototype of the listener have to be like my_on_confirm_dialog(self, confirmed_value), where
            confirmed_value is the text content of the input field.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.eventManager.register_listener(self.EVENT_ONCONFIRMVALUE, listener, funcname)


class ListView(Widget):
    """List widget it can contain ListItems. Add items to it by using the standard append(item, key) function or
    generate a filled list from a string list by means of the function new_from_list. Use the list in conjunction of
    its onselection event. Register a listener with ListView.set_on_selection_listener.
    """

    EVENT_ONSELECTION = 'onselection'

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        """
        Args:
            kwargs: See Widget.__init__()
        """
        super(ListView, self).__init__(**kwargs)
        self.type = 'ul'
        self.selected_item = None
        self.selected_key = None

    @classmethod
    def new_from_list(cls, items, **kwargs):
        """Populates the ListView with a string list.

        Args:
            items (list): list of strings to fill the widget with.
        """
        obj = cls(**kwargs)
        for key, item in enumerate(items):
            obj.append(item, str(key))
        return obj

    def append(self, item, key=''):
        """Appends child items to the ListView. The items are accessible by list.children[key].

        Args:
            item (ListItem): the item to add.
            key (str): string key for the item.
        """
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
        """Removes all children from the list"""
        self.selected_item = None
        self.selected_key = None
        super(ListView, self).empty()

    def onselection(self, clicked_item):
        """Called when a new item gets selected in the list."""
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
        """Registers the listener for the ListView.onselection event.

        Note: The prototype of the listener have to be like my_list_onselection(self, selectedKey). Where selectedKey is
        the unique string identifier for the selected item. To access the item use ListView.children[key], or its value
        directly by ListView.get_value.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.eventManager.register_listener(self.EVENT_ONSELECTION, listener, funcname)

    def get_value(self):
        """
        Returns:
            str: The value of the selected item or None
        """
        if self.selected_item is None:
            return None
        return self.selected_item.get_value()

    def get_key(self):
        """
        Returns:
            str: The key of the selected item or None if no item is selected.
        """
        return self.selected_key

    def select_by_key(self, key):
        """Selects an item by its key.

        Args:
            key (str): The unique string identifier of the item that have to be selected.
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
        """Selects an item by the text content of the child.

        Args:
            value (str): Text content of the item that have to be selected.
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
    """List item widget for the ListView.

    ListItems are characterized by a textual content. They can be selected from
    the ListView. Do NOT manage directly its selection by registering set_on_click_listener, use instead the events of
    the ListView.
    """

    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        """
        Args:
            text (str, unicode): The textual content of the ListItem.
            kwargs: See Widget.__init__()
        """
        super(ListItem, self).__init__(**kwargs)
        self.type = 'li'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)

    def set_text(self, text):
        """
        Args:
            text (str):
        """
        self.add_child('text', text)

    def get_text(self):
        """
        Returns:
            str: The text content of the ListItem
        """
        return self.get_child('text')

    def get_value(self):
        """
        Returns:
            str: The text content of the ListItem
        """
        return self.get_text()

    def onclick(self):
        """Called when the item gets clicked. It is managed by the container ListView."""
        return self.eventManager.propagate(self.EVENT_ONCLICK, [self])


class DropDown(Widget):
    """Drop down selection widget. Implements the onchange(value) event. Register a listener for its selection change
    by means of the function DropDown.set_on_change_listener.
    """

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        """
        Args:
            kwargs: See Widget.__init__()
        """
        super(DropDown, self).__init__(**kwargs)
        self.type = 'select'
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(id)s').value;" \
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id': id(self),
                                                               'evt': self.EVENT_ONCHANGE}
        self.selected_item = None
        self.selected_key = None

    def select_by_key(self, key):
        """Selects an item by its unique string identifier.

        Args:
            key (str): Unique string identifier of the DropDownItem that have to be selected.
        """
        for item in self.children.values():
            if 'selected' in item.attributes:
                del item.attributes['selected']
        self.children[key].attributes['selected'] = 'selected'
        self.selected_key = key
        self.selected_item = self.children[key]

    def set_value(self, value):
        """Selects a DropDownItem by means of the contained text-

        Args:
            value (str): Textual content of the DropDownItem that have to be selected.
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
        """
        Returns:
            str: The value of the selected item or None.
        """
        if self.selected_item is None:
            return None
        return self.selected_item.get_value()

    def get_key(self):
        """
        Returns:
            str: The unique string identifier of the selected item or None.
        """
        return self.selected_key

    def onchange(self, value):
        """Called when a new DropDownItem gets selected.
        """
        log.debug('combo box. selected %s' % value)
        self.set_value(value)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [value])

    @decorate_set_on_listener("onchange", "(self,new_value)")
    def set_on_change_listener(self, listener, funcname):
        """Registers the listener for the DropDown.onchange event.

        Note: The prototype of the listener have to be like my_dropdown_onchange(self, value). Where value is
        the textual content of the selected item.

        Args:
            listener (App, Widget): Instance of the listener. It can be the App or a Widget.
            funcname (str): Literal name of the listener function, member of the listener instance
        """
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)


class DropDownItem(Widget):
    """item widget for the DropDown"""

    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        """
        Args:
            kwargs: See Widget.__init__()
        """
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
        """
        Args:
            filename (str): an url to an image
            kwargs: See Widget.__init__()
        """
        super(Image, self).__init__(**kwargs)
        self.type = 'img'
        self.attributes['src'] = filename


class Table(Widget):
    """
    table widget - it will contains TableRow
    """

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        """
        Args:
            kwargs: See Widget.__init__()
        """
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
        """
        Args:
            kwargs: See Widget.__init__()
        """
        super(TableRow, self).__init__(**kwargs)
        self.type = 'tr'
        self.style['float'] = 'none'


class TableItem(Widget):
    """item widget for the TableRow."""

    @decorate_constructor_parameter_types([str])
    def __init__(self, text='', **kwargs):
        """
        Args:
            text (str):
            kwargs: See Widget.__init__()
        """
        super(TableItem, self).__init__(**kwargs)
        self.type = 'td'
        self.style['float'] = 'none'
        self.add_child('text', text)


class TableTitle(Widget):
    """title widget for the table."""

    @decorate_constructor_parameter_types([str])
    def __init__(self, title='', **kwargs):
        """
        Args:
            title (str):
            kwargs: See Widget.__init__()
        """
        super(TableTitle, self).__init__(**kwargs)
        self.type = 'th'
        self.style['float'] = 'none'
        self.add_child('text', title)


class Input(Widget):
    @decorate_constructor_parameter_types([str, str])
    def __init__(self, input_type='', default_value='', **kwargs):
        """
        Args:
            input_type (str): HTML5 input type
            default_value (str):
            kwargs: See Widget.__init__()
        """
        kwargs['_class'] = input_type
        super(Input, self).__init__(**kwargs)
        self.type = 'input'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(id)s').value;" \
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id': id(self),
                                                               'evt': self.EVENT_ONCHANGE}
        self.attributes['value'] = str(default_value)
        self.attributes['type'] = input_type

    def set_value(self, value):
        self.attributes['value'] = str(value)

    def get_value(self):
        """returns the new text value."""
        return self.attributes['value']

    def onchange(self, value):
        #0 hinibits the unwanted gui update that causes focus lost and difficulties in editing
        self.attributes.__setitem__('value', value, 0)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [value])

    @decorate_set_on_listener("onchange", "(self,new_value)")
    def set_on_change_listener(self, listener, funcname):
        """register the listener for the onchange event."""
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)

    def set_enabled(self, enabled):
        if enabled:
            try:
                del self.attributes['disabled']
            except KeyError:
                pass
        else:
            self.attributes['disabled'] = None

    def set_read_only(self, readonly):
        if readonly:
            self.attributes['readonly'] = None
        else:
            try:
                del self.attributes['readonly']
            except KeyError:
                pass


class CheckBoxLabel(Widget):
    @decorate_constructor_parameter_types([str, bool, str])
    def __init__(self, label='', checked=False, user_data='', **kwargs):
        """
        Args:
            label (str):
            checked (bool):
            user_data (str):
            kwargs: See Widget.__init__()
        """
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
    """check box widget useful as numeric input field implements the onchange event."""

    @decorate_constructor_parameter_types([bool, str])
    def __init__(self, checked=False, user_data='', **kwargs):
        """
        Args:
            checked (bool):
            user_data (str):
            kwargs: See Widget.__init__()
        """
        super(CheckBox, self).__init__('checkbox', user_data, **kwargs)
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(id)s').checked;" \
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id': id(self),
                                                               'evt': self.EVENT_ONCHANGE}
        self.set_value(checked)

    def onchange(self, value):
        self.set_value(value in ('True', 'true'), 0)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [value])

    def set_value(self, checked, update_ui = 1):
        if checked:
            self.attributes.__setitem__('checked', 'checked', update_ui)
        else:
            if 'checked' in self.attributes:
                self.attributes.__delitem__('checked', update_ui)

    def get_value(self):
        """
        Returns:
            bool:
        """
        return 'checked' in self.attributes


class SpinBox(Input):
    """spin box widget useful as numeric input field implements the onchange event.
    """

    @decorate_constructor_parameter_types([str, int, int, int])
    def __init__(self, default_value='100', min=100, max=5000, step=1, **kwargs):
        """
        Args:
            default_value (str):
            min (int):
            max (int):
            step (int):
            kwargs: See Widget.__init__()
        """
        super(SpinBox, self).__init__('number', default_value, **kwargs)
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['step'] = str(step)
        self.attributes[self.EVENT_ONKEYPRESS] = \
            'return event.charCode >= 48 && event.charCode <= 57 || event.charCode == 46 || event.charCode == 13;'


class Slider(Input):

    EVENT_ONINPUT = 'oninput'

    @decorate_constructor_parameter_types([str, int, int, int])
    def __init__(self, default_value='', min=0, max=10000, step=1, **kwargs):
        """
        Args:
            default_value (str):
            min (int):
            max (int):
            step (int):
            kwargs: See Widget.__init__()
        """
        super(Slider, self).__init__('range', default_value, **kwargs)
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['step'] = str(step)

    def oninput(self, value):
        return self.eventManager.propagate(self.EVENT_ONINPUT, [value])

    @decorate_set_on_listener("oninput", "(self,new_value)")
    def set_oninput_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONINPUT] = \
            "var params={};params['value']=document.getElementById('%(id)s').value;" \
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id': id(self), 'evt': self.EVENT_ONINPUT}
        self.eventManager.register_listener(self.EVENT_ONINPUT, listener, funcname)


class ColorPicker(Input):
    @decorate_constructor_parameter_types([str])
    def __init__(self, default_value='#995500', **kwargs):
        """
        Args:
            default_value (str): hex rgb color string (#rrggbb)
            kwargs: See Widget.__init__()
        """
        super(ColorPicker, self).__init__('color', default_value, **kwargs)


class Date(Input):
    @decorate_constructor_parameter_types([str])
    def __init__(self, default_value='2015-04-13', **kwargs):
        """
        Args:
            default_value (str): date string (yyyy-mm-dd)
            kwargs: See Widget.__init__()
        """
        super(Date, self).__init__('date', default_value, **kwargs)


class GenericObject(Widget):
    """
    GenericObject widget - allows to show embedded object like pdf,swf..
    """

    @decorate_constructor_parameter_types([str])
    def __init__(self, filename, **kwargs):
        """
        Args:
            filename (str): URL
            kwargs: See Widget.__init__()
        """
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

    EVENT_ONSELECTION = 'onselection'

    @decorate_constructor_parameter_types([str, bool])
    def __init__(self, text, is_folder=False, **kwargs):
        super(FileFolderItem, self).__init__(**kwargs)
        super(FileFolderItem, self).set_layout_orientation(Widget.LAYOUT_HORIZONTAL)
        self.style['margin'] = '3px'
        self.isFolder = is_folder
        self.attributes[self.EVENT_ONCLICK] = ''
        self.icon = Widget(_class='FileFolderItemIcon')
        self.icon.set_size(30, 30)
        # the icon click activates the onselection event, that is propagates to registered listener
        if is_folder:
            self.icon.set_on_click_listener(self, self.EVENT_ONCLICK)
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
        self.label.style['font-weight'] = 'bold' if self.selected else 'normal'

    def onselection(self):
        self.set_selected(not self.selected)
        return self.eventManager.propagate(self.EVENT_ONSELECTION, [self])

    @decorate_set_on_listener("onselection", "(self,folderItemInstance)")
    def set_on_selection_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONSELECTION, listener, funcname)

    def set_text(self, t):
        self.children['text'].set_text(t)

    def get_text(self):
        return self.children['text'].get_text()


class FileSelectionDialog(GenericDialog):
    """file selection dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "confirm_value" and "cancel_dialog" events."""

    EVENT_ONCONFIRMVALUE = 'confirm_value'

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
        """
        Args:
            kwargs: See Widget.__init__()
        """
        super(MenuBar, self).__init__(**kwargs)
        self.type = 'nav'
        self.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)


class Menu(Widget):
    """Menu widget can contain MenuItem."""

    @decorate_constructor_parameter_types([])
    def __init__(self, **kwargs):
        """
        Args:
            kwargs: See Widget.__init__()
        """
        super(Menu, self).__init__(**kwargs)
        self.type = 'ul'
        self.set_layout_orientation(Widget.LAYOUT_HORIZONTAL)


class MenuItem(Widget):
    """MenuItem widget can contain other MenuItem."""

    @decorate_constructor_parameter_types([str])
    def __init__(self, text, **kwargs):
        """
        Args:
            text (str):
            kwargs: See Widget.__init__()
        """
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
        self.EVENT_ON_DATA = 'ondata'

        self.attributes[self.EVENT_ONCHANGE] = \
            "var files = this.files;" \
            "for(var i=0; i<files.length; i++){" \
            "uploadFile('%(id)s','%(evt_success)s','%(evt_failed)s','%(evt_data)s',files[i]);}" % {
                'id': id(self), 'evt_success': self.EVENT_ON_SUCCESS, 'evt_failed': self.EVENT_ON_FAILED,
                'evt_data': self.EVENT_ON_DATA}

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
        
    def ondata(self, filedata, filename):
        with open(self._savepath+filename,'wb') as f:
            f.write(filedata)
        return self.eventManager.propagate(self.EVENT_ON_DATA, [filedata, filename])

    @decorate_set_on_listener("ondata", "(self,filedata, filename)")
    def set_on_data_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ON_DATA, listener, funcname)


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
        headers = {'Content-type': 'application/octet-stream',
                   'Content-Disposition': 'attachment; filename=%s' % os.path.basename(self._filename)}
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
