# -*- coding: utf-8 -*-

import remi.gui as gui
from remi.gui import *
from threading import Timer
import traceback
import time

import epics
#from epics import caget, caput, cainfo


# noinspection PyUnresolvedReferences
class EPICSWidget(object):
    epics_pv = None #here will be stored the PV instance

    def __del__(self):
        self.epics_pv.clear_auto_monitor()
        self.epics_pv.disconnect()

    @decorate_set_on_listener("(self, emitter, pvname=None, conn=None, chid=None, **kwargs)")
    @decorate_event
    def onConnectionChange(self, pvname=None, conn=None, chid=None, **kwargs):
        #print('ca connection status changed:  ', pvname,  conn, chid)
        #Here I use the outline red color to show the unconnected state
        # of course this can be avoided or changed
        self.style['outline'] = "1px solid red"
        if conn:
            del self.style['outline']
        return (pvname, conn, chid, kwargs)

    @decorate_set_on_listener("(self, emitter, pvname=None, value=None, **kwargs)")
    @decorate_event
    def onChanges(self, pvname=None, value=None, **kwargs):
        #as default I write the value to the widget itself
        self.set_value(str(value))
        return (pvname, value, kwargs)


class EPICSBooleanButton(gui.Widget, EPICSWidget):
    """ A Button widget that sets the bit when clicked.
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAuCAYAAABXuSs3AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAKMSURBVGiB7ZqxaxNRGMB/9+7uXZK2aaMVEUWEKNSh4CQIrhWnujiIQqGig7gXF/+B7tLNbp2KQyfBwcVdsdhWJa5WHZKKvZqXe3cO57VNmraJyd0ZuB88LnkvfO/H43sfB18Mz/OCIAhoN4DdZ9IYhrH7bDesSPJlRfHsrc+nmpGK6HGcGQp4clVwsywBMJRSgVKKqWXNpitS1juaS6M+L26ZSCnDE1dKsenaAHy/MUNjtNJ10JG1WYofHvTbtYnPWwKlFLZth+Ke5wGheKP0EXVireugemizz5rt8TyPIAgQe+KDQZO41jptn47RWofiAL7vp+3TMZGrtb9mAxTfP0bnf3QdMPf1Wt/kjiLytVoXRtZnEhHolf+7cB9BJp40mXjSDKz4gXLYHQ6vHtmUD8z7LC+4zAGz00M8PXv4q3Jl4xdTr7vfuUfx9pvP3xnm9v086893WFzZZjFamMzz7rpg7c02d1d72zOWVJn75oNjcDmO4H+JRXz+tKCyEaZKXPQlVcoTw3yZaJ776dpAox/h2xJLjocXUrI02eg5lw8jllRZXPGoYHBqPI7oIQNbx2MRn522KNc1S/9Qnzslpsvps7yws1e/Y6BH8TpTC/XOf766w5U+XdYsx5MmE0+aTDxpMvGkycSTRkTNoEEh8hXRl0Ehch3cEzcMA9M0GbdV2k7Hcj7/G9M098Qty+LhxSrnHDdtt0M5adW5d2ELy7LCU1dKBa7rUqvVqFaruK5LvV5Ptbvc2lV2HIdCoUCpVGJsbIxCoYAVLRSLRaSUKKVQStHaYkmDSFxKiZSSXC6H4zjhvOd5ge/7aK2bRtQkSruXL4TANM2mIYTA0FoHrWmR9h8QIlpTZv/nP6KyI2uh/zMtAAAAAElFTkSuQmCC"
    @decorate_constructor_parameter_types([str, str, bool])
    def __init__(self, button_label, epics_pv_name, toggle=False, *args, **kwargs):
        self.color_inactive = 'darkgray'
        self.color_active = 'rgb(0,255,0)'
        self.button = gui.Button(button_label)
        self.led = gui.Widget(width=15, height=5, style={'position':'absolute', 'left':'2px', 'top':'2px', 'background-color':self.color_inactive})
        self.led_status = False
        super(EPICSBooleanButton, self).__init__(*args, **kwargs)
        self.append([self.button, self.led])
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'100px','height':'30px'})
        self.toggle = toggle
        self.epics_pv = epics.PV(epics_pv_name, auto_monitor=True, callback=self.onChanges, connection_callback=self.onConnectionChange, connection_timeout=2)
        self.button.onmousedown.do(self.set_bit)
        if not self.toggle:
            self.button.onmouseup.do(self.reset_bit)

    #this method gets called when a change occurs on style or attributes dictionaries of the widget
    def _need_update(self, emitter=None):
        width = gui.from_pix(self.style.get('width', "100").replace("%",""))
        height = gui.from_pix(self.style.get('height', "100").replace("%",""))
        self.button.set_size(width, height)
        gui.Widget._need_update(self, emitter)

    def set_bit(self, emitter, *args, **kwargs):
        self.pressed = True
        self.written = False
        value = 1
        if self.toggle:
            value = 0 if self.led_status else 1
        self.epics_pv.put(value, callback = (self.put_done if not self.toggle else None) )

    def put_done(self, *args, **kwargs):
        self.written = True
        #this function gets called when a set_bit is completed and the button is not toggle
        # and so the value have to be reset
        if not self.pressed:
            self.epics_pv.put(0)

    def reset_bit(self, emitter, x, y, *args, **kwargs):
        self.pressed = False
        if self.written:
            self.epics_pv.put(0)

    def set_value(self, value):
        #this function gets called when the camonitor notifies a change on the PV
        self.led_status = float(value)>0.0
        self.led.style.update({'background-color':self.color_active if self.led_status else self.color_inactive})


class EPICSLed(HBox, EPICSWidget):
    """A Status indicator widget.
    """
    icon = "data:image/png;base64,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"
    @decorate_constructor_parameter_types([str, str])
    def __init__(self, epics_pv_name, *args, **kwargs):
        self.color_inactive = 'darkgray'
        self.color_active = 'rgb(0,180,0)'
        super(EPICSLed, self).__init__(*args, **kwargs)
        self.style.update({'align-items':'center', 'justify-content':'center'})
        self.label_value = gui.Label("0", style={'text-align':'center', 'color':'white'})
        self.append(self.label_value)
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'50px','height':'50px', 'background-color':self.color_inactive})
        self.epics_pv = epics.PV(epics_pv_name, auto_monitor=True, callback=self.onChanges, connection_callback=self.onConnectionChange, connection_timeout=2)

    #this method gets called when a change occurs on style or attributes dictionaries of the widget
    def _need_update(self, emitter=None):
        width = gui.from_pix(self.style.get('width', "100").replace("%",""))
        height = gui.from_pix(self.style.get('height', "100").replace("%",""))
        radius = min(width, height)/2
        self.style['border-radius'] = gui.to_pix(radius)
        gui.HBox._need_update(self, emitter)

    def set_value(self, value):
        _value = float(value)
        self.label_value.set_text( '1' if _value>0.0 else '0' )
        self.style.update({'background-color':self.color_active if _value>0.0 else self.color_inactive})

        
class EPICSValueMeterWidget(Progress, EPICSWidget):
    """A simple progress bar indicating a value.
    """
    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAApCAYAAACoYAD2AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAlwSFlzAAAOwgAADsIBFShKgAAAAG1JREFUWEft1qENgEAMQNEec6AwDMG4jIbC3QZAQuXhvijJf6aVP+mJa9cjiptylmYkxUiKkRQjKUZSjKQYSTGSMvyZt/3M7dux9dx487Lm9vLclP++yWo8N8VIipEUIylGUoykGEkxkmIkI+IGyZcQRHB9PC8AAAAASUVORK5CYII="
    @decorate_constructor_parameter_types([str, int])
    def __init__(self, epics_pv_name, max_value, *args, **kwargs):
        super(EPICSValueMeterWidget, self).__init__(0, max_value,*args, **kwargs)
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'100px','height':'30px'})
        self.epics_pv = epics.PV(epics_pv_name, auto_monitor=True, callback=self.onChanges, connection_callback=self.onConnectionChange, connection_timeout=2)

    def set_value(self, value):
        Progress.set_value(self, value)


try:
    import pygal
except:
    print("It is required to install pygal to use EPICSPlotPV widget")

class EPICSPlotPV(gui.Svg, EPICSWidget):
    """A simple plot bar indicating a value.
        REQUIRES library pygal to be installed
    """
    icon = "data:image/png;base64,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"
    @decorate_constructor_parameter_types([str, int])
    def __init__(self, epics_pv_name, max_values_count, *args, **kwargs):
        super(EPICSPlotPV, self).__init__(100, 100, *args, **kwargs)
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'100px','height':'30px', 'overflow':'hidden', 'background-color':'lightgray'})
        self.style['margin'] = '10px'
        self.values = gui.SvgPolyline(max_values_count)
        self.pv_name = epics_pv_name
        self.epics_pv = epics.PV(epics_pv_name, auto_monitor=True, callback=self.onChanges, connection_callback=self.onConnectionChange, connection_timeout=2)

    def set_size(self, width, height):
        gui.Svg.set_size(self, width, height)
        self.attributes['width'] = width
        self.attributes['height'] = height

    #this method gets called when a change occurs on style or attributes dictionaries of the widget
    def _need_update(self, emitter=None):
        width = gui.from_pix(self.style.get('width', "100").replace("%",""))
        height = gui.from_pix(self.style.get('height', "100").replace("%",""))
        self.set_size(width, height)
        gui.Svg._need_update(self, emitter)

    def set_value(self, value):
        self.values.add_coord(time.clock(), float(value))
        try:
            plot = pygal.XY()
            pairs = []
            for i in range(0, len(self.values.coordsX)):
                pairs.append([self.values.coordsX[i], self.values.coordsY[i]])
            plot.add(self.pv_name, pairs)
            self.add_child("chart", plot.render())
        except:
            self.style['overflow'] = "visible"
            self.add_child("chart", gui.SvgText(10,10, "Install pygal to use this widget"))
