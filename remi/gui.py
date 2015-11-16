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
import traceback

from .server import runtimeInstances, debug_message, debug_alert


def to_pix(x):
    return str(x) + 'px'


def from_pix(x):
    v = 0
    try:
        v = int(float(x.replace('px', '')))
    except Exception as e:
        debug_alert(traceback.format_exc())
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
    def __init__(self):
        # the runtime instances are processed every time a requests arrives, searching for the called method
        # if a class instance is not present in the runtimeInstances, it will
        # we not callable
        runtimeInstances.append(self)

        self.renderChildrenList = list()
        self.children = {}
        self.attributes = {}  # properties as class id style

        self.type = 'tag'
        self.attributes['id'] = str(id(self))
        self.attributes['class'] = self.__class__.__name__

    def __setitem__(self, key, value):
        """it is used for fast access to 'self.attributes[]'."""
        self.attributes[key] = value

    @staticmethod
    def _replace_client_specific_values(html, client):
        return html

    def repr(self, client, include_children = True):
        """it is used to automatically represent the object to HTML format
        packs all the attributes, children and so on."""
        classname = self.__class__.__name__

        # concatenating innerHTML. in case of html object we use repr, in case
        # of string we use directly the content
        innerHTML = ''
        for s in self.renderChildrenList:
            if isinstance(s, type('')):
                innerHTML = innerHTML + s
            elif include_children:
                innerHTML = innerHTML + s.repr(client)

        html = '<%s %s>%s</%s>' % (self.type, ' '.join(map(lambda k, v: k + "=\"" + str(
            v) + "\"", self.attributes.keys(), self.attributes.values())), innerHTML, self.type)
        return self._replace_client_specific_values(html, client)

    def append(self, key, value):
        """it allows to add child to this.

        The key can be everything you want, in order to access to the
        specific child in this way 'widget.children[key]'.

        """
        if hasattr(value, 'attributes'):
            value.attributes['parent_widget'] = str(id(self))

        if key in self.children.keys():
            self.renderChildrenList.remove(self.children[key])
        self.renderChildrenList.append(value)

        self.children[key] = value

    def remove(self, child):
        if child in self.children.values():
            #runtimeInstances.pop( runtimeInstances.index( self.children[key] ) )
            self.renderChildrenList.remove(child)
            for k in self.children.keys():
                if str(id(self.children[k])) == str(id(child)):
                    self.children.pop(k)
                    #when the child is removed we stop the iteration
                    #this implies that a child replication should not be allowed
                    break


class Widget(Tag):

    """base class for gui widgets.

    In html, it is a DIV tag    
    the "self.type" attribute specifies the HTML tag representation    
    the "self.attributes[]" attribute specifies the HTML attributes like "style" "class" "id" 
    the "self.style[]" attribute specifies the CSS style content like "font" "color". 
    It will be packet togheter with "self.attributes"

    """
    #constants
    LAYOUT_HORIZONTAL = True
    LAYOUT_VERTICAL = False

    def __init__(self, w=1, h=1, layout_orientation=LAYOUT_HORIZONTAL, widget_spacing=0):
        """w = numeric with
        h = numeric height
        layout_orientation = specifies the "float" css attribute
        widget_spacing = specifies the "margin" css attribute for the children"""
        super(Widget,self).__init__()

        self.style = {}

        self.type = 'div'

        self.layout_orientation = layout_orientation
        self.widget_spacing = widget_spacing

        # some constants for the events
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

        if w > -1:
            self.style['width'] = to_pix(w)
        if h > -1:
            self.style['height'] = to_pix(h)
        self.style['margin'] = '0px auto'

        self.oldRootWidget = None  # used when hiding the widget

        self.eventManager = EventManager()

    def repr(self, client, include_children = True):
        """it is used to automatically represent the widget to HTML format
        packs all the attributes, children and so on."""
        self['style'] = jsonize(self.style)

        return super(Widget,self).repr(client, include_children)

    def append(self, key, value):
        """it allows to add child widgets to this.

        The key can be everything you want, in order to access to the
        specific child in this way 'widget.children[key]'.

        """
        super(Widget,self).append(key, value)

        if hasattr(self.children[key], 'style'):
            spacing = to_pix(self.widget_spacing)
            selfHeight = 0
            selfWidth = 0
            if 'height' in self.style.keys() and 'height' in self.children[key].style.keys():
                selfHeight = from_pix(self.style['height']) - from_pix(self.children[key].style['height'])
            if 'width' in self.style.keys() and 'width' in self.children[key].style.keys():
                selfWidth = from_pix(self.style['width']) - from_pix(self.children[key].style['width'])
            self.children[key].style['margin'] = spacing + " " + to_pix(selfWidth/2)
            
            if self.layout_orientation:
                self.children[key].style['margin'] = to_pix(selfHeight/2) + " " + spacing
                if 'float' in self.children[key].style.keys():
                    if not (self.children[key].style['float'] == 'none'):
                        self.children[key].style['float'] = 'left'
                else:
                    self.children[key].style['float'] = 'left'

    def onfocus(self):
        return self.eventManager.propagate(self.EVENT_ONFOCUS, [])

    def set_on_focus_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONFOCUS] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONFOCUS)
        self.eventManager.register_listener(self.EVENT_ONFOCUS, listener, funcname)

    def onblur(self):
        return self.eventManager.propagate(self.EVENT_ONBLUR, [])

    def set_on_blur_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONBLUR] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONBLUR)
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
        if hasattr(self,'baseAppInstance'):
            self.baseAppInstance.client.root = self.oldRootWidget

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)


