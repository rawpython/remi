# -*- coding: utf-8 -*-

import remi
import remi.gui as gui
from remi.gui import *
import snap7
import threading
from threading import Timer
import traceback

# https://python-snap7.readthedocs.io/en/latest/util.html
# https://github.com/gijzelaerr/python-snap7/blob/master/example/boolean.py


style_inheritance_dict = {'opacity':'inherit', 'overflow':'inherit', 'background-color':'inherit', 'background-image':'inherit', 'background-position':'inherit', 'background-repeat':'inherit', 'border-color':'inherit', 'border-width':'inherit', 'border-style':'inherit', 'border-radius':'inherit', 'color':'inherit', 'font-family':'inherit', 'font-size':'inherit', 'font-style':'inherit', 'font-weight':'inherit', 'white-space':'inherit', 'letter-spacing':'inherit'}
style_inheritance_text_dict = {'opacity':'inherit', 'overflow':'inherit', 'color':'inherit', 'font-family':'inherit', 'font-size':'inherit', 'font-style':'inherit', 'font-weight':'inherit', 'white-space':'inherit', 'letter-spacing':'inherit'}


class PLCSiemens(Image):
    """ This is a snap7 interface that allows to communicate with Siemens PLC.
        It handles the connection and reconnection.
        Widgets' event "link_to" have to be connected to this widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAvCAYAAAAIA1FgAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAADmwAAA5sBPN8HMQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANGSURBVFiF7ZbNbxtFGIefmR2vP+PUjkntxHGapmmpKpIoECggjpyQEBKqeoIjXDhw5cD/wZ0LEgiJEzck1EIrlUYBl7RJ1bQlbUpCHNux15+7MxycWnLzoX6sJZDyk1bzzsc+s/q9s7uv+PTzL40dCBCLRShsl/A8j1K5AoARnet5JAyoWDSC1hpjIDuS5sH6390Fi+9WyL49zungCPdam+TsFAMyjKObLNRXmbTTTIdyXKrdIiJsitohq4YoeBUWf19C3fvr4b47G2MAmLTTnLLTDMgQuUCKpeYDzgZHOR+eYt0tMmmn+cm5wRfDF/mm/AspK85qe4NFQBKuQ7gOyu2BFzYfAeChSVhRbKGomxbbXpU7rQ1iMoRGs+mWcY3mu52rvBaepKirnLYzHWsu3MAAmF/nMZfe6MK3NtZpvpOkOOYSt6N4xiNk2QQtm1KzihAgkcSDEZx2g4bXRglJW7sIIVGPXNRhSRldCTG68rinAA00SPbc1iABQGC3b+22AZT+/r1dH44dts9zSXF7wndoFy4++BEAs3wKbk75DD9zpxMVkp3M+gk3q7lOtN0Hz8237/sO7cLFiTUATGkQSnGf4Rd/6ERPvER+SPpKe0LKfPUxAKYR7AO87K/PPXD5ydcAmIVpzG8z/sJJlDtRuOErGECZq3OdaG2kZ0JaL55rZX5+a9+JZCr9wvC+HsX+nvP7q7do1mv+gwM2avzky76DH6u/tuw3eH5+FsepUW80GRtNc/nKdeZmzlGuVKlWHWZfOcv9tYfUG01i0QiBgOLaQv7p4JZloZRiKBkmffwl5mbOIaXg5IksrVabfwrb5JdWeHN+FtfTLOZv7vvke2yxLInahTtOjT/+XCYSCaGNYfXuGuWdCrVaHYBK1UFKweuvTiPE3qJSfPjRZ37/Ors6sCjKZTMMxgeoVB3GshkuX7nOYHyA1FCCUnmHWDRKq9VCStlTvD4VfDRzHBVQ5JdWyKSHMcbgeR5npibYKhS764QQzw53PY/EsUFGMsNsbG4xMZ4lFArSarURQhAOh2i32wgOLuAPhF9byKOUhet6PePLt++itUZK2S2znxkO7AEDaK172sP0//0qHsGP4Efw/zL8X7xWNIa0/NaYAAAAAElFTkSuQmCC"

    #OpencvImage inherits gui.Image and so it already inherits attr_src. 
    # I'm redefining it in order to avoid editor_attribute_decorator
    # and so preventing it to be shown in editor.
    @property
    def attr_src(self): return self.attributes.get('src', '')
    @attr_src.setter
    def attr_src(self, value): self.attributes['src'] = str(value)

    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The IP address as string', str, {})
    def ip_address(self): return self.__dict__.get('__ip_address', '127.0.0.1')
    @ip_address.setter
    def ip_address(self, v): 
        self.__dict__['__ip_address'] = v
        self.disconnect()
        self.connect()

    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The rack number as integer', int, {'possible_values': '', 'min': -1, 'max': 65535, 'default': 0, 'step': 1})
    def rack(self): return self.__dict__.get('__rack', -1)
    @rack.setter
    def rack(self, v): 
        self.__dict__['__rack'] = v
        self.disconnect()
        self.connect()

    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The slot number as integer', int, {'possible_values': '', 'min': -1, 'max': 65535, 'default': 0, 'step': 1})
    def slot(self): return self.__dict__.get('__slot', -1)
    @slot.setter
    def slot(self, v): 
        self.__dict__['__slot'] = v
        self.disconnect()
        self.connect()
        
    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The update interval in seconds as float', float, {'possible_values': '', 'min': 0.0, 'max': 655350.0, 'default': 1.0, 'step': 1})
    def update_interval(self): return self.__dict__.get('__update_interval', 1.0)
    @update_interval.setter
    def update_interval(self, v): 
        self.__dict__['__update_interval'] = v
        #self.disconnect()
        #self.connect()

    snap7_client = snap7.client.Client()    #the snap7.client.Client() instance that manages data exchange with PLC  
    connected = False
    linked_widgets = []                     #the widget list that are linked to the PLC
    update_lock = threading.RLock()
    app_instance = None

    def __init__(self, ip_address='', rack=0, slot=3, update_interval=1.0, *args, **kwargs):
        self.__ip_address = ''
        default_style = {'position':'absolute','left':'10px','top':'10px'}
        default_style.update(kwargs.get('style',{}))
        kwargs['style'] = default_style
        kwargs['width'] = kwargs['style'].get('width', kwargs.get('width','23px'))
        kwargs['height'] = kwargs['style'].get('height', kwargs.get('height','47px'))
        super(PLCSiemens, self).__init__(self.icon, *args, **kwargs)
        self.on_disconnected()
        self._set_params()
        self.__rack = rack
        self.__slot = slot
        if len(ip_address):
            self.ip_address = ip_address
        else:
            self.__ip_address = ip_address
        self.__update_interval = update_interval
        self.check_connection_state()

    def disconnect(self):
        try:
            self.snap7_client.disconnect()
        except Exception:
            print(traceback.format_exc())

    def connect(self):
        try:
            if self.rack<0 or self.slot<0:
                return
            print("connecting to ip:%s  rack:%s  slot:%s"%(self.ip_address, self.rack, self.slot))
            self.snap7_client.connect(self.ip_address, self.rack, self.slot)
            
        except Exception:
            print(traceback.format_exc())

    def _set_params(self):
        values = ()
        """(
                (snap7.snap7types.PingTimeout, 1000),
                (snap7.snap7types.SendTimeout, 500),
                (snap7.snap7types.RecvTimeout, 3500),
                (snap7.snap7types.SrcRef, 128),
                (snap7.snap7types.DstRef, 128),
                (snap7.snap7types.SrcTSap, 128),
                (snap7.snap7types.PDURequest, 470)
            )
        """
        for param, value in values:
            self.snap7_client.set_param(param, value)

    def get_cpu_info(self):
        """ i.e.
            ('ModuleTypeName', 'CPU 315-2 PN/DP'),
            ('SerialNumber', 'S C-CXXXXXXXXXXX'),
            ('ASName', 'SNAP7-SERVER'),
            ('Copyright', 'Original Siemens Equipment'),
            ('ModuleName', 'CPU 315-2 PN/DP')
        """
        fields = ('ModuleTypeName','SerialNumber','ASName','Copyright','ModuleName')
        cpuInfo = self.snap7_client.get_cpu_info()
        info_string = "IP address: %s\n"%self.ip_address
        for field in fields:
            info_string = info_string + "%s: %s\n"%(field,str(getattr(cpuInfo, field, '')))
        return info_string

    @decorate_event
    def on_connected(self):
        self.attributes['title'] =  "IP address: %s"%self.ip_address #self.get_cpu_info()
        return ()

    @decorate_event
    def on_disconnected(self):
        self.attributes['title'] = "%s : not connected"%self.ip_address
        return ()

    def __del__(self):
        self.update_interval = 0
        self.snap7_client.destroy()

    def search_app_instance(self, node):
        if issubclass(node.__class__, remi.server.App):
            return node
        if not hasattr(node, "get_parent"):
            return None
        return self.search_app_instance(node.get_parent()) 

    def check_connection_state(self):
        _con = self.snap7_client.get_connected()
        if _con != self.connected:
            if _con:
                self.on_connected()
            else:
                self.on_disconnected()
        self.connected = _con

        if self.app_instance==None:
            self.app_instance = self.search_app_instance(self)
            
        if self.app_instance:
            with self.update_lock:
                with self.app_instance.update_lock:
                    for w in self.linked_widgets:
                        if hasattr(w, "update"):
                            try:
                                w.update()
                            except Exception:
                                print(traceback.format_exc())

        if self.update_interval>0.0:
            Timer(self.update_interval, self.check_connection_state).start()

    def set_bool(self, db_index, byte_index, bit_index, value):
        reading = self.snap7_client.db_read(db_index, byte_index, 1)    # read 1 byte from db 31 staring from byte 120
        snap7.util.set_bool(reading, 0, bit_index, value)   # set a value of fifth bit
        self.snap7_client.db_write(db_index, byte_index, reading)    # write back the bytearray and now the boolean value is changed 

    def get_bool(self, db_index, byte_index, bit_index):
        bytes_to_read_write = 1
        mem = self.snap7_client.db_read(db_index, byte_index, bytes_to_read_write)
        return snap7.util.get_bool(mem, byte_index, bit_index)

    def get_byte(self, db_index, byte_index):
        bytes_to_read_write = 1
        mem = self.snap7_client.db_read(db_index, byte_index, bytes_to_read_write)
        return bytearray(mem)

    def set_int(self, db_index, byte_index, value):
        mem = self.snap7_client.db_read(db_index, byte_index, 2)
        snap7.util.set_int(mem, 0, value)
        self.snap7_client.db_write(db_index, byte_index, mem)

    def get_int(self, db_index, byte_index):
        mem = self.snap7_client.db_read(db_index, byte_index, 2) #an int from 2 bytes
        return snap7.util.get_int(mem, 0) #0 or byte_index?

    def set_real(self, db_index, byte_index, value):
        mem = self.snap7_client.db_read(db_index, byte_index, 4)
        snap7.util.set_real(mem, 0, value)
        self.snap7_client.db_write(db_index, byte_index, mem)

    def get_real(self, db_index, byte_index):
        mem = self.snap7_client.db_read(db_index, byte_index, 4) #a real from 4 bytes
        return snap7.util.get_real(mem, 0) #0 or byte_index?

    def set_string(self, db_index, byte_index, max_size, value):
        mem = self.snap7_client.db_read(db_index, byte_index, max_size)
        snap7.util.set_string(mem, 0, value, max_size)
        self.snap7_client.db_write(db_index, byte_index, mem)

    def get_string(self, db_index, byte_index, max_size):
        mem = self.snap7_client.db_read(db_index, byte_index, max_size)
        return snap7.util.get_string(mem, 0, max_size) #0 or byte_index?

    def on_link_to(self, widget):
        """ Each widget registers itself to the PLC class by linking its "link_to" event 
            toward the "on_link_to" listener
        """
        with self.update_lock:
            widget.set_plc_instance(self)
            #the widget is appended to a link for cyclical update purpose
            self.linked_widgets.append(widget)

    def remove_link_to(self, widget):
        with self.update_lock:
            self.linked_widgets.remove(widget)


# noinspection PyUnresolvedReferences
class SiemensWidget(object):
    plc_instance = None

    def _setup(self):
        #this must be called after the Widget super constructor
        self.link_to.do = self.do

    def do(self, callback, *userdata):
        if self.plc_instance and (callback is None):
            print("removing connection to the PLC")
            self.plc_instance.remove_link_to(self)
            self.plc_instance = None

        if hasattr(self.link_to.event_method_bound, '_js_code'):
            self.link_to.event_source_instance.attributes[self.link_to.event_name] = self.link_to.event_method_bound._js_code%{
                'emitter_identifier':self.link_to.event_source_instance.identifier, 'event_name':self.link_to.event_name}
        self.link_to.callback = callback
        self.link_to.userdata = userdata
        self.link_to.kwuserdata = {}
        #here the callback is called immediately to make it possible link to the plc
        if callback is not None: #protection against the callback replacements in the editor
            callback(self, *userdata)

    @decorate_set_on_listener("(self, emitter)")
    @decorate_event
    def link_to(self):
        return ()

    def set_plc_instance(self, plc_instance):
        self.plc_instance = plc_instance


class _Mixin_DB_property():
    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The DB number as integer', int, {'possible_values': '', 'min': -1, 'max': 65535, 'default': 0, 'step': 1})
    def db_index(self): return self.__dict__.get('__db_index', -1)
    @db_index.setter
    def db_index(self, v): self.__dict__['__db_index'] = v

class _Mixin_Byte_property():
    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The byte index in the DB as integer', int, {'possible_values': '', 'min': -1, 'max': 65535, 'default': 0, 'step': 1})
    def byte_index(self): return self.__dict__.get('__byte_index', -1)
    @byte_index.setter
    def byte_index(self, v): self.__dict__['__byte_index'] = v

class _Mixin_Bit_property():
    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The bit index in the byte as integer', int, {'possible_values': '', 'min': -1, 'max': 65535, 'default': 0, 'step': 1})
    def bit_index(self):  return self.__dict__.get('__bit_index', -1)
    @bit_index.setter
    def bit_index(self, v): self.__dict__['__bit_index'] = v


class SiemensButton(gui.Container, SiemensWidget, _Mixin_DB_property, _Mixin_Byte_property, _Mixin_Bit_property):
    """ A Button widget that sets the bit when clicked.
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAuCAYAAABXuSs3AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAKMSURBVGiB7ZqxaxNRGMB/9+7uXZK2aaMVEUWEKNSh4CQIrhWnujiIQqGig7gXF/+B7tLNbp2KQyfBwcVdsdhWJa5WHZKKvZqXe3cO57VNmraJyd0ZuB88LnkvfO/H43sfB18Mz/OCIAhoN4DdZ9IYhrH7bDesSPJlRfHsrc+nmpGK6HGcGQp4clVwsywBMJRSgVKKqWXNpitS1juaS6M+L26ZSCnDE1dKsenaAHy/MUNjtNJ10JG1WYofHvTbtYnPWwKlFLZth+Ke5wGheKP0EXVireugemizz5rt8TyPIAgQe+KDQZO41jptn47RWofiAL7vp+3TMZGrtb9mAxTfP0bnf3QdMPf1Wt/kjiLytVoXRtZnEhHolf+7cB9BJp40mXjSDKz4gXLYHQ6vHtmUD8z7LC+4zAGz00M8PXv4q3Jl4xdTr7vfuUfx9pvP3xnm9v086893WFzZZjFamMzz7rpg7c02d1d72zOWVJn75oNjcDmO4H+JRXz+tKCyEaZKXPQlVcoTw3yZaJ776dpAox/h2xJLjocXUrI02eg5lw8jllRZXPGoYHBqPI7oIQNbx2MRn522KNc1S/9Qnzslpsvps7yws1e/Y6BH8TpTC/XOf766w5U+XdYsx5MmE0+aTDxpMvGkycSTRkTNoEEh8hXRl0Ehch3cEzcMA9M0GbdV2k7Hcj7/G9M098Qty+LhxSrnHDdtt0M5adW5d2ELy7LCU1dKBa7rUqvVqFaruK5LvV5Ptbvc2lV2HIdCoUCpVGJsbIxCoYAVLRSLRaSUKKVQStHaYkmDSFxKiZSSXC6H4zjhvOd5ge/7aK2bRtQkSruXL4TANM2mIYTA0FoHrWmR9h8QIlpTZv/nP6KyI2uh/zMtAAAAAElFTkSuQmCC"

    @property
    @gui.editor_attribute_decorator('WidgetSpecific','Specifies if the button is toggle or must reset the value on release', bool, {})
    def toggle(self): return self.__dict__.get('__toggle', None)
    @toggle.setter
    def toggle(self, v): self.__dict__['__toggle'] = v

    @property
    @editor_attribute_decorator("WidgetSpecific",'''Text content''', str, {})
    def text(self): return self.button.get_text()
    @text.setter
    def text(self, value): self.button.set_text(value)

    button = None   # The gui.Button widget instance
    led = None      # The led indicator Widget

    def __init__(self, button_label='siemens button', db_index=-1, byte_index=-1, bit_index=-1, toggle=False, *args, **kwargs):
        self.color_inactive = 'darkgray'
        self.color_active = 'rgb(0,255,0)'
        _style = style_inheritance_text_dict
        _style.update(style_inheritance_dict)
        self.button = gui.Button(button_label, width="100%", height="100%", style=_style)
        self.led = gui.Widget(width=15, height=5, style={'position':'absolute', 'left':'2px', 'top':'2px', 'background-color':self.color_inactive})
        self.led_status = False
        default_style = {'position':'absolute','left':'10px','top':'10px', 'background-color':'rgb(4, 90, 188)', 'color':'white'}
        default_style.update(kwargs.get('style',{}))
        kwargs['style'] = default_style
        kwargs['width'] = kwargs['style'].get('width', kwargs.get('width','100px'))
        kwargs['height'] = kwargs['style'].get('height', kwargs.get('height','100px'))
        super(SiemensButton, self).__init__(*args, **kwargs)
        SiemensWidget._setup(self)
        _style = {'position':'relative'}
        _style.update(style_inheritance_dict)
        self.append(gui.Container(children=[self.button, self.led], width="100%", height="100%", style=_style))
        self.toggle = toggle
        self.button.onmousedown.do(self.set_bit)
        self.button.onmouseup.do(self.reset_bit)

    def set_bit(self, emitter, *args, **kwargs):
        if self.db_index<0 or self.byte_index<0 or self.bit_index<0:
            return
        self.written = False
        value = 1
        if self.toggle:
            value = 0 if self.led_status else 1
        self.plc_instance.set_bool(self.db_index, self.byte_index, self.bit_index, value)

    def reset_bit(self, emitter, x, y, *args, **kwargs):
        if self.db_index<0 or self.byte_index<0 or self.bit_index<0:
            return
        if not self.toggle:
            self.plc_instance.set_bool(self.db_index, self.byte_index, self.bit_index, 0)

    def _set_value(self, value):
        #this function gets called when the camonitor notifies a change on the PV
        self.led_status = value
        self.led.style.update({'background-color':self.color_active if self.led_status else self.color_inactive})

    def update(self, *args):
        #this method gets called by the plc_instance
        if self.plc_instance==None:
            return
        if self.db_index<0 or self.byte_index<0 or self.bit_index<0:
            return
        value = self.plc_instance.get_bool(self.db_index, self.byte_index, self.bit_index)
        self._set_value(value)


