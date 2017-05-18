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

import remi.gui as gui
from remi import App
from cli import start_app

import math
from threading import Timer
import random


class InputGauge(gui.VBox):
    #@decorate_constructor_parameter_types([int, int, int, int])
    def __init__(self, width, height, _min, _max, **kwargs):
        super(InputGauge, self).__init__(**kwargs)
        self.set_size(width, height)
        self.gauge = Gauge(width, height, _min, _max)
        self.gauge.set_value(_min)
        self.append(self.gauge)
        
        self.set_on_mousedown_listener(self.confirm_value)
        self.set_on_mousemove_listener(self.gauge.onmousemove)
    
    def confirm_value(self, widget, x, y):
        """event called clicking on the gauge and so changing its value.
           propagates the new value
        """
        self.gauge.onmousedown(self.gauge, x, y)
        params = (self.gauge.value)
        return self.eventManager.propagate(self.EVENT_ONCHANGE, params)

    #@decorate_set_on_listener("confirm_value", "(value, widget)")
    def set_on_confirm_value_listener(self, callback, *userdata):
        self.eventManager.register_listener(self.EVENT_ONCHANGE, callback, *userdata)
    


class Gauge(gui.Svg):
    def __init__(self, width, height, _min, _max):
        super(Gauge, self).__init__(width, height)
        self.width = width
        self.height = height
        self.min = _min
        self.max = _max
        self.scale_angle_range = math.pi*2-1.0
        self.scale_value_range = _max - _min
        self.base_angle = 0 #-self.scale_angle_range/2.0

        self.radius = min(width, height)/2.0
        circle = gui.SvgCircle(width/2.0, height/2.0, self.radius)
        self.append(circle)
        circle.set_fill('gray')
        circle.set_stroke(1,'lightgray')

        circle = gui.SvgCircle(width/2.0, height/2.0, self.radius*92.0/100.0)
        self.append(circle)
        circle.set_fill('lightgray')
        circle.set_stroke(1,'lightgray')

        font_size = self.radius*10.0/100.0
        xy = self.value_to_xy_tuple(_min, self.radius*90.0/100.0)
        textMin = gui.SvgText(xy[0], xy[1], str(_min))
        xy = self.value_to_xy_tuple(_max, self.radius*90.0/100.0)
        textMax = gui.SvgText(xy[0], xy[1], str(_max))
        textMin.style['font-size'] = gui.to_pix(font_size)
        textMax.style['font-size'] = gui.to_pix(font_size)
        textMin.style['text-anchor'] = "end"
        textMax.style['text-anchor'] = "end"
        textMin.set_fill('red')
        textMax.set_fill('green')

        for i in range( 0, 11 ):
            xy1 = self.value_to_xy_tuple(self.min + self.scale_value_range/10*i, self.radius*92.0/100.0)
            xy2 = self.value_to_xy_tuple(self.min + self.scale_value_range/10*i, self.radius)
            tick = gui.SvgLine(xy1[0], xy1[1], xy2[0], xy2[1])
            tick.set_stroke(2, 'white')
            self.append(tick)

        self.append(textMin)
        self.append(textMax)
    
        self.arrow = gui.SvgPolyline()
        self.arrow.add_coord(-self.radius*20.0/100.0,0)
        self.arrow.add_coord(-self.radius*23.0/100.0,self.radius*10.0/100.0)
        self.arrow.add_coord(0,0)
        self.arrow.add_coord(-self.radius*23.0/100.0,-self.radius*10.0/100.0)
        self.arrow.add_coord(-self.radius*20.0/100.0,0)
        self.arrow.style['fill'] = 'white'
        self.arrow.set_stroke(1.0, 'white')
        self.append(self.arrow)

        self.arrow_preview = gui.SvgPolyline()
        self.arrow_preview.add_coord(-self.radius*10.0/100.0,0)
        self.arrow_preview.add_coord(-self.radius*13.0/100.0,self.radius*5.0/100.0)
        self.arrow_preview.add_coord(0,0)
        self.arrow_preview.add_coord(-self.radius*13.0/100.0,-self.radius*5.0/100.0)
        self.arrow_preview.add_coord(-self.radius*10.0/100.0,0)
        self.arrow_preview.style['fill'] = 'beige'
        self.arrow_preview.set_stroke(1.0, 'beige')
        self.append(self.arrow_preview)

        self.set_value(_min)

    def value_to_angle(self, value):
        return self.base_angle + (value-self.min) * self.scale_angle_range / self.scale_value_range #substraction in order to go clockwise
    
    def angle_to_value(self, angle):
        print("angolo:" + str(math.degrees(angle)))
        print("valore:" + str((angle-self.base_angle) * self.scale_value_range / self.scale_angle_range + self.min))
        return (angle-self.base_angle) * self.scale_value_range / self.scale_angle_range + self.min

    def value_to_xy_tuple(self, value, radius):
        return [math.cos(self.value_to_angle(value))*radius + self.radius, self.radius - math.sin(self.value_to_angle(value))*radius]

    def xy_tuple_to_value(self, xy):
        return self.angle_to_value(math.atan2(xy[1], xy[0])%(math.pi*2))

    def set_value(self, value):
        if value<self.min:
            value = self.min
        if value>self.max:
            value = self.max
        self.value = value
        angle = self.value_to_angle(value)
        xy = self.value_to_xy_tuple(value, self.radius-10)
        self.arrow.attributes['transform'] = "translate(%s,%s) rotate(%s)" % (xy[0], xy[1], math.degrees(-angle))
        self.set_value_preview(value)

    def set_value_preview(self, value):
        if value<self.min:
            value = self.min
        if value>self.max:
            value = self.max
        angle = self.value_to_angle(value)
        xy = self.value_to_xy_tuple(value, self.radius-10)
        self.arrow_preview.attributes['transform'] = "translate(%s,%s) rotate(%s)" % (xy[0], xy[1], math.degrees(-angle))

    def onmousedown(self, widget, x, y):
        value = self.xy_tuple_to_value([int(x)-self.radius, -(int(y)-self.radius)])
        self.set_value(value)

    def onmousemove(self, widget, x, y):
        value = self.xy_tuple_to_value([int(x)-self.radius, -(int(y)-self.radius)])
        self.set_value_preview(value)


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        self.wid = gui.VBox(margin='0px auto') #margin 0px auto to center the screen
        self.wid.set_size(620, 620)
        
        self.gauge = InputGauge(200, 200, 1000, 10000)
        self.wid.append(self.gauge)

        # returning the root widget
        return self.wid

if __name__ == "__main__":
    start_app(MyApp, address='0.0.0.0')