class Button(Widget):

    """
    button widget: implements the onclick event.
    """

    def __init__(self, w, h, text=''):
        super(Button, self).__init__(w, h)
        self.type = 'button'
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.set_text(text)

    def set_text(self, t):
        self.append('text', t)

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)


class TextInput(Widget):

    """multiline text area widget implements the onclick event.
    """

    def __init__(self, w, h, single_line=True):
        super(TextInput, self).__init__(w, h)
        self.type = 'textarea'

        self.EVENT_ONENTER = 'onenter'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['newValue']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self), 'evt':self.EVENT_ONCHANGE}
        self.set_text('')

        if single_line:
            self.style['resize'] = 'none'
            self.attributes['rows'] = '1'

    def set_text(self, t):
        """sets the text content."""
        self.append('text', t)

    def get_text(self):
        return self.children['text']

    def set_value(self, t):
        self.set_text(t)

    def get_value(self):
        #facility, same as get_text
        return self.get_text()

    def onchange(self, newValue):
        """returns the new text value."""
        self.set_text(newValue)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [newValue])

    def set_on_change_listener(self, listener, funcname):
        """register the listener for the onchange event."""
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)

    def onkeydown(self,newValue):
        """returns the new text value."""
        self.set_text(newValue)
        return self.eventManager.propagate(self.EVENT_ONKEYDOWN, [newValue])
        
    def set_on_key_down_listener(self,listener,funcname):
        self.attributes[self.EVENT_ONKEYDOWN] = \
            "var params={};params['newValue']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self), 'evt':self.EVENT_ONKEYDOWN}
        self.eventManager.register_listener(self.EVENT_ONKEYDOWN, listener, funcname)

    def onenter(self,newValue):
        """returns the new text value."""
        self.set_text(newValue)
        return self.eventManager.propagate(self.EVENT_ONENTER, [newValue])

    def set_on_enter_listener(self,listener,funcname):
        self.attributes[self.EVENT_ONKEYDOWN] = """
            if (event.keyCode == 13) {
                var params={};
                params['newValue']=document.getElementById('%(id)s').value;
                sendCallbackParam('%(id)s','%(evt)s',params);
                return false;
            }""" % {'id':id(self), 'evt':self.EVENT_ONENTER}
        self.eventManager.register_listener(self.EVENT_ONENTER, listener, funcname)


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
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)


