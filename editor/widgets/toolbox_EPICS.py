# -*- coding: utf-8 -*-

import remi
import remi.gui as gui
from remi.gui import *
import traceback
import time
import math
import epics
# from epics import caget, caput, cainfo

style_inheritance_dict = {
    "opacity": "inherit",
    "overflow": "inherit",
    "background-color": "inherit",
    "background-image": "inherit",
    "background-position": "inherit",
    "background-repeat": "inherit",
    "border-color": "inherit",
    "border-width": "inherit",
    "border-style": "inherit",
    "border-radius": "inherit",
    "color": "inherit",
    "font-family": "inherit",
    "font-size": "inherit",
    "font-style": "inherit",
    "font-weight": "inherit",
    "white-space": "inherit",
    "letter-spacing": "inherit",
}
style_inheritance_text_dict = {
    "opacity": "inherit",
    "overflow": "inherit",
    "color": "inherit",
    "font-family": "inherit",
    "font-size": "inherit",
    "font-style": "inherit",
    "font-weight": "inherit",
    "white-space": "inherit",
    "letter-spacing": "inherit",
}


# noinspection PyUnresolvedReferences
class EPICSWidget(object):
    @property
    @gui.editor_attribute_decorator("WidgetSpecific", "The PV name", str, {})
    def epics_pv_name(self):
        return self.__epics_pv_name

    @epics_pv_name.setter
    def epics_pv_name(self, v):
        self.__epics_pv_name = v
        self.disconnect()
        try:
            self.epics_pv = epics.PV(
                self.__epics_pv_name,
                auto_monitor=True,
                callback=self.onChanges,
                connection_callback=self.onConnectionChange,
                connection_timeout=2,
            )
        except Exception:
            print(traceback.format_exc())

    epics_pv = None  # here will be stored the PV instance
    app_instance = None

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        if self.epics_pv:
            self.epics_pv.clear_auto_monitor()
            self.epics_pv.disconnect()

    @decorate_set_on_listener(
        "(self, emitter, pvname=None, conn=None, chid=None, **kwargs)"
    )
    @decorate_event
    def onConnectionChange(self, pvname=None, conn=None, chid=None, **kwargs):
        # print('ca connection status changed:  ', pvname,  conn, chid)
        # Here I use the outline red color to show the unconnected state
        # of course this can be avoided or changed
        self.style["outline"] = "1px solid red"
        if conn:
            del self.style["outline"]
        return (pvname, conn, chid, kwargs)

    @decorate_set_on_listener("(self, emitter, pvname=None, value=None, **kwargs)")
    @decorate_event
    def onChanges(self, pvname=None, value=None, **kwargs):
        # as default I write the value to the widget itself
        self.set_value(str(value))
        return (pvname, value, kwargs)

    def search_app_instance(self, node):
        if issubclass(node.__class__, remi.server.App):
            return node
        if not hasattr(node, "get_parent"):
            return None
        return self.search_app_instance(node.get_parent())

    def get_app_instance(self):
        if self.app_instance is None:
            self.app_instance = self.search_app_instance(self)
        return self.app_instance


