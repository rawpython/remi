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

import traceback
from configuration import *
import server
from server import *
import os #used for directory browse functionalities

# simple and stupid tricks


def to_pix(x):
    return str(x) + 'px'


def from_pix(x):
    return int(float(x.replace('px', '')))


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

    In html, it is a DIV tag    
    the "self.type" attribute specifies the HTML tag representation    
    the "self.attributes[]" attribute specifies the HTML attributes like "style" "class" "id" 
    the "self.style[]" attribute specifies the CSS style content like "font" "color". 
    It will be packet togheter with "self.attributes"

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

        self.attributes['class'] = self.__class__.__name__
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
            spacing = to_pix(self.widget_spacing)
            selfHeight = 0
            selfWidth = 0
            if 'height' in self.style.keys() and 'height' in self.children[key].style.keys():
                selfHeight = from_pix(self.style['height']) - from_pix(self.children[key].style['height'])
            if 'width' in self.style.keys() and 'width' in self.children[key].style.keys():
                selfWidth = from_pix(self.style['width']) - from_pix(self.children[key].style['width'])
            self.children[key].style['margin'] = spacing + " " + to_pix(selfWidth/2)
            
            if self.layout_orizontal:
                self.children[key].style['margin'] = to_pix(selfHeight/2) + " " + spacing
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
                    #when the child is removed we stop the iteration
                    #this implies that a child replication should not be allowed
                    break

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

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class Button(Widget):

    """
    button widget: implements the onclick event.
    """

    def __init__(self, w, h, text=''):
        super(Button, self).__init__(w, h)
        self.type = 'button'
        #self.attributes[self.EVENT_ONCLICK] = "var params={};params['x']=1;params['y']=3;sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "',params);"
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.set_text(text)

    def set_text(self, t):
        self.append('text', t)

    def onclick(self):
        debug_message('Button pressed: ', self.children['text'])
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
    """

    def __init__(self, w, h, single_line = True):
        super(TextInput, self).__init__(w, h)
        self.type = 'textarea'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = "var params={};params['newValue']=document.getElementById('" + str(
            id(self)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONCHANGE + "',params);"

        self.set_text('')

        if single_line:
            self.style['resize'] = 'none'
            self.attributes['rows'] = '1'

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
            
    def onkeydown(self,newValue):
        """returns the new text value."""
        self.set_text(newValue)
        params = list()
        params.append(newValue)
        return self.eventManager.propagate(self.EVENT_ONKEYDOWN, params)
        
    def set_on_key_down_listener(self,listener,funcname):
        self.attributes[
            self.EVENT_ONKEYDOWN] = "var params={};params['newValue']=document.getElementById('" + str(
            id(self)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONKEYDOWN + "',params);"
        self.eventManager.register_listener(
            self.EVENT_ONKEYDOWN, listener, funcname)


class SpinBox(Widget):

    """spin box widget usefull as numeric input field implements the onclick
    event.
    """

    def __init__(self, w, h, min=100, max=5000, value=1000, step=1):
        super(SpinBox, self).__init__(w, h)
        self.type = 'input'
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

    def set_value(self,value):
        self.attributes['value'] = str(value)


class Label(Widget):

    def __init__(self, w, h, text):
        super(Label, self).__init__(w, h)
        self.type = 'p'
        self.append('text', text)

    def set_text(self, t):
        self.append('text', t)

    def get_text(self):
        return self.children['text']
        
    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class GenericDialog(Widget):

    """input dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "onConfirm" and "onCancel" events."""

    def __init__(self, width=500, height=160, title='Title', message='Message'):
        self.width = width
        self.height = height
        super(GenericDialog, self).__init__(self.width, self.height, False, 10)

        self.EVENT_ONCONFIRM = 'confirm_dialog'
        self.EVENT_ONCANCEL = 'cancel_dialog'

        t = Label(self.width - 20, 50, title)
        m = Label(self.width - 20, 30, message)

        self.container = Widget(self.width - 20,0, False, 0)
        self.conf = Button(50, 30, 'Ok')
        self.cancel = Button(50, 30, 'Cancel')

        t.style['font-size'] = '16px'
        t.style['font-weight'] = 'bold'

        hlay = Widget(self.width - 20, 30)
        hlay.append('1', self.conf)
        hlay.append('2', self.cancel)
        self.conf.style['float'] = 'right'
        self.cancel.style['float'] = 'right'

        self.append('1', t)
        self.append('2', m)
        self.append('3', self.container)
        self.append('4', hlay)

        self.conf.attributes[self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCONFIRM + "');"
        self.cancel.attributes[self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCANCEL + "');"

        self.inputs = {}

        self.baseAppInstance = None

    def add_field_with_label(self,fieldName,field):
        fields_spacing = 5
        field_height = from_pix(field.style['height']) + fields_spacing*2
        field_width = from_pix(field.style['width']) + fields_spacing*4
        self.style['height'] = to_pix( from_pix(self.style['height']) + field_height)
        self.container.style['height'] = to_pix(from_pix(self.container.style['height']) + field_height)
        self.inputs[fieldName] = field
        label = Label( (self.width-20)-field_width-1, 30, fieldName )
        container = Widget(self.width-20, field_height , True, fields_spacing)
        container.append('lbl' + fieldName,label)
        container.append(fieldName,self.inputs[fieldName])
        self.container.append(fieldName,container)
        
    def add_field(self,fieldName,field):
        fields_spacing = 5
        field_height = from_pix(field.style['height']) + fields_spacing*2
        field_width = from_pix(field.style['width']) + fields_spacing*4
        self.style['height'] = to_pix( from_pix(self.style['height']) + field_height)
        self.container.style['height'] = to_pix(from_pix(self.container.style['height']) + field_height)
        self.inputs[fieldName] = field
        container = Widget(self.width-20, field_height , True, fields_spacing)
        container.append(fieldName,self.inputs[fieldName])
        self.container.append(fieldName,container)

    def get_field(self,fieldName):
        return self.inputs[fieldName]

    def confirm_dialog(self):
        """event called pressing on OK button.
        """
        self.hide()
        params = list()
        return self.eventManager.propagate(self.EVENT_ONCONFIRM, params)

    def set_on_confirm_dialog_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCONFIRM, listener, funcname)

    def cancel_dialog(self):
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCANCEL, list())

    def set_on_cancel_dialog_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCANCEL, listener, funcname)


class InputDialog(GenericDialog):

    """input dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "onConfirm" and "onCancel" events."""

    def __init__(self, width=500, height=160, title='Title', message='Message'):
        super(InputDialog, self).__init__(width, height, title, message)

        self.inputText = TextInput(width - 20, 30)
        self.add_field('textinput',self.inputText)

        self.EVENT_ONCONFIRMVALUE = 'confirm_value'        
        self.set_on_confirm_dialog_listener(self, 'confirm_value')

    def confirm_value(self):
        """event called pressing on OK button.
        propagates the string content of the input field
        """
        self.hide()
        params = list()
        params.append(self.inputText.get_text())
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, params)

    def set_on_confirm_value_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCONFIRMVALUE, listener, funcname)


class ListView(Widget):

    """list widget it can contain ListItems."""

    def __init__(self, w, h, horizontal=False):
        super(ListView, self).__init__(w, h, horizontal)
        self.type = 'ul'
        self.EVENT_ONSELECTION = 'onselection'
        self.selected_item = None

    def append(self, key, item):
        #if an event listener is already set for the added item, it will not generate a selection event
        if item.attributes[self.EVENT_ONCLICK] == '':
            item.set_on_click_listener(self,self.EVENT_ONSELECTION)
        item.attributes['item_selected'] = False
        super(self.__class__, self).append(key,item)

    def onselection(self,clicked_item):
        selected_key = None
        for k in self.children.keys():
            if self.children[k]==clicked_item:
                selected_key = k
                debug_message('ListView - onselection. Selected item key: ',k)
                if self.selected_item != None:
                    self.selected_item['item_selected'] = False
                self.selected_item = self.children[selected_key]
                self.selected_item['item_selected'] = True
                break
        params = list()
        params.append(selected_key)
        return self.eventManager.propagate(self.EVENT_ONSELECTION, params)

    def set_on_selection_listener(self, listener, funcname):
        """The listener will receive the key of the selected item.
        If you add the element from an array, use a numeric incremental key
        """
        self.eventManager.register_listener(
            self.EVENT_ONSELECTION, listener, funcname)


class ListItem(Widget):

    """item widget for the ListView implements the onclick event.
    """

    def __init__(self, w, h, text):
        super(ListItem, self).__init__(w, h)
        self.type = 'li'

        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)

    def set_text(self, text):
        self.append('text', text)

    def get_text(self):
        return self.children['text']

    def onclick(self):
        params = list()
        params.append(self)
        return self.eventManager.propagate(self.EVENT_ONCLICK, params)

    def set_on_click_listener(self, listener, funcname):
        """WARNING!!! DO NOT USE. If used disables the set_on_selection_listener of the ListView"""
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class DropDown(Widget):

    """combo box widget implements the onchange event.
    """

    def __init__(self, w, h):
        super(DropDown, self).__init__(w, h)
        self.type = 'select'
        self.attributes[self.EVENT_ONCHANGE] = "var params={};params['newValue']=document.getElementById('" + str(
            id(self)) + "').value;sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ONCHANGE + "',params);"

    def select_by_key(self, itemKey):
        """
        selects the item by its key
        """
        for item in self.children.values():
            if 'selected' in item.attributes:
                del item.attributes['selected']
        self.children[itemKey].attributes['selected'] = 'selected'

    def set_value(self, newValue):
        """
        selects the item by the contained text
        """
        for item in self.children.values():
            if item.attributes['value'] == newValue:
                item.attributes['selected'] = 'selected'
            else:
                if 'selected' in item.attributes:
                    del item.attributes['selected']

    def onchange(self, newValue):
        params = list()
        params.append(newValue)
        debug_message('combo box. selected', newValue)
        self.set_value(newValue)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, params)

    def set_on_change_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCHANGE, listener, funcname)


class DropDownItem(Widget):

    """item widget for the DropDown implements the onclick event.
    """

    def __init__(self, w, h, text):
        super(DropDownItem, self).__init__(w, h)
        self.type = 'option'
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
        self.attributes['src'] = BASE_ADDRESS + filename

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, list())

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)
            

class Table(Widget):

    """
    table widget - it will contains TableRow
    """

    def __init__(self, w, h):
        super(Table, self).__init__(w, h)
        self.type = 'table'
        self.style['float'] = 'none'


class TableRow(Widget):

    """
    row widget for the Table - it will contains TableItem
    """

    def __init__(self):
        super(TableRow, self).__init__(-1, -1)
        self.type = 'tr'
        self.style['float'] = 'none'


class TableItem(Widget):

    """item widget for the TableRow."""

    def __init__(self):
        super(TableItem, self).__init__(-1, -1)
        self.type = 'td'
        self.style['float'] = 'none'


class TableTitle(Widget):

    """title widget for the table."""

    def __init__(self, title=''):
        super(TableTitle, self).__init__(-1, -1)
        self.type = 'th'
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

    def set_value(self,value):
        self.attributes['value'] = str(value)

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
        self.attributes['data'] = filename


class FileFolderNavigator(Widget):
    
    """FileFolderNavigator widget.
    """

    def __init__(self, w, h, multiple_selection,selection_folder):
        self.w = w
        self.h = h
        self.multiple_selection = multiple_selection
        self.sep = os.sep #'/' #default separator in path os.sep
        super(FileFolderNavigator, self).__init__(w, h, False)
        
        self.selectionlist = list() #here are stored selected files and folders
        self.controlsContainer = Widget(w,25,True)
        self.controlBack = Button(45,25,'Up')
        self.controlBack.set_on_click_listener(self,'dir_go_back')
        self.controlGo = Button(45,25,'Go >>')
        self.controlGo.set_on_click_listener(self,'dir_go')
        self.pathEditor = TextInput(w-90,25)
        self.pathEditor.style['resize'] = 'none'
        self.pathEditor.attributes['rows'] = '1'
        self.controlsContainer.append('1',self.controlBack)
        self.controlsContainer.append('2',self.pathEditor)
        self.controlsContainer.append('3',self.controlGo)
        
        self.itemContainer = Widget(w,h-25,False)
        self.itemContainer.style['overflow-y'] = 'scroll'
        self.itemContainer.style['overflow-x'] = 'hidden'
        
        self.append('controls',self.controlsContainer)
        self.append('items',self.itemContainer)
        
        self.folderItems = list()
        self.chdir(selection_folder) #move to actual working directory
    
    def get_selection_list(self):
        return self.selectionlist
        
    def populate_folder_items(self,directory):
        fpath = directory + self.sep
        debug_message("FileFolderNavigator - populate_folder_items")
        l = os.listdir(directory)
        #used to restore a valid path after a wrong edit in the path editor
        self.lastValidPath = directory 
        #we remove the container avoiding graphic update adding items
        #this speeds up the navigation
        self.remove(self.itemContainer)
        #creation of a new instance of a itemContainer
        self.itemContainer = Widget(self.w,self.h-25,False)
        self.itemContainer.style['overflow-y'] = 'scroll'
        self.itemContainer.style['overflow-x'] = 'hidden'
        
        for i in l:
            isFolder = False
            if not os.path.isfile(fpath+i):
                isFolder = True
            fi = FileFolderItem(self.w,33,i,isFolder)
            fi.set_on_click_listener(self,'on_folder_item_click') #navigation purpose
            fi.set_on_selection_listener(self,'on_folder_item_selected') #selection purpose
            self.folderItems.append(fi)
            self.itemContainer.append(i,fi)
        self.append('items',self.itemContainer)

    def dir_go_back(self):
        curpath = os.getcwd() #backup the path
        try:
            os.chdir( self.pathEditor.get_text() )
            os.chdir('..')
            self.chdir(os.getcwd())
        except Exception as e:
            self.pathEditor.set_text(self.lastValidPath)
            debug_alert(traceback.format_exc())
        os.chdir( curpath ) #restore the path

    def dir_go(self):
        #when the GO button is pressed, it is supposed that the pathEditor is changed
        curpath = os.getcwd() #backup the path
        try:
            os.chdir( self.pathEditor.get_text() )
            self.chdir(os.getcwd())
        except Exception as e:
            debug_alert(traceback.format_exc())
            self.pathEditor.set_text(self.lastValidPath)
        os.chdir( curpath ) #restore the path
        
    def chdir(self, directory):
        curpath = os.getcwd() #backup the path
        debug_message("FileFolderNavigator - chdir:" + directory + "\n")
        for c in self.folderItems:
            self.itemContainer.remove(c) #remove the file and folders from the view
        self.folderItems = list()
        self.selectionlist = list() #reset selected file list
        os.chdir(directory)
        directory = os.getcwd()
        self.populate_folder_items(directory)
        self.pathEditor.set_text(directory)
        os.chdir( curpath ) #restore the path
        
    def on_folder_item_selected(self,folderitem):
        if not self.multiple_selection:
            self.selectionlist = list()
            for c in self.folderItems:
                c.set_selected(False)
            folderitem.set_selected(True)
        debug_message("FileFolderNavigator - on_folder_item_click")
        #when an item is clicked it is added to the file selection list
        f = self.pathEditor.get_text() + self.sep + folderitem.get_text()
        if f in self.selectionlist:
            self.selectionlist.remove(f)
        else:
            print("element not in the list, appending\n")
            self.selectionlist.append(f)

    def on_folder_item_click(self,folderitem):
        debug_message("FileFolderNavigator - on_folder_item_dblclick")
        #when an item is clicked two time
        f = self.pathEditor.get_text() + self.sep + folderitem.get_text()
        if not os.path.isfile(f):
            self.chdir(f)

    def get_selected_filefolders(self):
        return self.selectionlist
        

class FileFolderItem(Widget):

    """FileFolderItem widget for the FileFolderNavigator implements the onclick event.
    """

    def __init__(self, w, h, text, isFolder = False):
        super(FileFolderItem, self).__init__(w, h, True)
        self.EVENT_ONSELECTION = 'onselection'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.icon = Widget(33, h)
        #the icon click activates the onselection event, that is propagates to registered listener
        self.icon.set_on_click_listener(self,self.EVENT_ONSELECTION)
        self.icon.attributes['class'] = 'FileFolderItemIcon'

        iconFile = 'res/file.png'
        if isFolder:
            iconFile = 'res/folder.png'

        self.icon.style['background-image'] = "url('" + iconFile + "')"
        self.label = Label(w-33, h, text)
        if isFolder:
            self.label.set_on_click_listener(self,self.EVENT_ONCLICK)
        else:
            self.label.set_on_click_listener(self,self.EVENT_ONSELECTION)
        self.append('icon', self.icon)
        self.append('text', self.label)
        self.selected = False

    def onclick(self):
        params = list()
        params.append(self)
        return self.eventManager.propagate(self.EVENT_ONCLICK, params)

    def set_on_click_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)

    def set_selected(self, selected):
        self.selected = selected
        if self.selected:
            self.style['color'] = 'red'
        else:
            self.style['color'] = 'black'

    def onselection(self):
        self.set_selected(not self.selected)
        params = list()
        params.append(self)
        return self.eventManager.propagate(self.EVENT_ONSELECTION, params)

    def set_on_selection_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONSELECTION, listener, funcname)
            
    def set_text(self, t):
        """sets the text content."""
        self.children['text'].set_text(t)

    def get_text(self):
        return self.children['text'].get_text()


class FileSelectionDialog(GenericDialog):

    """file selection dialog, it opens a new webpage allows the OK/ABORT functionality
    implementing the "onConfirm" and "onAbort" events."""

    def __init__(self, width = 600, fileFolderNavigatorHeight = 210, title = 'File dialog', message = 'Select files and folders', multiple_selection = True, selection_folder = '.'):
        super(FileSelectionDialog, self).__init__(width, 160, title, message)
        
        self.fileFolderNavigator = FileFolderNavigator(width-20,fileFolderNavigatorHeight,multiple_selection,selection_folder)

        self.add_field('fileFolderNavigator',self.fileFolderNavigator)

        self.EVENT_ONCONFIRMVALUE = 'confirm_value'        
        self.set_on_confirm_dialog_listener(self, 'confirm_value')

    def confirm_value(self):
        """event called pressing on OK button.
           propagates the string content of the input field
        """
        self.hide()
        params = list()
        params.append(self.fileFolderNavigator.get_selection_list())
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, params)

    def set_on_confirm_value_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ONCONFIRMVALUE, listener, funcname)


class Menu(Widget):

    """Menu widget can contain MenuItem."""

    def __init__(self, w, h, horizontal=True):
        super(Menu, self).__init__(w, h, horizontal)
        self.type = 'ul'


class MenuItem(Widget):
    
    """MenuItem widget can contain other MenuItem."""

    def __init__(self, w, h, text):
        self.w = w
        self.h = h
        self.subcontainer = None
        super(MenuItem, self).__init__(w, h)
        self.type = 'li'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)
        self.append = self.addSubMenu
    
    def addSubMenu(self, key, value):
        if self.subcontainer == None:
            self.subcontainer = Menu(self.w, self.h, False)
            super(self.__class__, self).append('subcontainer', self.subcontainer)
        self.subcontainer.append(key, value)

    def set_text(self, text):
        self.append('text', text)

    def get_text(self):
        return self.children['text']

    def onclick(self):
        params = list()
        #params.append()
        return self.eventManager.propagate(self.EVENT_ONCLICK, params)

    def set_on_click_listener(self, listener, funcname):
        self.attributes[
            self.EVENT_ONCLICK] = "sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "');"
        self.eventManager.register_listener(
            self.EVENT_ONCLICK, listener, funcname)


class FileUploader(Widget):

    """
    FileUploader widget:
        allows to upload multiple files to a specified folder.
        implements the onsuccess and onfailed events.
    """

    def __init__(self, w, h, savepath='./', multiple_selection_allowed=False):
        super(FileUploader, self).__init__(w, h)
        self.savepath = savepath
        self.multiple_selection_allowed = multiple_selection_allowed
        self.type = 'input'
        #self.attributes[self.EVENT_ONCLICK] = "var params={};params['x']=1;params['y']=3;sendCallback('" + str(id(self)) + "','" + self.EVENT_ONCLICK + "',params);"
        """
        <input type="file" id="fileinput" multiple="multiple" accept="image/*" />
        """
        self.attributes['type']='file'
        if multiple_selection_allowed:
            self.attributes['multiple']='multiple'
        self.attributes['accept']='*.*'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.EVENT_ON_SUCCESS = 'onsuccess'
        self.EVENT_ON_FAILED = 'onfailed'
        fileUploadScript = "function uploadFile(savePath,file){\
            var url = 'http://" + IP_ADDR + ':' + str(HTTP_PORT_NUMBER) + "';\
            var xhr = new XMLHttpRequest();\
            var fd = new FormData();\
            xhr.open('POST', url, true);\
            xhr.setRequestHeader('savepath', savePath);\
            xhr.setRequestHeader('filename', file.name);\
            xhr.onreadystatechange = function() {\
                if (xhr.readyState == 4 && xhr.status == 200) {\
                    /* Every thing ok, file uploaded */\
                    var params={};params['filename']=file.name;\
                    sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ON_SUCCESS + "',params);\
                    console.log('upload success: ' + file.name);\
                }else if(xhr.status == 400){\
                    var params={};params['filename']=file.name;\
                    sendCallbackParam('" + str(id(self)) + "','" + self.EVENT_ON_FAILED + "',params);\
                    console.log('upload failed: ' + file.name);\
                }\
            };\
            fd.append('upload_file', file);\
            xhr.send(fd);\
        };"
        self.attributes[self.EVENT_ONCHANGE] = fileUploadScript + "var files = this.files;for(var i=0; i<files.length; i++){uploadFile('" + self.savepath + "',files[i]);}"
        
    def onsuccess(self,filename):
        params = list()
        params.append(filename)
        return self.eventManager.propagate(self.EVENT_ON_SUCCESS, params)

    def set_on_success_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ON_SUCCESS, listener, funcname)

    def onfailed(self,filename):
        params = list()
        params.append(filename)
        return self.eventManager.propagate(self.EVENT_ON_FAILED, params)

    def set_on_failed_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ON_FAILED, listener, funcname)


class FileDownloader(Widget):

    """FileDownloader widget. Allows to start a file download."""

    def __init__(self, w, h, text, filePathName):
        super(FileDownloader, self).__init__(w, h, True)
        self.type = 'a'
        self.attributes['download'] = ''
        self.attributes['href'] = "http://" + IP_ADDR + ":" + str(HTTP_PORT_NUMBER) + '/' + filePathName
        self.set_text(text)

    def set_text(self, t):
        self.append('text', t)
        