class GenericDialog(Widget):

    """input dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "confirm_value" and "cancel_dialog" events."""

    def __init__(self, width=500, height=160, title='Title', message='Message'):
        self.width = width
        self.height = height
        super(GenericDialog, self).__init__(self.width, self.height, Widget.LAYOUT_VERTICAL, 10)

        self.EVENT_ONCONFIRM = 'confirm_dialog'
        self.EVENT_ONCANCEL = 'cancel_dialog'

        t = Label(self.width - 20, 50, title)
        m = Label(self.width - 20, 30, message)

        self.container = Widget(self.width - 20,0, Widget.LAYOUT_VERTICAL, 0)
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

        self.conf.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCONFIRM)
        self.cancel.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCANCEL)

        self.inputs = {}

        self.baseAppInstance = None

    def add_field_with_label(self,key,labelDescription,field):
        fields_spacing = 5
        field_height = from_pix(field.style['height']) + fields_spacing*2
        field_width = from_pix(field.style['width']) + fields_spacing*4
        self.style['height'] = to_pix(from_pix(self.style['height']) + field_height)
        self.container.style['height'] = to_pix(from_pix(self.container.style['height']) + field_height)
        self.inputs[key] = field
        label = Label(self.width-20-field_width-1, 30, labelDescription )
        container = Widget(self.width-20, field_height, Widget.LAYOUT_HORIZONTAL, fields_spacing)
        container.append('lbl' + key,label)
        container.append(key, self.inputs[key])
        self.container.append(key, container)
        
    def add_field(self,key,field):
        fields_spacing = 5
        field_height = from_pix(field.style['height']) + fields_spacing*2
        field_width = from_pix(field.style['width']) + fields_spacing*4
        self.style['height'] = to_pix(from_pix(self.style['height']) + field_height)
        self.container.style['height'] = to_pix(from_pix(self.container.style['height']) + field_height)
        self.inputs[key] = field
        container = Widget(self.width-20, field_height, Widget.LAYOUT_HORIZONTAL, fields_spacing)
        container.append(key, self.inputs[key])
        self.container.append(key, container)

    def get_field(self, key):
        return self.inputs[key]

    def confirm_dialog(self):
        """event called pressing on OK button.
        """
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCONFIRM, [])

    def set_on_confirm_dialog_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCONFIRM, listener, funcname)

    def cancel_dialog(self):
        self.hide()
        return self.eventManager.propagate(self.EVENT_ONCANCEL, [])

    def set_on_cancel_dialog_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCANCEL, listener, funcname)


class InputDialog(GenericDialog):

    """input dialog, it opens a new webpage allows the OK/CANCEL functionality
    implementing the "confirm_value" and "cancel_dialog" events."""

    def __init__(self, width=500, height=160, title='Title', message='Message',
                    initial_value=''):
        super(InputDialog, self).__init__(width, height, title, message)

        self.inputText = TextInput(width - 20, 30)
        self.inputText.set_on_enter_listener(self,'on_text_enter_listener')
        self.add_field('textinput',self.inputText)
        self.inputText.set_text(initial_value)

        self.EVENT_ONCONFIRMVALUE = 'confirm_value'
        self.set_on_confirm_dialog_listener(self, 'confirm_value')

    def on_text_enter_listener(self,value):
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

    def set_on_confirm_value_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCONFIRMVALUE, listener, funcname)


class ListView(Widget):

    """list widget it can contain ListItems."""

    def __init__(self, w, h, orientation=Widget.LAYOUT_VERTICAL):
        super(ListView, self).__init__(w, h, orientation)
        self.type = 'ul'
        self.EVENT_ONSELECTION = 'onselection'
        self.selected_item = None
        self.selected_key = None

    def append(self, key, item):
        # if an event listener is already set for the added item, it will not generate a selection event
        if item.attributes[self.EVENT_ONCLICK] == '':
            item.set_on_click_listener(self, self.EVENT_ONSELECTION)
        item.attributes['selected'] = False
        super(ListView, self).append(key, item)

    def onselection(self, clicked_item):
        self.selected_key = None
        for k in self.children:
            if self.children[k] == clicked_item:
                self.selected_key = k
                debug_message('ListView - onselection. Selected item key: ',k)
                if self.selected_item is not None:
                    self.selected_item['selected'] = False
                self.selected_item = self.children[self.selected_key]
                self.selected_item['selected'] = True
                break
        return self.eventManager.propagate(self.EVENT_ONSELECTION, [self.selected_key])

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

    def select_by_key(self, itemKey):
        """
        selects an item by its key
        """
        self.selected_key = None
        self.selected_item = None
        for item in self.children.values():
            item.attributes['selected'] = False

        if itemKey in self.children:
            self.children[itemKey].attributes['selected'] = True
            self.selected_key = itemKey
            self.selected_item = self.children[itemKey]

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
        
    def get_value(self):
        return self.get_text()

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [self])


