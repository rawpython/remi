# -*- coding: utf-8 -*-

import remi.gui
from remi.gui import *
import snap7


# https://python-snap7.readthedocs.io/en/latest/util.html
# https://github.com/gijzelaerr/python-snap7/blob/master/example/boolean.py

class PLCSiemens(Image):
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAvCAYAAAAIA1FgAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAADmwAAA5sBPN8HMQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANGSURBVFiF7ZbNbxtFGIefmR2vP+PUjkntxHGapmmpKpIoECggjpyQEBKqeoIjXDhw5cD/wZ0LEgiJEzck1EIrlUYBl7RJ1bQlbUpCHNux15+7MxycWnLzoX6sJZDyk1bzzsc+s/q9s7uv+PTzL40dCBCLRShsl/A8j1K5AoARnet5JAyoWDSC1hpjIDuS5sH6390Fi+9WyL49zungCPdam+TsFAMyjKObLNRXmbTTTIdyXKrdIiJsitohq4YoeBUWf19C3fvr4b47G2MAmLTTnLLTDMgQuUCKpeYDzgZHOR+eYt0tMmmn+cm5wRfDF/mm/AspK85qe4NFQBKuQ7gOyu2BFzYfAeChSVhRbKGomxbbXpU7rQ1iMoRGs+mWcY3mu52rvBaepKirnLYzHWsu3MAAmF/nMZfe6MK3NtZpvpOkOOYSt6N4xiNk2QQtm1KzihAgkcSDEZx2g4bXRglJW7sIIVGPXNRhSRldCTG68rinAA00SPbc1iABQGC3b+22AZT+/r1dH44dts9zSXF7wndoFy4++BEAs3wKbk75DD9zpxMVkp3M+gk3q7lOtN0Hz8237/sO7cLFiTUATGkQSnGf4Rd/6ERPvER+SPpKe0LKfPUxAKYR7AO87K/PPXD5ydcAmIVpzG8z/sJJlDtRuOErGECZq3OdaG2kZ0JaL55rZX5+a9+JZCr9wvC+HsX+nvP7q7do1mv+gwM2avzky76DH6u/tuw3eH5+FsepUW80GRtNc/nKdeZmzlGuVKlWHWZfOcv9tYfUG01i0QiBgOLaQv7p4JZloZRiKBkmffwl5mbOIaXg5IksrVabfwrb5JdWeHN+FtfTLOZv7vvke2yxLInahTtOjT/+XCYSCaGNYfXuGuWdCrVaHYBK1UFKweuvTiPE3qJSfPjRZ37/Ors6sCjKZTMMxgeoVB3GshkuX7nOYHyA1FCCUnmHWDRKq9VCStlTvD4VfDRzHBVQ5JdWyKSHMcbgeR5npibYKhS764QQzw53PY/EsUFGMsNsbG4xMZ4lFArSarURQhAOh2i32wgOLuAPhF9byKOUhet6PePLt++itUZK2S2znxkO7AEDaK172sP0//0qHsGP4Efw/zL8X7xWNIa0/NaYAAAAAElFTkSuQmCC"
    @decorate_constructor_parameter_types([str, int, int])
    def __init__(self, ip_address, rack=0, slot=3, poll_connection_state=True, *args, **kwargs):
        super(PLCSiemens, self).__init__(self.icon, *args, **kwargs)
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'23px','height':'47px'})
        self.snap7_client = snap7.client.Client()
        self._set_params()
        self.ip_address = ip_address
        self.snap7_client.connect(self.ip_address, rack, slot)
        self.poll_connection_state = poll_connection_state
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
        self.attributes['title'] =  self.get_cpu_info()
        return ()

    @decorate_event
    def on_disconnected(self):
        self.attributes['title'] = "%s : not connected"%self.ip_address
        return ()

    def __del__(self):
        self.poll_connection_state = False
        self.snap7_client.destroy()

    def check_connection_state(self):
        _con = self.snap7_client.get_connected()
        if _con != self.connected:
            if _con:
                self.on_connected()
            else:
                self.on_disconnected()
        self.connected = _con

        if self.poll_connection_state:
            Timer(1, self.check_connection_state).start()

    def set_bool(self, db_area_mem, byte_index, bit_index, value):
        bytes_to_read_write = 1
        mem = self.snap7_client.db_read(db_area_mem, byte_index, bytes_to_read_write)
        snap7.util.set_bool(mem, value_to_write, bit_index)
        self.snap7_client.db_write(mem, db_area_mem, byte_index, bytes_to_read_write)

    def get_bool(self, db_area_mem, byte_index, bit_index):
        bytes_to_read_write = 1
        mem = self.snap7_client.db_read(db_area_mem, byte_index, bytes_to_read_write)
        return snap7.util.get_bool(mem, byte_index, bit_index)

    def set_int(self, db_area_mem, byte_index, value):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 2)
        snap7.util.set_int(mem, 0, value)
        self.snap7_client.db_write(mem, db_area_mem, byte_index, 2)

    def get_int(self, db_area_mem, byte_index):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 2) #an int from 2 bytes
        return snap7.util.get_int(mem, 0) #0 or byte_index?

    def set_real(self, db_area_mem, byte_index, value):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 4)
        snap7.util.set_real(mem, 0, value)
        self.snap7_client.db_write(mem, db_area_mem, byte_index, 4)

    def get_real(self, db_area_mem, byte_index):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, 4) #a real from 4 bytes
        return snap7.util.get_real(mem, 0) #0 or byte_index?

    def set_string(self, db_area_mem, byte_index, max_size, value):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, max_size)
        snap7.util.set_real(mem, 0, value, max_size)
        self.snap7_client.db_write(mem, db_area_mem, byte_index, max_size)

    def get_string(self, db_area_mem, byte_index, max_size):
        mem = self.snap7_client.db_read(db_area_mem, byte_index, max_size)
        return snap7.util.get_string(mem, 0, max_size) #0 or byte_index?

    def on_link_to(self, widget):
        """ Each widget registers itself to the PLC class by linking its "link_to" event 
            toward the "on_link_to" listener
        """
        widget.set_plc_instance(self)


class ButtonSetResetBit(Button):
    """A Button widget that sets the bit when clicked.
    """
    @decorate_constructor_parameter_types([str, int, int, int])
    def __init__(self, text, db_area_mem, byte_index, bit_index, *args, **kwargs):
        """
        Args:
            text (str): The text that will be displayed on the button.
            kwargs: See Widget.__init__()
        """
        super(ButtonSetResetBit, self).__init__(*args, **kwargs)
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'100px','height':'30px'})
        self.type = 'button'
        self.set_text(text)
        self.plc_instance = None
        self.db_area_mem = db_area_mem
        self.byte_index = byte_index
        self.bit_index = bit_index

    @decorate_set_on_listener("(self, emitter)")
    @decorate_event
    def link_to(self):
        return ()

    def set_plc_instance(self, plc_instance):
        self.plc_instance = plc_instance

    @decorate_set_on_listener("(self,emitter)")
    @decorate_event_js("sendCallback('%(emitter_identifier)s','%(event_name)s');" \
                       "event.stopPropagation();event.preventDefault();")
    @decorate_event
    def onclick(self):
        if not self.plc_instance == None:
            self.plc_instance.set_bool(self.db_area_mem, self.byte_index, self.bit_index, value)
        Button.onclick(self)

        