class EPICSBooleanButton(gui.Container, EPICSWidget):
    """A Button widget that sets the bit when clicked."""

    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAuCAYAAABXuSs3AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAKMSURBVGiB7ZqxaxNRGMB/9+7uXZK2aaMVEUWEKNSh4CQIrhWnujiIQqGig7gXF/+B7tLNbp2KQyfBwcVdsdhWJa5WHZKKvZqXe3cO57VNmraJyd0ZuB88LnkvfO/H43sfB18Mz/OCIAhoN4DdZ9IYhrH7bDesSPJlRfHsrc+nmpGK6HGcGQp4clVwsywBMJRSgVKKqWXNpitS1juaS6M+L26ZSCnDE1dKsenaAHy/MUNjtNJ10JG1WYofHvTbtYnPWwKlFLZth+Ke5wGheKP0EXVireugemizz5rt8TyPIAgQe+KDQZO41jptn47RWofiAL7vp+3TMZGrtb9mAxTfP0bnf3QdMPf1Wt/kjiLytVoXRtZnEhHolf+7cB9BJp40mXjSDKz4gXLYHQ6vHtmUD8z7LC+4zAGz00M8PXv4q3Jl4xdTr7vfuUfx9pvP3xnm9v086893WFzZZjFamMzz7rpg7c02d1d72zOWVJn75oNjcDmO4H+JRXz+tKCyEaZKXPQlVcoTw3yZaJ776dpAox/h2xJLjocXUrI02eg5lw8jllRZXPGoYHBqPI7oIQNbx2MRn522KNc1S/9Qnzslpsvps7yws1e/Y6BH8TpTC/XOf766w5U+XdYsx5MmE0+aTDxpMvGkycSTRkTNoEEh8hXRl0Ehch3cEzcMA9M0GbdV2k7Hcj7/G9M098Qty+LhxSrnHDdtt0M5adW5d2ELy7LCU1dKBa7rUqvVqFaruK5LvV5Ptbvc2lV2HIdCoUCpVGJsbIxCoYAVLRSLRaSUKKVQStHaYkmDSFxKiZSSXC6H4zjhvOd5ge/7aK2bRtQkSruXL4TANM2mIYTA0FoHrWmR9h8QIlpTZv/nP6KyI2uh/zMtAAAAAElFTkSuQmCC"

    @property
    @gui.editor_attribute_decorator(
        "WidgetSpecific",
        "Specifies if the button is toggle or must reset the value on release",
        bool,
        {},
    )
    def toggle(self):
        return self.__toggle

    @toggle.setter
    def toggle(self, v):
        self.__toggle = v
        self.button.onmouseup.do(self.reset_bit if not self.__toggle else None)

    @property
    @editor_attribute_decorator("WidgetSpecific", """Text content""", str, {})
    def text(self):
        return self.button.get_text()

    @text.setter
    def text(self, value):
        self.button.set_text(value)

    button = None  # The gui.Button widget instance
    led = None  # The led indicator Widget

    def __init__(
        self,
        button_label="epics button",
        epics_pv_name="",
        toggle=False,
        *args,
        **kwargs,
    ):
        self.color_inactive = "darkgray"
        self.color_active = "rgb(0,255,0)"
        self.button = gui.Button(
            button_label, width="100%", height="100%", style=style_inheritance_dict
        )
        self.led = gui.Widget(
            width=15,
            height=5,
            style={
                "position": "absolute",
                "left": "2px",
                "top": "2px",
                "background-color": self.color_inactive,
            },
        )
        self.led_status = False
        default_style = {
            "position": "absolute",
            "left": "10px",
            "top": "10px",
            "background-color": "rgb(4, 90, 188)",
            "color": "white",
        }
        default_style.update(kwargs.get("style", {}))
        kwargs["style"] = default_style
        kwargs["width"] = kwargs["style"].get("width", kwargs.get("width", "100px"))
        kwargs["height"] = kwargs["style"].get("height", kwargs.get("height", "100px"))
        super(EPICSBooleanButton, self).__init__(*args, **kwargs)
        _style = {"position": "relative"}
        _style.update(style_inheritance_dict)
        self.append(
            gui.Container(
                children=[self.button, self.led],
                width="100%",
                height="100%",
                style=_style,
            )
        )
        self.toggle = toggle
        self.epics_pv_name = epics_pv_name
        self.button.onmousedown.do(self.set_bit)

    def set_bit(self, emitter, *args, **kwargs):
        self.pressed = True
        self.written = False
        value = 1
        if self.toggle:
            value = 0 if self.led_status else 1
        self.epics_pv.put(value, callback=(self.put_done if not self.toggle else None))

    def put_done(self, *args, **kwargs):
        self.written = True
        # this function gets called when a set_bit is completed and the button is not toggle
        # and so the value have to be reset
        if not self.pressed:
            self.epics_pv.put(0)

    def reset_bit(self, emitter, x, y, *args, **kwargs):
        self.pressed = False
        if self.written:
            self.epics_pv.put(0)

    def set_value(self, value):
        if not self.get_app_instance():
            return
        with self.get_app_instance().update_lock:
            # this function gets called when the camonitor notifies a change on the PV
            self.led_status = float(value) > 0.0
            self.led.style.update(
                {
                    "background-color": self.color_active
                    if self.led_status
                    else self.color_inactive
                }
            )