class DropDown(Widget):

    """combo box widget implements the onchange event.
    """

    def __init__(self, w, h):
        super(DropDown, self).__init__(w, h)
        self.type = 'select'
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['newValue']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self),
                                                               'evt':self.EVENT_ONCHANGE}
        self.selected_item = None
        self.selected_key = None
        
    def select_by_key(self, itemKey):
        """
        selects an item by its key
        """
        for item in self.children.values():
            if 'selected' in item.attributes:
                del item.attributes['selected']
        self.children[itemKey].attributes['selected'] = 'selected'
        self.selected_key = itemKey
        self.selected_item = self.children[itemKey]

    def set_value(self, newValue):
        """
        selects the item by the contained text
        """
        self.selected_key = None
        self.selected_item = None
        for k in self.children:
            item = self.children[k]
            if item.attributes['value'] == newValue:
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

    def onchange(self, newValue):
        debug_message('combo box. selected', newValue)
        self.set_value(newValue)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [newValue])

    def set_on_change_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)


class DropDownItem(Widget):

    """item widget for the DropDown implements the onclick event.
    """

    def __init__(self, w, h, text):
        super(DropDownItem, self).__init__(w, h)
        self.type = 'option'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)

    def set_text(self, text):
        self.attributes['value'] = text
        self.append('text', text)

    def get_text(self):
        return self.attributes['value']

    def set_value(self, text):
        return self.set_text(text)

    def get_value(self):
        return self.get_text()


class Image(Widget):

    """image widget."""

    def __init__(self, w, h, filename):
        """filename should be an URL."""
        super(Image, self).__init__(w, h)
        self.type = 'img'
        self.attributes['src'] = filename

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)


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
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['newValue']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self),
                                                               'evt':self.EVENT_ONCHANGE}
        self.attributes['value'] = str(defaultValue)
        self.attributes['type'] = _type

    def set_value(self,value):
        self.attributes['value'] = str(value)

    def get_value(self):
        """returns the new text value."""
        return self.attributes['value']

    def onchange(self, newValue):
        self.attributes['value'] = newValue
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [newValue])

    def set_on_change_listener(self, listener, funcname):
        """register the listener for the onchange event."""
        self.eventManager.register_listener(self.EVENT_ONCHANGE, listener, funcname)


class CheckBoxLabel(Widget):
    def __init__(self, w, h, label='', checked=False, user_data=''):
        super(CheckBoxLabel, self).__init__(w, h, Widget.LAYOUT_HORIZONTAL)
        inner_checkbox_width = 30
        inner_label_padding_left = 10
        self._checkbox = CheckBox(inner_checkbox_width, h, checked, user_data)
        self._label = Label(w-inner_checkbox_width-inner_label_padding_left, h, label)
        self.append('checkbox', self._checkbox)
        self.append('label', self._label)
        self._label.style['padding-left'] = to_pix(inner_label_padding_left)

        self.set_value = self._checkbox.set_value
        self.get_value = self._checkbox.get_value
        self.set_on_change_listener = self._checkbox.set_on_change_listener
        self.onchange = self._checkbox.onchange


class CheckBox(Input):

    """check box widget usefull as numeric input field implements the onchange
    event.
    """

    def __init__(self, w, h, checked=False, user_data=''):
        super(CheckBox, self).__init__(w, h, 'checkbox', user_data)
        self.attributes[self.EVENT_ONCHANGE] = \
            "var params={};params['newValue']=document.getElementById('%(id)s').checked;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self),
                                                               'evt':self.EVENT_ONCHANGE}
        self.set_value(checked)

    def onchange(self, newValue):
        self.set_value( newValue in ('True', 'true') )
        return self.eventManager.propagate(self.EVENT_ONCHANGE, [newValue])

    def set_value(self, checked):
        if checked:
            self.attributes['checked']='checked'
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

    def __init__(self, w, h, defaultValue='100', min=100, max=5000, step=1):
        super(SpinBox, self).__init__(w, h, 'number', defaultValue)
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['step'] = str(step)


