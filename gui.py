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

from configuration import *
import server
from server import *

# simple and stupid tricks


def to_pix(x):
    return str(x) + 'px'


def from_pix(x):
    return int(x.replace('px', ''))


def jsonize(d):
    return ';'.join(map(lambda k, v: k + ':' + v + '', d.keys(), d.values()))

# Manages the event propagation to the listeners functions


class EventManager():

    def __init__(self):
        self.listeners = {}
    # if for an event there is a listener, it calls the listener passing the
    # parameters

    def propagate(self, eventname, params):
        if not eventname in self.listeners.keys():
            return
        listener = self.listeners[eventname]
        return getattr(listener['instance'], listener['funcname'])(*params)
    # register a listener for a specific event

    def register_listener(self, eventname, instance, funcname):
        listener = {}
        listener['instance'] = instance
        listener['funcname'] = funcname
        self.listeners[eventname] = listener


class Widget(object):

    """base class for gui widgets.

    In html, it is a DIV tag    the "self.type" attribute specifies the
    HTML tag representation    the "self.attributes[]" attribute
    specifies the HTML attributes like "style" "class" "id" the
    "self.style[]"              attribute specifies the CSS style
    content like "font" "color". It will be packet togheter with
    "self.attributes"

    """

    def __init__(self, w=1, h=1, layout_orizontal=True, widget_spacing=0):
        """w = numeric with
        h = numeric height
        layout_orizontal = specifies the "float" css attribute
        widget_spacing = specifies the "margin" css attribute for the children"""

        # the runtime instances are processed every time a requests arrives, searching for the called method
        # if a class instance is not present in the runtimeInstances, it will
        # we not callable
        runtimeInstances.append(self)

        self.renderChildrenList = list()
        self.children = {}
        self.attributes = {}  # properties as class id style
        self.style = {}

        self.type = 'div'

        self.layout_orizontal = layout_orizontal
        self.widget_spacing = widget_spacing

        # some constants for the events
        self.BASE_ADDRESS = BASE_ADDRESS
        self.EVENT_ONCLICK = 'onclick'
        self.EVENT_ONDBLCLICK = 'ondblclick'
        self.EVENT_ONMOUSEDOWN = 'onmousedown'
        self.EVENT_ONMOUSEMOVE = 'onmousemove'
        self.EVENT_ONMOUSEOVER = 'onmouseover'
        self.EVENT_ONMOUSEOUT = 'onmouseout'
        self.EVENT_ONMOUSEUP = 'onmouseup'
        self.EVENT_ONKEYDOWN = 'onkeydown'
        self.EVENT_ONKEYPRESS = 'onkeypress'
        self.EVENT_ONKEYUP = 'onkeyup'
        self.EVENT_ONCHANGE = 'onchange'
        self.EVENT_ONFOCUS = 'onfocus'
        self.EVENT_ONBLUR = 'onblur'

        self.EVENT_ONUPDATE = 'onupdate'

        self.attributes['class'] = 'Widget'
        self.attributes['id'] = str(id(self))

        if w > -1:
            self.style['width'] = to_pix(w)
        if h > -1:
            self.style['height'] = to_pix(h)
        self.style['margin'] = '0px auto'

        self.oldRootWidget = None  # used when hiding the widget

        self.eventManager = EventManager()

    def __repr__(self):
        """it is used to automatically represent the widget to HTML format
        packs all the attributes, children and so on."""
        self['style'] = jsonize(self.style)
        classname = self.__class__.__name__

        # concatenating innerHTML. in case of html object we use repr, in case
        # of string we use directly the content
        innerHTML = ''
        for s in self.renderChildrenList:
            if isinstance(s, type('')):
                innerHTML = innerHTML + s
            else:
                innerHTML = innerHTML + repr(s)

        return '<%s %s>%s</%s>' % (self.type, ' '.join(map(lambda k, v: k + "=\"" + str(
            v) + "\"", self.attributes.keys(), self.attributes.values())), innerHTML, self.type)

    def repr_without_children(self):
        """it is used to automatically represent the widget to HTML format
        packs all the attributes."""
        self['style'] = jsonize(self.style)
        classname = self.__class__.__name__

        # concatenating innerHTML. in case of html object we use repr, in case
        # of string we use directly the content
        innerHTML = ''
        for s in self.renderChildrenList:
            if isinstance(s, type('')):
                innerHTML = innerHTML + s

        return '<%s %s>%s</%s>' % (self.type, ' '.join(map(lambda k, v: k + "=\"" + str(
            v) + "\"", self.attributes.keys(), self.attributes.values())), innerHTML, self.type)

    def __setitem__(self, key, value):
        """it is used for fast access to 'self.attributes[]'."""
        self.attributes[key] = value

    def append(self, key, value):
        """it allows to add child widgets to this.

        The key can be everything you want, in order to access to the
        specific child in this way 'widget.children[key]'.

        """
        if hasattr(value, 'attributes'):
            value.attributes['parent_widget'] = str(id(self))

        if key in self.children.keys():
            self.renderChildrenList.remove(self.children[key])
        self.renderChildrenList.append(value)

        self.children[key] = value

        if hasattr(self.children[key], 'style'):
            self.children[key].style['margin'] = to_pix(self.widget_spacing)
            if self.layout_orizontal:
                if 'float' in self.children[key].style.keys():
                    if not (self.children[key].style['float'] == 'none'):
                        self.children[key].style['float'] = 'left'
                else:
                    self.children[key].style['float'] = 'left'

    def remove(self, widget):
        if widget in self.children.values():
            #runtimeInstances.pop( runtimeInstances.index( self.children[key] ) )
            self.renderChildrenList.remove(widget)
            for k in self.children.keys():
                if str(id(self.children[k])) == str(id(widget)):
                    self.children.pop(k)

    def onfocus(self):
        return self.eventManager.propagate(self.EVENT_ONFOCUS, list())

    def set_on_focus_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONFOCUS] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONFOCUS + "');"
        #self.attributes[ self.EVENT_ONFOCUS ]=" var id=\'id=\'+'"+str(id(self))+"' ;sendCommand('" + self.BASE_ADDRESS + str(id(self)) + "/" + self.EVENT_ONFOCUS + "',id);"
        self.eventManager.register_listener(
            self.EVENT_ONFOCUS, listener, funcname)

    def onblur(self):
        return self.eventManager.propagate(self.EVENT_ONBLUR, list())

    def set_on_blur_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONBLUR] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONBLUR + "');"
        self.eventManager.register_listener(
            self.EVENT_ONBLUR, listener, funcname)

    def __getitem__(self, key):
        """This allows to set the parameter "Content type" when you return a widget
        you can return a widget in a callback in oreder to show it as main
        widget, now without specifing the content-type"""
        if key == 0:
            return self
        else:
            return 'text/html'

    def show(self, baseAppInstance):
        """Allows to show the widget as root window"""
        self.baseAppInstance = baseAppInstance
        # here the widget is set up as root, in server.gui_updater is monitored
        # this change and the new window is send to the browser
        self.oldRootWidget = self.baseAppInstance.client.root
        self.baseAppInstance.client.root = self

    def hide(self):
        """The root window is restored after a show"""
        if hasattr(self,'baseAppInstance'):
            self.baseAppInstance.client.root = self.oldRootWidget