class BitStatusWidget(HBox, SiemensWidget, _Mixin_DB_property, _Mixin_Byte_property, _Mixin_Bit_property):
    """A Status indicator widget.
        Connect the event link_to to a PLCSiemens widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEUAAAAdCAIAAABzMjbkAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJrSURBVFhH3ZQxSBtRGMffcpDlpiylEG5xOYTQrUgGN5FMEjIJIhnawVGQuJxwk0OLHUKXgtCCZMgSh3aQFjoIVlBKaCDFQggR4pBMN914vvfu/9XLJTUqr5/gj/9wd3m53/e99+6JJ0jEC0nNB8DDBUnNB8DDBUnNB8DDBUnNB8DDBUnNB8DDBUnNB8DDBUnNB8CTpu27otzEzXTuMGQSks5KIDonwl8Tji2aqZ/+EQBPmkfup7kqnILwd8Rzce9+wovG+rxtyetMbrnWCnWhhC54YsTEkGZZuH47LjlxMzj2l3MZOcay5zeOBvJJ/JdkHbelLaTmnv30agvC3T4Poig49/KWUz1TlSQn/6zqWHkvHrHt/i08OWR6P99e2fZKvR9GYb9RzlrFgyFDP8ODopUtvjv5M5Le0WXvStY9Xmxw1buUP2pa3hw9n92PnojXhz/VK/ESSCeqmZ6H9CNVnfpGYS6bUbvJP1a7YrxYvW0cvd80d+5Hrsv3vdKLZ7Yl99t640LOSfyGZB235SH93Mx+0P20Ylurn9V1oli1gE7lsJtet5n93Kx2ODqVGzW/+5uhH7UpFt50pDfs18f6Wfyg1yr+wE5lz0H362beSvaDIfra9eRJEY5+vV+y437iifgiv5/4w+PpJwpb+yU6vQpb+hRSFb59KZ/p7sJWLT6lMrlyteKKpY/D9JBo+MNTN/ogqyzSYg2Otgp0vpX21cGolP+5H1ZIaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj5PDiGuAaoeNYuSC/YWAAAAAElFTkSuQmCC"

    @property
    @gui.editor_attribute_decorator('WidgetSpecific','The label text', str, {})
    def text(self): return self.label.text
    @text.setter
    def text(self, v): self.label.text = v

    label = None        #a gui.Label widget that shows the fixed label text
    label_value = None  #a gui.Label widget that shows the value as '1' or '0'

    def __init__(self, text='bit status widget', db_index=-1, byte_index=-1, bit_index=-1, *args, **kwargs):
        """
        Args:
            text (str): The text that will be displayed on the label.
            kwargs: See Widget.__init__()
        """
        default_style = {'position':'absolute','left':'10px','top':'10px', 'align-items':'stretch', 'justify-content':'flex-start'}
        default_style.update(kwargs.get('style',{}))
        kwargs['style'] = default_style
        kwargs['width'] = kwargs['style'].get('width', kwargs.get('width','100px'))
        kwargs['height'] = kwargs['style'].get('height', kwargs.get('height','30px'))
        super(BitStatusWidget, self).__init__(*args, **kwargs)
        SiemensWidget._setup(self)
        _style = style_inheritance_text_dict
        _style.update(style_inheritance_dict)
        _style['border']  = '1px solid black'
        self.label = gui.Label(text, width="100%", height="100%", style=_style)
        _style.update({'background-color':'gray', 'text-align':'center'})
        self.label_value = gui.Label("0", width='30px', height="100%", style=_style)
        self.append([self.label, self.label_value])
        self.db_index = db_index
        self.byte_index = byte_index
        self.bit_index = bit_index

    def update(self, *args):
        if self.plc_instance==None:
            return
        if self.db_index<0 or self.byte_index<0 or self.bit_index<0:
            return
        value = self.plc_instance.get_bool(self.db_index, self.byte_index, self.bit_index)
        self.label_value.set_text( '1' if value else '0' )
        style={'border':'1px solid black', 'background-color':'gray'}
        if value:
            style={'border':'1px solid black', 'background-color':'yellow'}
        self.label_value.style.update(style)


class WordEditWidget(SpinBox, SiemensWidget, _Mixin_DB_property, _Mixin_Byte_property):
    """ A Word (16bit) value edit.
        Connect the event link_to to a PLCSiemens widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAeCAIAAADINCUsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGjSURBVGhD7ZYxjoNADEWpt8wl0qbYHIT7pEqdg3CDvQJSirQUXIFy+x3P/MH2jBuKGSGtn1LAt4n4LyBl+HUy7oJxF4y7YNwF4y4Yd8F0dfFlgdkJ+Acu1mXZcFixLcuKQ3YxjQO4Pt7I3o8rsmEYpxjxWgYDMclJoAjRXpM22/F53S+352zo2Obn7XJ/fXCaXFBpKIj9441TD1mUHQHzKpHWIdpraN6W2LnUYYTVOyIaCqSYhNyjYz0NGCHaazBrS9HctFO5sFXULmRgXmOFaK/BrDl7f1tEQLigu99fbUWcyFgXpbNxIjvieitEew0tdyJaCFgiAuY7onrHR0AnWkW6JG/QNs2sEO01caEPR10U70MtIhBC+fhrNTizwm/UV2CjOYfeESBK5N+4QMkilBu6nqZGiPYabLSl6G/riC7kb7j3p7B6IohcViDs8GEdor0mLjTFbG6E+bmguwXp/qMKhbSFjoL9C/hhqEK016TNdhz8r9ULtNdg1o7D/8G7gPYazE6Au2C6ujg57oJxF4y7YNwF4y4Yd8EMP/PqH/rM6x+8Pwvc9mLA2gAAAABJRU5ErkJggg=="
    def __init__(self, db_index=-1, byte_index=-1, *args, **kwargs):
        """
        Args:
            kwargs: See Widget.__init__()
        """
        default_style = {'position':'absolute','left':'10px','top':'10px'}
        default_style.update(kwargs.get('style',{}))
        kwargs['style'] = default_style
        kwargs['width'] = kwargs['style'].get('width', kwargs.get('width','100px'))
        kwargs['height'] = kwargs['style'].get('height', kwargs.get('height','30px'))
        super(WordEditWidget, self).__init__(0, -32767, 32766, 1,*args, **kwargs)
        SiemensWidget._setup(self)
        self.db_index = db_index
        self.byte_index = byte_index
        self.onchange.do(self.on_changed)

    def on_changed(self, emitter, new_value):
        if self.plc_instance==None:
            return
        if self.db_index<0 or self.byte_index<0:
            return
        self.plc_instance.set_int( self.db_index, self.byte_index, int(self.get_value()))


class ByteViewWidget(Label, SiemensWidget, _Mixin_DB_property, _Mixin_Byte_property):
    """ A Byte (8bit) value view.
        Connect the event link_to to a PLCSiemens widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    #icon = default_icon("ByteViewWidget")

    @property
    def text(self): return self.get_text()
    @text.setter
    def text(self, value): self.set_text(value)

    def __init__(self, db_index=-1, byte_index=-1, *args, **kwargs):
        """
        Args:
            kwargs: See Widget.__init__()
        """
        default_style = {'position':'absolute','left':'10px','top':'10px'}
        default_style.update(kwargs.get('style',{}))
        kwargs['style'] = default_style
        kwargs['width'] = kwargs['style'].get('width', kwargs.get('width','100px'))
        kwargs['height'] = kwargs['style'].get('height', kwargs.get('height','30px'))
        super(ByteViewWidget, self).__init__(*args, **kwargs)
        SiemensWidget._setup(self)
        self.db_index = db_index
        self.byte_index = byte_index

    def update(self, *args):
        if self.plc_instance==None:
            return
        if self.db_index<0 or self.byte_index<0:
            return
        value = self.plc_instance.get_byte(self.db_index, self.byte_index)
        self.set_text( bin(value[0]) )