class Slider(Input):

    def __init__(self, w, h, defaultValue='', min=0, max=10000, step=1):
        super(Slider, self).__init__(w, h, 'range', defaultValue)
        self.attributes['min'] = str(min)
        self.attributes['max'] = str(max)
        self.attributes['step'] = str(step)
        self.EVENT_ONINPUT = 'oninput'

    def oninput(self, newValue):
        return self.eventManager.propagate(self.EVENT_ONINPUT, [newValue])

    def set_oninput_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONINPUT] = \
            "var params={};params['newValue']=document.getElementById('%(id)s').value;"\
            "sendCallbackParam('%(id)s','%(evt)s',params);" % {'id':id(self), 'evt':self.EVENT_ONINPUT}
        self.eventManager.register_listener(self.EVENT_ONINPUT, listener, funcname)


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
        super(FileFolderNavigator, self).__init__(w, h, Widget.LAYOUT_VERTICAL)
        self.w = w
        self.h = h
        self.multiple_selection = multiple_selection
        self.sep = os.sep #'/' #default separator in path os.sep

        self.selectionlist = list()  # here are stored selected files and folders
        self.controlsContainer = Widget(w, 25, Widget.LAYOUT_HORIZONTAL)
        self.controlBack = Button(45, 25, 'Up')
        self.controlBack.set_on_click_listener(self, 'dir_go_back')
        self.controlGo = Button(45, 25, 'Go >>')
        self.controlGo.set_on_click_listener(self, 'dir_go')
        self.pathEditor = TextInput(w-90, 25)
        self.pathEditor.style['resize'] = 'none'
        self.pathEditor.attributes['rows'] = '1'
        self.controlsContainer.append('1', self.controlBack)
        self.controlsContainer.append('2', self.pathEditor)
        self.controlsContainer.append('3', self.controlGo)

        self.itemContainer = Widget(w, h-25, Widget.LAYOUT_VERTICAL)
        self.itemContainer.style['overflow-y'] = 'scroll'
        self.itemContainer.style['overflow-x'] = 'hidden'

        self.append('controls', self.controlsContainer)
        self.append('items', self.itemContainer)

        self.folderItems = list()
        self.chdir(selection_folder)  # move to actual working directory

    def get_selection_list(self):
        return self.selectionlist

    def populate_folder_items(self,directory):
        fpath = directory + self.sep
        debug_message("FileFolderNavigator - populate_folder_items")
        l = os.listdir(directory)
        # used to restore a valid path after a wrong edit in the path editor
        self.lastValidPath = directory 
        # we remove the container avoiding graphic update adding items
        # this speeds up the navigation
        self.remove(self.itemContainer)
        # creation of a new instance of a itemContainer
        self.itemContainer = Widget(self.w,self.h-25,Widget.LAYOUT_VERTICAL)
        self.itemContainer.style['overflow-y'] = 'scroll'
        self.itemContainer.style['overflow-x'] = 'hidden'

        for i in l:
            isFolder = not os.path.isfile(fpath+i)
            fi = FileFolderItem(self.w, 33, i, isFolder)
            fi.set_on_click_listener(self, 'on_folder_item_click')  # navigation purpose
            fi.set_on_selection_listener(self, 'on_folder_item_selected')  # selection purpose
            self.folderItems.append(fi)
            self.itemContainer.append(i, fi)
        self.append('items', self.itemContainer)

    def dir_go_back(self):
        curpath = os.getcwd()  # backup the path
        try:
            os.chdir( self.pathEditor.get_text() )
            os.chdir('..')
            self.chdir(os.getcwd())
        except Exception as e:
            self.pathEditor.set_text(self.lastValidPath)
            debug_alert(traceback.format_exc())
        os.chdir(curpath)  # restore the path

    def dir_go(self):
        # when the GO button is pressed, it is supposed that the pathEditor is changed
        curpath = os.getcwd()  # backup the path
        try:
            os.chdir(self.pathEditor.get_text())
            self.chdir(os.getcwd())
        except Exception as e:
            debug_alert(traceback.format_exc())
            self.pathEditor.set_text(self.lastValidPath)
        os.chdir(curpath)  # restore the path

    def chdir(self, directory):
        curpath = os.getcwd()  # backup the path
        debug_message("FileFolderNavigator - chdir:" + directory + "\n")
        for c in self.folderItems:
            self.itemContainer.remove(c)  # remove the file and folders from the view
        self.folderItems = []
        self.selectionlist = []  # reset selected file list
        os.chdir(directory)
        directory = os.getcwd()
        self.populate_folder_items(directory)
        self.pathEditor.set_text(directory)
        os.chdir(curpath)  # restore the path

    def on_folder_item_selected(self,folderitem):
        if not self.multiple_selection:
            self.selectionlist = []
            for c in self.folderItems:
                c.set_selected(False)
            folderitem.set_selected(True)
        debug_message("FileFolderNavigator - on_folder_item_click")
        # when an item is clicked it is added to the file selection list
        f = self.pathEditor.get_text() + self.sep + folderitem.get_text()
        if f in self.selectionlist:
            self.selectionlist.remove(f)
        else:
            self.selectionlist.append(f)

    def on_folder_item_click(self,folderitem):
        debug_message("FileFolderNavigator - on_folder_item_dblclick")
        # when an item is clicked two time
        f = self.pathEditor.get_text() + self.sep + folderitem.get_text()
        if not os.path.isfile(f):
            self.chdir(f)

    def get_selected_filefolders(self):
        return self.selectionlist