class Button(Widget):

    """
    button widget:
        implements the onclick event. reloads the web page because it uses the GET call.
        requires
    """

    def __init__(self, w, h, text=''):
        super(Button, self).__init__(w, h)
        self.type = 'button'
        self.attributes['class'] = 'Button'
        #self.attributes[self.EVENT_ONCLICK] = "var params={};params['x']=1;params['y']=3;sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "',params);"
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.set_text(text)

    def set_text(self, t):
        self.append('text', t)

    def onclick(self):
        print('Button pressed: ', self.children['text'])
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        """Register a listener for the click event.

        listener = class instance
            funcname = the name of member function that will be called.
        example:
            bt.set_on_click_listener( listenerClass, "ontest" )

        """
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class TextInput(Widget):

    """multiline text area widget implements the onclick event.

    reloads the web page because it uses the GET call. implements the
    onchange event with POST method, without reloading the web page

    """

    def __init__(self, w, h):
        super(TextInput, self).__init__(w, h)
        self.type = 'textarea'
        self.attributes['class'] = 'TextInput'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = "var params={};params['newValue']=document.getElementById('" + str(
            id(self)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONCHANGE + "',params);"

        self.set_text('')

    def set_text(self, t):
        """sets the text content."""
        self.append('text', t)

    def get_text(self):
        return self.children['text']

    def onchange(self, newValue):
        """returns the new text value."""
        self.set_text(newValue)
        params = list()
        params.append(newValue)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, params)

    def set_on_change_listener(self, listener, funcname):
        """register the listener for the onchange event."""
        self.eventManager.register_listener(
            self.EVENT_ONCHANGE, listener, funcname)

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class SpinBox(Widget):

    """spin box widget usefull as numeric input field implements the onclick
    event.

    reloads the web page because it uses the GET call. implements the
    onchange event with POST method, without reloading the web page

    """

    def __init__(self, w, h, min=100, max=5000, value=1000, step=1):
        super(SpinBox, self).__init__(w, h)
        self.type = 'input'
        self.attributes['class'] = 'SpinBox'
        self.attributes['type'] = 'number'
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['value'] = str(value)
        self.attributes['step'] = str(step)

        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = "var params={};params['newValue']=document.getElementById('" + str(
            id(self)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONCHANGE + "',params);"

    def onchange(self, newValue):
        params = list()
        params.append(newValue)
        self.attributes['value'] = newValue
        return self.eventManager.propagate(self.EVENT_ONCHANGE, params)

    def set_on_change_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCHANGE, listener, funcname)

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)

    def value(self):
        return self.attributes['value']


