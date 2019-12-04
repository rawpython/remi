# -*- coding: utf-8 -*-

import remi.gui as gui
from remi.gui import *
import snap7
from threading import Timer
import traceback

# https://python-snap7.readthedocs.io/en/latest/util.html
# https://github.com/gijzelaerr/python-snap7/blob/master/example/boolean.py

class PLCSiemens(Image):
    """ This is a snap7 interface that allows to communicate with Siemens PLC.
        It handles the connection and reconnection.
        Widgets' event "link_to" have to be connected to this widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAvCAYAAAAIA1FgAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAADmwAAA5sBPN8HMQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANGSURBVFiF7ZbNbxtFGIefmR2vP+PUjkntxHGapmmpKpIoECggjpyQEBKqeoIjXDhw5cD/wZ0LEgiJEzck1EIrlUYBl7RJ1bQlbUpCHNux15+7MxycWnLzoX6sJZDyk1bzzsc+s/q9s7uv+PTzL40dCBCLRShsl/A8j1K5AoARnet5JAyoWDSC1hpjIDuS5sH6390Fi+9WyL49zungCPdam+TsFAMyjKObLNRXmbTTTIdyXKrdIiJsitohq4YoeBUWf19C3fvr4b47G2MAmLTTnLLTDMgQuUCKpeYDzgZHOR+eYt0tMmmn+cm5wRfDF/mm/AspK85qe4NFQBKuQ7gOyu2BFzYfAeChSVhRbKGomxbbXpU7rQ1iMoRGs+mWcY3mu52rvBaepKirnLYzHWsu3MAAmF/nMZfe6MK3NtZpvpOkOOYSt6N4xiNk2QQtm1KzihAgkcSDEZx2g4bXRglJW7sIIVGPXNRhSRldCTG68rinAA00SPbc1iABQGC3b+22AZT+/r1dH44dts9zSXF7wndoFy4++BEAs3wKbk75DD9zpxMVkp3M+gk3q7lOtN0Hz8237/sO7cLFiTUATGkQSnGf4Rd/6ERPvER+SPpKe0LKfPUxAKYR7AO87K/PPXD5ydcAmIVpzG8z/sJJlDtRuOErGECZq3OdaG2kZ0JaL55rZX5+a9+JZCr9wvC+HsX+nvP7q7do1mv+gwM2avzky76DH6u/tuw3eH5+FsepUW80GRtNc/nKdeZmzlGuVKlWHWZfOcv9tYfUG01i0QiBgOLaQv7p4JZloZRiKBkmffwl5mbOIaXg5IksrVabfwrb5JdWeHN+FtfTLOZv7vvke2yxLInahTtOjT/+XCYSCaGNYfXuGuWdCrVaHYBK1UFKweuvTiPE3qJSfPjRZ37/Ors6sCjKZTMMxgeoVB3GshkuX7nOYHyA1FCCUnmHWDRKq9VCStlTvD4VfDRzHBVQ5JdWyKSHMcbgeR5npibYKhS764QQzw53PY/EsUFGMsNsbG4xMZ4lFArSarURQhAOh2i32wgOLuAPhF9byKOUhet6PePLt++itUZK2S2znxkO7AEDaK172sP0//0qHsGP4Efw/zL8X7xWNIa0/NaYAAAAAElFTkSuQmCC"
    @decorate_constructor_parameter_types([str, int, int])
    def __init__(self, ip_address, rack=0, slot=3, update_interval_millisec=1.0, *args, **kwargs):
        if not 'width' in kwargs:
            kwargs['width'] = 23
        if not 'height' in kwargs:
            kwargs['height'] = 47
        super(PLCSiemens, self).__init__(self.icon, *args, **kwargs)
        self.linked_widgets = []
        self.style.update({'position':'absolute','left':'10px','top':'10px'})
        self.snap7_client = snap7.client.Client()
        self._set_params()
        self.ip_address = ip_address
        self.snap7_client.connect(self.ip_address, rack, slot)
        self.update_interval_millisec = update_interval_millisec
        self.connected = False
        self.on_disconnected()
        self.check_connection_state()
        
    def _set_params(self):
        values = (
                (snap7.snap7types.PingTimeout, 1000),
                (snap7.snap7types.SendTimeout, 500),
                (snap7.snap7types.RecvTimeout, 3500),
                (snap7.snap7types.SrcRef, 128),
                (snap7.snap7types.DstRef, 128),
                (snap7.snap7types.SrcTSap, 128),
                (snap7.snap7types.PDURequest, 470),
            )
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
        self.update_interval_millisec = 0
        self.snap7_client.destroy()

    def check_connection_state(self):
        _con = self.snap7_client.get_connected()
        if _con != self.connected:
            if _con:
                self.on_connected()
            else:
                self.on_disconnected()
        self.connected = _con
        for w in self.linked_widgets:
            if hasattr(w, "update"):
                try:
                    w.update()
                except:
                    print(traceback.format_exc())
        if self.update_interval_millisec>0.0:
            Timer(1, self.check_connection_state).start()

    def set_bool(self, db_area_mem, byte_index, bit_index, value):
        reading = self.snap7_client.db_read(db_area_mem, byte_index, 1)    # read 1 byte from db 31 staring from byte 120
        snap7.util.set_bool(reading, 0, bit_index, value)   # set a value of fifth bit
        self.snap7_client.db_write(db_area_mem, byte_index, reading)    # write back the bytearray and now the boolean value is changed 

    def get_bool(self, db_area_mem, byte_index, bit_index):
        bytes_to_read_write = 1
        mem = self.snap7_client.db_read(db_area_mem, byte_index, bytes_to_read_write)
        return snap7.util.get_bool(mem, byte_index, bit_index)

    def set_int(self, db_area_mem, byte_index, value):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 2)
        snap7.util.set_int(mem, 0, value)
        self.snap7_client.db_write(db_area_mem, byte_index, mem)

    def get_int(self, db_area_mem, byte_index):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 2) #an int from 2 bytes
        return snap7.util.get_int(mem, 0) #0 or byte_index?

    def set_real(self, db_area_mem, byte_index, value):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 4)
        snap7.util.set_real(mem, 0, value)
        self.snap7_client.db_write(db_area_mem, byte_index, mem)

    def get_real(self, db_area_mem, byte_index):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 4) #a real from 4 bytes
        return snap7.util.get_real(mem, 0) #0 or byte_index?

    def set_string(self, db_area_mem, byte_index, max_size, value):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, max_size)
        snap7.util.set_string(mem, 0, value, max_size)
        self.snap7_client.db_write(db_area_mem, byte_index, mem)

    def get_string(self, db_area_mem, byte_index, max_size):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, max_size)
        return snap7.util.get_string(mem, 0, max_size) #0 or byte_index?

    def on_link_to(self, widget):
        """ Each widget registers itself to the PLC class by linking its "link_to" event 
            toward the "on_link_to" listener
        """
        widget.set_plc_instance(self)
        #the widget is appended to a link for cyclical update purpose
        self.linked_widgets.append(widget)


# noinspection PyUnresolvedReferences
class SiemensWidget(object):
    def _setup(self):
        #this must be called after the Widget super constructor
        self.link_to.do = self.do

    def do(self, callback, *userdata):
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


class ButtonSetResetBit(Button, SiemensWidget):
    """ A Button widget that sets the bit when clicked.
        Connect the event link_to to a PLCSiemens widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAuCAYAAABXuSs3AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAUFSURBVGiB7ZlbbBRVGIC/2Z3Z7Q7tsqXd0ptCWWhKA4Y0kRSCFRKIiKQPiClRYloSSDQgiQQSIMiDgooSuSiICdZoAiiND5hwEWJ9EJGAsdCIXLpAudiWxe62trPs7Fx8WHZqaSli2S1N+iWTnTnnP+d858x/TrIZQdM00zRNervWtO5jS+gQjyNiXPKwX+WT3wwuhgSrsnWMCfmx+5WZ5azMKEdDZ3nTF+xvP8GvvvdZeGMba73zmOIqtNqtaP6SyfJYKtxTea5xA01akDrfB5xQLrI+8A3HRq2zYsOmyoSGFVwct5U3mqo53FHH5uxXOR32c6ijjr35yymTx3PmTiMvXt9MkxbsEldVlXdP6jQrtl5nl2pL4Z2sBTzfuJEpciFbcyrZ336C0ZIXhyCSI6ZT0/4LRzvOAvB75AZz0kp4QspkilzIVTXAKMnLVSmAhJ08aQRzG98DQMcAYIw0krezKjjScQav3Y3bJlPhnkqqLYVnrrzF9pxFLMuYzZqWvd3FmxXpvq9FNTVUU6PSM52PWw+zo/VIn6+xzVAAqI9co9Q1jmzRQ33kWu+xumLdFziymJtWYj3/bYQpcuYxM/UpKm5sIah3WHU20zTRNK1PEdXUqLj+ESWuAk6O2ciW7MoeMVWeGezKXcKu3CVkix4ATof9lMqFTHaN5VS4wYp1CKIV+2bmXKv8w9vfsd77EgKxdN3XdpzqYC1rvfO4NG4bZXLxw4nnSSMYbpeZ0LCCsivrWegpI0sc3i1mZctX+C4tw3dpGZfVFgDOR25SIGUxTS7iVNhvxd4xolbswhvbrfLdoR/IEoczM3UiAM8OK+br9p/JvrCYz1qPsTRjthUrmqaJrut9ijsEkeq819FMA0mwo5sGqtl9ssXOfGYOiw3YoDYDYGBSH7nGaMnLLa2ta7UEwYoF+FE5B0DEiLIh8C2f5i4GoEwu5oW0EpY3V5MppqEYkS5xAMMw+hS/ot5idcsetuVUETV1ljbtJqR3cjUaQDU1mrQg892lzHeXArDp9gFu6+206QrHOs6SJ42g04jQFA0SRedmtJVduUus/if5V3E52oKBSXWolqr06bQbCvtaj/O0y8fBJ1dzQf2Typs7rDZCZ2enGQgEmHEwo4dwsKCGtvzv+5xUshEFE0EQ+hZ/HKmd8xder5feD+5BwJB4shkSTzaDVlzsX3MnR1+T8PUoN6jZqbAKqCofxro8oWfTu/jPdzCr9uFH7qd474NvWpDK/EUu/vg8TPWBTqrjFRNd1E2zce6nTl6u79+YCUmVVS0GOAXGJ6LzuyREfNNIG/7zsVRJFI8kVXxFqVwu6l7WrkhA9FF03ysJyfHYhnSwZ2K037l8PxKSKtUHNPwIeDMT0XuMQXuOJ0S8qlzEF9HZ8z/O5/9KgjanQc3OcNf5nQD6KR5h1s7Ig8Pi1IeZ9Ig261COJ5sh8WQzJJ5shsSTzZB4srEJgoAg3P/P7ONG3NcWfxgsxF0H74oLgoDdbidTUgfa6YE86bqD3W7vEhdFkcVjg+Q7lQe3HiAyxAivjG5DFMXYqquqaiqKQigUIhgMoigKkUjE+roMWL/JIp668bRwOp3Iskx6ejoejwdZlhHjFW63G4fDgaqqqKraTXygiIs7HA4cDgcpKSk4nc5YuaZppmEY6Lre7Yp/0Booeev0sNmw2+3dLpvNhqDrunlvWgxUitzLvSnz7/t/AIHaIUqnNr0FAAAAAElFTkSuQmCC"
    @decorate_constructor_parameter_types([str, int, int, int, bool])
    def __init__(self, text, db_area_mem, byte_index, bit_index, toggle=False, *args, **kwargs):
        """
        Args:
            text (str): The text that will be displayed on the button.
            kwargs: See Widget.__init__()
        """
        #SiemensWidget.__init__(self)
        super(ButtonSetResetBit, self).__init__(text, *args, **kwargs)
        SiemensWidget._setup(self)

        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'100px','height':'30px'})
        self.toggle = toggle
        self.plc_instance = None
        self.db_area_mem = db_area_mem
        self.byte_index = byte_index
        self.bit_index = bit_index
        self.onmousedown.do(self.set_bit, value = 1)

        self.value = 0
        if not self.toggle:
            self.onmouseup.do(self.set_bit, value = 0)

    def set_bit(self, emitter, *args, **kwargs):
        if self.plc_instance==None:
            return
        self.value = kwargs.get('value', self.value)
        if self.toggle:
            self.value = not self.plc_instance.get_bool(self.db_area_mem, self.byte_index, self.bit_index)
        self.plc_instance.set_bool(self.db_area_mem, self.byte_index, self.bit_index, self.value)


