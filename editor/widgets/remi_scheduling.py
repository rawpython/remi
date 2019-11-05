# -*- coding: utf-8 -*-

import remi.gui
from remi.gui import *
import remi.gui as gui
from threading import Timer


# https://python-snap7.readthedocs.io/en/latest/util.html
# https://github.com/gijzelaerr/python-snap7/blob/master/example/boolean.py

class TimerWidget(Widget):
    icon = "data:image/png;base64,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"

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
