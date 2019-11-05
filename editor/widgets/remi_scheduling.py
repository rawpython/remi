# -*- coding: utf-8 -*-

import remi.gui
from remi.gui import *
import remi.gui as gui
from threading import Timer


# https://python-snap7.readthedocs.io/en/latest/util.html
# https://github.com/gijzelaerr/python-snap7/blob/master/example/boolean.py

class TimerWidget(Widget):
    @gui.decorate_constructor_parameter_types([int, bool])
    def __init__(self, interval_milliseconds, autostart, *args, **kwargs):
        super(TimerWidget, self).__init__(*args, **kwargs)
        self.style.update({'position':'absolute','left':'10px','top':'10px','width':'30px','height':'30px','border':'2px solid dashed'})
        self.interval = interval_milliseconds
        self.autostart = autostart
        self.stop = False
        if autostart: 
            self.onelapsed()

    @gui.decorate_set_on_listener("(self, emitter)")
    @gui.decorate_event
    def onelapsed(self, *args):
        if not self.stop:
            Timer(self.interval/1000.0, self.onelapsed).start()
        self.stop = False
        return ()

    def stop(self, *args):
        self.stop = True