class BitStatusWidget(HBox, SiemensWidget):
    """A Status indicator widget.
        Connect the event link_to to a PLCSiemens widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEUAAAAdCAIAAABzMjbkAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJrSURBVFhH3ZQxSBtRGMffcpDlpiylEG5xOYTQrUgGN5FMEjIJIhnawVGQuJxwk0OLHUKXgtCCZMgSh3aQFjoIVlBKaCDFQggR4pBMN914vvfu/9XLJTUqr5/gj/9wd3m53/e99+6JJ0jEC0nNB8DDBUnNB8DDBUnNB8DDBUnNB8DDBUnNB8DDBUnNB8DDBUnNB8CTpu27otzEzXTuMGQSks5KIDonwl8Tji2aqZ/+EQBPmkfup7kqnILwd8Rzce9+wovG+rxtyetMbrnWCnWhhC54YsTEkGZZuH47LjlxMzj2l3MZOcay5zeOBvJJ/JdkHbelLaTmnv30agvC3T4Poig49/KWUz1TlSQn/6zqWHkvHrHt/i08OWR6P99e2fZKvR9GYb9RzlrFgyFDP8ODopUtvjv5M5Le0WXvStY9Xmxw1buUP2pa3hw9n92PnojXhz/VK/ESSCeqmZ6H9CNVnfpGYS6bUbvJP1a7YrxYvW0cvd80d+5Hrsv3vdKLZ7Yl99t640LOSfyGZB235SH93Mx+0P20Ylurn9V1oli1gE7lsJtet5n93Kx2ODqVGzW/+5uhH7UpFt50pDfs18f6Wfyg1yr+wE5lz0H362beSvaDIfra9eRJEY5+vV+y437iifgiv5/4w+PpJwpb+yU6vQpb+hRSFb59KZ/p7sJWLT6lMrlyteKKpY/D9JBo+MNTN/ogqyzSYg2Otgp0vpX21cGolP+5H1ZIaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj4AHi5Iaj5PDiGuAaoeNYuSC/YWAAAAAElFTkSuQmCC"
    @decorate_constructor_parameter_types([str, int, int, int])
    def __init__(self, text, db_area_mem, byte_index, bit_index, *args, **kwargs):
        """
        Args:
            text (str): The text that will be displayed on the label.
            kwargs: See Widget.__init__()
        """
        #SiemensWidget.__init__(self)
        if not 'width' in kwargs:
            kwargs['width'] = 100
        if not 'height' in kwargs:
            kwargs['height'] = 30
        super(BitStatusWidget, self).__init__(*args, **kwargs)
        SiemensWidget._setup(self)
        self.style.update({'align-items':'stretch', 'justify-content':'flex-start'})
        self.label = gui.Label(text, style={'border':'1px solid black'})
        self.label_value = gui.Label("0", width='30px', style={'border':'1px solid black', 'background-color':'gray', 'text-align':'center'})
        self.append([self.label, self.label_value])
        self.style.update({'position':'absolute','left':'10px','top':'10px'})
        self.plc_instance = None
        self.db_area_mem = db_area_mem
        self.byte_index = byte_index
        self.bit_index = bit_index

    def update(self, *args):
        if self.plc_instance==None:
            return
        value = self.plc_instance.get_bool(self.db_area_mem, self.byte_index, self.bit_index)
        self.label_value.set_text( '1' if value else '0' )
        style={'border':'1px solid black', 'background-color':'gray'}
        if value:
            style={'border':'1px solid black', 'background-color':'yellow'}
        self.label_value.style.update(style)

        
class WordEditWidget(SpinBox, SiemensWidget):
    """ A Word (16bit) value edit.
        Connect the event link_to to a PLCSiemens widget on the "on_link_to" method.
        i.e.:
            widget.link_to.do(plc.on_link_to)
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAeCAIAAADINCUsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGjSURBVGhD7ZYxjoNADEWpt8wl0qbYHIT7pEqdg3CDvQJSirQUXIFy+x3P/MH2jBuKGSGtn1LAt4n4LyBl+HUy7oJxF4y7YNwF4y4Yd8F0dfFlgdkJ+Acu1mXZcFixLcuKQ3YxjQO4Pt7I3o8rsmEYpxjxWgYDMclJoAjRXpM22/F53S+352zo2Obn7XJ/fXCaXFBpKIj9441TD1mUHQHzKpHWIdpraN6W2LnUYYTVOyIaCqSYhNyjYz0NGCHaazBrS9HctFO5sFXULmRgXmOFaK/BrDl7f1tEQLigu99fbUWcyFgXpbNxIjvieitEew0tdyJaCFgiAuY7onrHR0AnWkW6JG/QNs2sEO01caEPR10U70MtIhBC+fhrNTizwm/UV2CjOYfeESBK5N+4QMkilBu6nqZGiPYabLSl6G/riC7kb7j3p7B6IohcViDs8GEdor0mLjTFbG6E+bmguwXp/qMKhbSFjoL9C/hhqEK016TNdhz8r9ULtNdg1o7D/8G7gPYazE6Au2C6ujg57oJxF4y7YNwF4y4Yd8EMP/PqH/rM6x+8Pwvc9mLA2gAAAABJRU5ErkJggg=="
    @decorate_constructor_parameter_types([str, int, int])
    def __init__(self, text, db_area_mem, byte_index, *args, **kwargs):
        """
        Args:
            text (str): The text that will be displayed on the label.
            kwargs: See Widget.__init__()
        """
        if not 'width' in kwargs:
            kwargs['width'] = 100
        if not 'height' in kwargs:
            kwargs['height'] = 30
        super(WordEditWidget, self).__init__(0, -32767, 32766, 1,*args, **kwargs)
        SiemensWidget._setup(self)
        self.style.update({'position':'absolute','left':'10px','top':'10px'})
        self.plc_instance = None
        self.db_area_mem = db_area_mem
        self.byte_index = byte_index
        self.onchange.do(self.on_changed)

    def on_changed(self, emitter, new_value):
        if self.plc_instance==None:
            return
        self.plc_instance.set_int( self.db_area_mem, self.byte_index, int(self.get_value()))