class Label(Widget):

    def __init__(self, w, h, text):
        super(Label, self).__init__(w, h)
        self.type = 'p'
        self.attributes['class'] = 'Label'
        self.append('text', text)

    def set_text(self, t):
        self.append('text', t)

    def get_text(self):
        return self.children['content']


class InputDialog(Widget):

    """input dialog, it opens a new webpage allows the OK/ABORT functionality
    implementing the "onConfirm" and "onAbort" events."""

    def __init__(self, title, message):
        w = 500
        h = 150
        super(InputDialog, self).__init__(w, h, False, 10)

        self.EVENT_ONCONFIRM = 'confirm_value'
        self.EVENT_ONABORT = 'abort_value'
        #self.style["font-family"] = "arial,sans-serif"
        t = Label(w - 70, 50, title)
        m = Label(w - 70, 30, message)
        self.inputText = TextInput(w - 120, 30)
        self.conf = Button(50, 30, 'Ok')
        self.abort = Button(50, 30, 'Abort')

        t.style['font-size'] = '16px'
        t.style['font-weight'] = 'bold'

        hlay = Widget(w - 20, 30)
        hlay.append('1', self.inputText)
        hlay.append('2', self.conf)
        hlay.append('3', self.abort)

        self.append('1', t)
        self.append('2', m)
        self.append('3', hlay)

        self.inputText.attributes[self.EVENT_ONCHANGE] = ''
        self.conf.attributes[self.EVENT_ONCLICK] = "var params={};params['value']=document.getElementById('" + str(
            id(self.inputText)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONCONFIRM + "',params);"
        self.abort.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONABORT + "');"
        self.inputText.attributes[self.EVENT_ONCLICK] = ''

        self.baseAppInstance = None

    def confirm_value(self, value):
        """event called pressing on OK button.

        propagates the string content of the input field

        """
        self.hide()
        params = list()
        params.append(value)
        return self.eventManager.propagate(self.EVENT_ONCONFIRM, params)

    def set_on_confirm_value_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCONFIRM, listener, funcname)

    def abort_value(self):
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONABORT, list())

    def set_on_abort_value_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONABORT, listener, funcname)


class ListView(Widget):

    """list widget it can contain ListItems."""

    def __init__(self, w, h):
        super(ListView, self).__init__(w, h)
        self.type = 'ul'
        self.attributes['class'] = 'ListView'