class FileFolderItem(Widget):

    """FileFolderItem widget for the FileFolderNavigator implements the onclick event."""

    def __init__(self, w, h, text, isFolder=False):
        super(FileFolderItem, self).__init__(w, h, Widget.LAYOUT_HORIZONTAL)
        self.EVENT_ONSELECTION = 'onselection'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.icon = Widget(33, h)
        # the icon click activates the onselection event, that is propagates to registered listener
        if isFolder:
            self.icon.set_on_click_listener(self, self.EVENT_ONCLICK)
        self.icon.attributes['class'] = 'FileFolderItemIcon'
        icon_file = 'res/folder.png' if isFolder else 'res/file.png'
        self.icon.style['background-image'] = "url('%s')" % icon_file
        self.label = Label(w-33, h, text)
        self.label.set_on_click_listener(self, self.EVENT_ONSELECTION)
        self.append('icon', self.icon)
        self.append('text', self.label)
        self.selected = False

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [self])

    def set_on_click_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)

    def set_selected(self, selected):
        self.selected = selected
        self.style['color'] = 'red' if self.selected else 'black'

    def onselection(self):
        self.set_selected(not self.selected)
        return self.eventManager.propagate(self.EVENT_ONSELECTION, [self])

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

    def __init__(self, width = 600, fileFolderNavigatorHeight=210, title='File dialog',
                 message='Select files and folders', multiple_selection=True, selection_folder='.'):
        super(FileSelectionDialog, self).__init__(width, 160, title, message)
        self.fileFolderNavigator = FileFolderNavigator(width-20, fileFolderNavigatorHeight,
                                                       multiple_selection, selection_folder)
        self.add_field('fileFolderNavigator',self.fileFolderNavigator)
        self.EVENT_ONCONFIRMVALUE = 'confirm_value'
        self.set_on_confirm_dialog_listener(self, 'confirm_value')

    def confirm_value(self):
        """event called pressing on OK button.
           propagates the string content of the input field
        """
        self.hide()
        params = [self.fileFolderNavigator.get_selection_list()]
        return self.eventManager.propagate(self.EVENT_ONCONFIRMVALUE, params)

    def set_on_confirm_value_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ONCONFIRMVALUE, listener, funcname)


class Menu(Widget):

    """Menu widget can contain MenuItem."""

    def __init__(self, w, h, orientation=Widget.LAYOUT_HORIZONTAL):
        super(Menu, self).__init__(w, h, orientation)
        self.type = 'ul'