class EPICSLed(HBox, EPICSWidget):
    """A Status indicator widget."""

    icon = "data:image/png;base64,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"

    @property
    @editor_attribute_decorator("Geometry", """Widget width.""", "css_size", {})
    def css_width(self):
        return self.style.get("width", None)

    @css_width.setter
    def css_width(self, value):
        self.style["width"] = str(value)
        self._update_size()

    @property
    @editor_attribute_decorator("Geometry", """Widget height.""", "css_size", {})
    def css_height(self):
        return self.style.get("height", None)

    @css_height.setter
    def css_height(self, value):
        self.style["height"] = str(value)
        self._update_size()

    label_value = None  # the gui.Label used to show the value 0 or 1

    def __init__(self, epics_pv_name="", *args, **kwargs):
        self.color_inactive = "darkgray"
        self.color_active = "rgb(0,180,0)"
        default_style = {
            "position": "absolute",
            "left": "10px",
            "top": "10px",
            "color": "white",
            "background-color": self.color_inactive,
            "align-items": "center",
            "justify-content": "center",
        }
        default_style.update(kwargs.get("style", {}))
        kwargs["style"] = default_style
        kwargs["width"] = kwargs["style"].get("width", kwargs.get("width", "50px"))
        kwargs["height"] = kwargs["style"].get("height", kwargs.get("height", "50px"))
        super(EPICSLed, self).__init__(*args, **kwargs)
        _style = {"text-align": "center"}
        _style.update(style_inheritance_text_dict)
        self.label_value = gui.Label("0", style=_style)
        self.append(self.label_value)
        self.epics_pv_name = epics_pv_name

    def _update_size(self):
        width = gui.from_pix(self.style.get("width", "100").replace("%", ""))
        height = gui.from_pix(self.style.get("height", "100").replace("%", ""))
        radius = min(width, height) / 2
        self.style["border-radius"] = gui.to_pix(radius)

    def set_value(self, value):
        if not self.get_app_instance():
            return
        with self.get_app_instance().update_lock:
            _value = float(value)
            self.label_value.set_text("1" if _value > 0.0 else "0")
            self.style.update(
                {
                    "background-color": self.color_active
                    if _value > 0.0
                    else self.color_inactive
                }
            )


class EPICSValueMeterWidget(Progress, EPICSWidget):
    """A simple progress bar indicating a value."""

    icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAApCAYAAACoYAD2AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAlwSFlzAAAOwgAADsIBFShKgAAAAG1JREFUWEft1qENgEAMQNEec6AwDMG4jIbC3QZAQuXhvijJf6aVP+mJa9cjiptylmYkxUiKkRQjKUZSjKQYSTGSMvyZt/3M7dux9dx487Lm9vLclP++yWo8N8VIipEUIylGUoykGEkxkmIkI+IGyZcQRHB9PC8AAAAASUVORK5CYII="

    def __init__(self, epics_pv_name="", max_value=100, *args, **kwargs):
        default_style = {"position": "absolute", "left": "10px", "top": "10px"}
        default_style.update(kwargs.get("style", {}))
        kwargs["style"] = default_style
        kwargs["width"] = kwargs["style"].get("width", kwargs.get("width", "100px"))
        kwargs["height"] = kwargs["style"].get("height", kwargs.get("height", "30px"))
        super(EPICSValueMeterWidget, self).__init__(0, max_value, *args, **kwargs)
        self.epics_pv_name = epics_pv_name

    def set_value(self, value):
        if not self.get_app_instance():
            return
        with self.get_app_instance().update_lock:
            Progress.set_value(self, value)


try:
    import pygal
except ImportError:
    print("It is required to install pygal to use EPICSPlotPV widget")