class ListItem(Widget):

    """item widget for the ListView implements the onclick event.

    reloads the web page because it uses the GET call.

    """

    def __init__(self, w, h, text):
        super(ListItem, self).__init__(w, h)
        self.type = 'li'
        self.attributes['class'] = 'ListItem'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.append('1', text)

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class DropDown(Widget):

    """combo box widget implements the onchange event with POST method, without
    reloading the web page."""

    def __init__(self, w, h):
        super(DropDown, self).__init__(w, h)
        self.type = 'select'
        self.attributes['class'] = 'DropDown'
        self.attributes[self.EVENT_ONCHANGE] = "var params={};params['newValue']=document.getElementById('" + str(
            id(self)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONCHANGE + "',params);"

    def onchange(self, newValue):
        params = list()
        params.append(newValue)
        print('combo box. selected', newValue)
        for item in self.children.values():
            if item.attributes['value'] == newValue:
                item.attributes['selected'] = 'selected'
            else:
                if 'selected' in item.attributes:
                    del item.attributes['selected']
        return self.eventManager.propagate(self.EVENT_ONCHANGE, params)

    def set_on_change_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCHANGE, listener, funcname)


class DropDownItem(Widget):

    """item widget for the DropDown implements the onclick event.

    reloads the web page because it uses the GET call.

    """

    def __init__(self, w, h, text):
        super(DropDownItem, self).__init__(w, h)
        self.type = 'option'
        self.attributes['class'] = 'DropDownItem'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.append('1', text)
        self.attributes['value'] = text

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class Image(Widget):

    """image widget."""

    def __init__(self, w, h, filename):
        """filename should be an URL."""
        super(Image, self).__init__(w, h)
        self.type = 'img'
        self.attributes['class'] = 'Image'
        self.attributes['src'] = BASE_ADDRESS + filename


class Table(Widget):

    """
    table widget - it will contains TableRow
    """

    def __init__(self, w, h):
        super(Table, self).__init__(w, h)
        self.type = 'table'
        self.attributes['class'] = 'Table'
        self.style['float'] = 'none'


class TableRow(Widget):

    """
    row widget for the Table - it will contains TableItem
    """

    def __init__(self):
        super(TableRow, self).__init__(-1, -1)
        self.type = 'tr'
        self.attributes['class'] = 'TableRow'
        self.style['float'] = 'none'


class TableItem(Widget):

    """item widget for the TableRow."""

    def __init__(self):
        super(TableItem, self).__init__(-1, -1)
        self.type = 'td'
        self.attributes['class'] = 'TableItem'
        self.style['float'] = 'none'


class TableTitle(Widget):

    """title widget for the table."""

    def __init__(self, title=''):
        super(TableTitle, self).__init__(-1, -1)
        self.type = 'th'
        self.attributes['class'] = 'TableTitle'
        self.append('text', title)
        self.style['float'] = 'none'


class Input(Widget):

    def __init__(self, w, h, _type='', defaultValue=''):
        super(Input, self).__init__(w, h)
        self.type = 'input'
        self.attributes['class'] = _type

        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = "var params={};params['newValue']=document.getElementById('" + str(
            id(self)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONCHANGE + "',params);"
        self.attributes['value'] = str(defaultValue)
        self.attributes['type'] = _type

    def value(self):
        """returns the new text value."""
        return self.attributes['value']

    def onchange(self, newValue):
        self.attributes['value'] = newValue
        params = list()
        params.append(newValue)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, params)

    def set_on_change_listener(self, listener, funcname):
        """register the listener for the onchange event."""
        self.eventManager.register_listener(
            self.EVENT_ONCHANGE, listener, funcname)


class Slider(Input):

    def __init__(self, w, h, defaultValue='', min=0, max=10000, step=1):
        super(Slider, self).__init__(w, h, 'range', defaultValue)
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['step'] = str(step)


class ColorPicker(Input):

    def __init__(self, w, h, defaultValue='#995500'):
        super(ColorPicker, self).__init__(w, h, 'color', defaultValue)


class Date(Input):

    def __init__(self, w, h, defaultValue='2015-04-13'):
        super(Date, self).__init__(w, h, 'date', defaultValue)


class GenericObject(Widget):

    """
    GenericObject widget - allows to show embedded object like pdf,swf..
    """

    def __init__(self, w, h, filename):
        """filename should be an URL."""
        super(GenericObject, self).__init__(w, h)
        self.type = 'object'
        self.attributes['class'] = 'GenericObject'
        self.attributes['data'] = filename