class MenuItem(Widget):
    
    """MenuItem widget can contain other MenuItem."""

    def __init__(self, w, h, text):
        super(MenuItem, self).__init__(w, h)
        self.w = w
        self.h = h
        self.subcontainer = None
        self.type = 'li'
        self.attributes[self.EVENT_ONCLICK] = ''
        self.set_text(text)
        self.append = self.addSubMenu

    def addSubMenu(self, key, value):
        if self.subcontainer is None:
            self.subcontainer = Menu(self.w, self.h, Widget.LAYOUT_VERTICAL)
            super(MenuItem, self).append('subcontainer', self.subcontainer)
        self.subcontainer.append(key, value)

    def set_text(self, text):
        self.append('text', text)

    def get_text(self):
        return self.children['text']

    def onclick(self):
        return self.eventManager.propagate(self.EVENT_ONCLICK, [])

    def set_on_click_listener(self, listener, funcname):
        self.attributes[self.EVENT_ONCLICK] = "sendCallback('%s','%s');" % (id(self), self.EVENT_ONCLICK)
        self.eventManager.register_listener(self.EVENT_ONCLICK, listener, funcname)


class FileUploader(Widget):

    """
    FileUploader widget:
        allows to upload multiple files to a specified folder.
        implements the onsuccess and onfailed events.
    """

    def __init__(self, w, h, savepath='./', multiple_selection_allowed=False):
        super(FileUploader, self).__init__(w, h)
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

        fileUploadScript = """
        function uploadFile(savePath,file){
            var url = '/';
            var xhr = new XMLHttpRequest();
            var fd = new FormData();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('savepath', savePath);
            xhr.setRequestHeader('filename', file.name);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    /* Every thing ok, file uploaded */
                    var params={};params['filename']=file.name;
                    sendCallbackParam('%(id)s','%(evt_success)s',params);
                    console.log('upload success: ' + file.name);
                }else if(xhr.status == 400){
                    var params={};params['filename']=file.name;
                    sendCallbackParam('%(id)s','%(evt_failed)s',params);
                    console.log('upload failed: ' + file.name);
                }
            };
            fd.append('upload_file', file);
            xhr.send(fd);
        };
        var files = this.files;for(var i=0; i<files.length; i++){uploadFile('%(savepath)s',files[i]);}
        """ % {'id':id(self),
               'evt_success':self.EVENT_ON_SUCCESS, 'evt_failed':self.EVENT_ON_FAILED,
               'savepath':self._savepath}

        self.attributes[self.EVENT_ONCHANGE] = fileUploadScript
        
    def onsuccess(self,filename):
        return self.eventManager.propagate(self.EVENT_ON_SUCCESS, [filename])

    def set_on_success_listener(self, listener, funcname):
        self.eventManager.register_listener(
            self.EVENT_ON_SUCCESS, listener, funcname)

    def onfailed(self,filename):
        return self.eventManager.propagate(self.EVENT_ON_FAILED, [filename])

    def set_on_failed_listener(self, listener, funcname):
        self.eventManager.register_listener(self.EVENT_ON_FAILED, listener, funcname)
        

class FileDownloader(Widget):

    """FileDownloader widget. Allows to start a file download."""

    def __init__(self, w, h, text, filename, path_separator='/'):
        super(FileDownloader, self).__init__(w, h, Widget.LAYOUT_HORIZONTAL)
        self.type = 'a'
        self.attributes['download'] = os.path.basename(filename)
        self.attributes['href'] = "/%s/download" % id(self)
        self.set_text(text)
        self._filename = filename
        self._path_separator = path_separator

    def set_text(self, t):
        self.append('text', t)

    def download(self):
        with open(self._filename, 'r+b') as f:
            content = f.read()
        headers = {'Content-type':'application/octet-stream',
                   'Content-Disposition':'attachment; filename=%s' % os.path.basename(self._filename)}
        return [content,headers]


class Link(Widget):

    def __init__(self, w, h, url, text, open_new_window=True):
        super(Link, self).__init__(w, h)
        self.type = 'a'
        self.attributes['href'] = url
        if open_new_window:
            self.attributes['target'] = "_blank"
        self.set_text(text)

    def set_text(self, t):
        self.append('text', t)

    def get_text(self):
        return self.children['text']

    def get_url(self):
        return self.children['href']


class VideoPlayer(Widget):

    def __init__(self, w, h, video, poster=None):
        super(VideoPlayer, self).__init__(w, h, Widget.LAYOUT_HORIZONTAL)
        self.type = 'video'
        self.attributes['src'] = video
        self.attributes['preload'] = 'auto'
        self.attributes['controls'] = None
        self.attributes['poster'] = poster