class EPICSPlotPV(gui.Svg, EPICSWidget):
    """A simple plot bar indicating a value.
    REQUIRES library pygal to be installed
    """

    icon = "data:image/png;base64,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"

    @property
    @editor_attribute_decorator(
        "WidgetSpecific",
        """Defines the maximum values count.""",
        int,
        {"possible_values": "", "min": 0, "max": 65535, "default": 0, "step": 1},
    )
    def max_values_count(self):
        return self.values.maxlen

    @max_values_count.setter
    def max_values_count(self, value):
        self.values.maxlen = int(value)

    def __init__(self, epics_pv_name="", max_values_count=100, *args, **kwargs):
        w = kwargs.get("style", {}).get("width", kwargs.get("width", 100))
        h = kwargs.get("style", {}).get("height", kwargs.get("height", 100))
        if "width" in kwargs.keys():
            del kwargs["width"]
        if "height" in kwargs.keys():
            del kwargs["height"]
        default_style = {
            "position": "absolute",
            "left": "10px",
            "top": "10px",
            "overflow": "hidden",
            "background-color": "lightgray",
            "margin": "10px",
        }
        default_style.update(kwargs.get("style", {}))
        kwargs["style"] = default_style
        super(EPICSPlotPV, self).__init__(w, h, *args, **kwargs)
        self.values = gui.SvgPolyline(max_values_count)
        self.epics_pv_name = epics_pv_name

    def set_value(self, value):
        if not self.get_app_instance():
            return
        with self.get_app_instance().update_lock:
            self.values.add_coord(time.clock(), float(value))
            try:
                plot = pygal.XY()
                pairs = []
                for i in range(0, len(self.values.coordsX)):
                    pairs.append([self.values.coordsX[i], self.values.coordsY[i]])
                plot.add(self.epics_pv_name, pairs)
                self.add_child("chart", plot.render())
            except Exception:
                self.style["overflow"] = "visible"
                self.add_child(
                    "chart", gui.SvgText(10, 10, "Install pygal to use this widget")
                )


class EPICSValueGaugeWidget(Svg, EPICSWidget):
    """A gauge indicator for an EPICS PV value"""

    icon = "data:image/png;base64,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"

    @property
    @editor_attribute_decorator(
        "WidgetSpecific",
        """Defines the minimum value.""",
        float,
        {"possible_values": "", "min": -65535, "max": 65535, "default": 0, "step": 1},
    )
    def min_value(self):
        return self.__dict__.get("__min_value", 0)

    @min_value.setter
    def min_value(self, value):
        self.__dict__["__min_value"] = value
        self.text_min_value.set_text(str(value))

    @property
    @editor_attribute_decorator(
        "WidgetSpecific",
        """Defines the maximum value.""",
        float,
        {"possible_values": "", "min": -65535, "max": 65535, "default": 0, "step": 1},
    )
    def max_value(self):
        return self.__dict__.get("__max_value", 1)

    @max_value.setter
    def max_value(self, value):
        self.__dict__["__max_value"] = value
        self.text_max_value.set_text(str(value))

    indicator = None  # a gui.SvgPolygon that indicates the actual value
    indicator_pin = None  # a gui.SvgCircle around which the indicator rotates
    text_min_value = None  # the gui.SvgText min value indicator
    text_max_value = None  # the gui.SvgText max value indicator
    text_actual_value = None  # the gui.SvgText value indicator

    def __init__(self, epics_pv_name="", min_value=0, max_value=100, *args, **kwargs):
        w = kwargs.get("style", {}).get("width", kwargs.get("width", 100))
        h = kwargs.get("style", {}).get("height", kwargs.get("height", 100))
        if "width" in kwargs.keys():
            del kwargs["width"]
        if "height" in kwargs.keys():
            del kwargs["height"]
        default_style = {"position": "absolute", "left": "10px", "top": "10px"}
        default_style.update(kwargs.get("style", {}))
        kwargs["style"] = default_style
        super(EPICSValueGaugeWidget, self).__init__(width=w, height=h, *args, **kwargs)
        self.epics_pv_name = epics_pv_name

        # the indicator
        self.indicator = gui.SvgPolygon(_maxlen=4)
        self.indicator.set_stroke(width=0.001, color="red")
        self.indicator.set_fill("red")

        indicator_pin_radius = 0.05
        self.indicator_pin = gui.SvgCircle(0, 0.5, indicator_pin_radius)
        self.indicator_pin.set_fill("black")

        # the value signs
        max_value - min_value
        radius_min = 0.4
        radius_max = 0.5
        for i in range(0, 10):
            angle = math.pi / 9 * i
            # sign = gui.SvgLine(math.cos(angle)*radius_min, radius_max-math.sin(angle)*radius_min, math.cos(angle)*radius_max, radius_max-math.sin(angle)*radius_max)
            sign = gui.SvgLine(
                math.cos(angle) * (radius_min - 0.01 + 0.1 * (i + 1) / 10),
                radius_max - math.sin(angle) * (radius_min - 0.01 + 0.1 * (i + 1) / 10),
                math.cos(angle) * radius_max,
                radius_max - math.sin(angle) * radius_max,
            )
            sign.set_stroke(0.01, "black")
            self.append(sign)

        # subindicators value signs
        max_value - min_value
        radius_min = 0.4
        radius_max = 0.5
        for i in range(0, 100):
            angle = math.pi / 99 * i
            # sign = gui.SvgLine(math.cos(angle)*radius_min, radius_max-math.sin(angle)*radius_min, math.cos(angle)*radius_max, radius_max-math.sin(angle)*radius_max)
            sign = gui.SvgLine(
                math.cos(angle) * (radius_min - 0.01 + 0.1 * (i + 10) / 100),
                radius_max
                - math.sin(angle) * (radius_min - 0.01 + 0.1 * (i + 10) / 100),
                math.cos(angle) * radius_max,
                radius_max - math.sin(angle) * radius_max,
            )
            sign.set_stroke(0.002, "black")
            self.append(sign)

        font_size = 0.1
        self.text_min_value = gui.SvgText(
            -radius_max, 0.5 + font_size + 0.01, str(min_value)
        )
        self.text_min_value.style["font-size"] = gui.to_pix(font_size)
        self.text_min_value.style["text-anchor"] = "start"

        self.text_max_value = gui.SvgText(
            radius_max, 0.5 + font_size + 0.01, str(max_value)
        )
        self.text_max_value.style["font-size"] = gui.to_pix(font_size)
        self.text_max_value.style["text-anchor"] = "end"

        self.text_actual_value = gui.SvgText(
            0, 0.5 + indicator_pin_radius + font_size + 0.01, str(max_value)
        )
        self.text_actual_value.style["font-size"] = gui.to_pix(font_size)
        self.text_actual_value.style["text-anchor"] = "middle"
        self.text_actual_value.style["font-weight"] = "bold"

        self.min_value = min_value
        self.max_value = max_value

        self.append(
            [
                self.indicator,
                self.indicator_pin,
                self.text_min_value,
                self.text_max_value,
                self.text_actual_value,
            ]
        )

        self.set_viewbox(-0.5, 0, 1, 0.70)
        self.value = self.min_value

    def set_value(self, value):
        if not self.get_app_instance():
            return
        with self.get_app_instance().update_lock:
            value = float(value)
            # min value at left
            # max value at right

            # value to radians
            scale = self.max_value - self.min_value
            if scale == 0.0:
                return
            relative_value = value - self.min_value
            angle = relative_value * math.pi / scale
            # inversion min at left
            angle = math.pi - angle

            radius = 0.5
            self.indicator.add_coord(
                math.cos(angle) * radius, radius - math.sin(angle) * radius
            )
            self.indicator.add_coord(
                math.cos(angle + 0.5) * 0.04, radius - math.sin(angle + 0.5) * 0.04
            )  # self.indicator.add_coord(0.02,0.4)
            self.indicator.add_coord(0, radius)
            self.indicator.add_coord(
                math.cos(angle - 0.5) * 0.04, radius - math.sin(angle - 0.5) * 0.04
            )

            if hasattr(self, "actual_value"):
                self.text_actual_value.set_text(str(value))
