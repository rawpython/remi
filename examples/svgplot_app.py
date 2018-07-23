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
from remi import start, App
from remi import server
import math
from threading import Timer
import random
import collections


class SvgComposedPoly(gui.SvgGroup):
    """ A group of polyline and circles
    """
    def __init__(self, x, y, maxlen, stroke, color, **kwargs):
        super(SvgComposedPoly, self).__init__(x, y, **kwargs)
        self.maxlen = maxlen
        self.plotData = gui.SvgPolyline(self.maxlen)
        self.append(self.plotData)
        self.set_stroke(stroke, color)
        self.set_fill(color)
        self.circle_radius = stroke
        self.circles_list = list()
        self.x_factor = 1.0
        self.y_factor = 1.0

    def add_coord(self, x, y):
        """ Adds a coord to the polyline and creates another circle
        """
        x = x*self.x_factor
        y = y*self.y_factor
        self.plotData.add_coord(x, y)
        self.circles_list.append(gui.SvgCircle(x, y, self.circle_radius))
        self.append(self.circles_list[-1])
        if len(self.circles_list) > self.maxlen:
            self.remove_child(self.circles_list[0])
            del self.circles_list[0]

    def scale(self, x_factor, y_factor):
        self.x_factor = x_factor/self.x_factor
        self.y_factor = y_factor/self.y_factor
        self.plotData.attributes['points'] = "" 
        tmpx = collections.deque()
        tmpy = collections.deque()

        for c in self.circles_list:
            self.remove_child(c)
        self.circles_list = list()

        while len(self.plotData.coordsX)>0:
            tmpx.append( self.plotData.coordsX.popleft() )
            tmpy.append( self.plotData.coordsY.popleft() )

        while len(tmpx)>0:
            self.add_coord(tmpx.popleft(), tmpy.popleft())
            
        self.x_factor = x_factor
        self.y_factor = y_factor
        

class SvgPlot(gui.Svg):
    def __init__(self, width, height):
        super(SvgPlot, self).__init__(width, height)
        self.width = width
        self.height = height
        self.polyList = []
        self.font_size = 15
        self.plot_inner_border = self.font_size
        self.textYMin = gui.SvgText(0, self.height + self.font_size, "min")
        self.textYMax = gui.SvgText(0, 0, "max")
        self.textYMin.style['font-size'] = gui.to_pix(self.font_size)
        self.textYMax.style['font-size'] = gui.to_pix(self.font_size)
        self.append([self.textYMin, self.textYMax])

    def append_poly(self, polys):
        for poly in polys:
            self.append(poly)
            self.polyList.append(poly)
            poly.textXMin = gui.SvgText(0, 0, "actualValue")
            poly.textXMax = gui.SvgText(0, 0, "actualValue")
            poly.textYVal = gui.SvgText(0, 0, "actualValue")
            poly.textYVal.style['font-size'] = gui.to_pix(self.font_size)

            poly.lineYValIndicator = gui.SvgLine(0, 0, 0, 0)
            poly.lineXMinIndicator = gui.SvgLine(0, 0, 0, 0)
            poly.lineXMaxIndicator = gui.SvgLine(0, 0, 0, 0)
            self.append([poly.textXMin, poly.textXMax, poly.textYVal, poly.lineYValIndicator, 
                poly.lineXMinIndicator, poly.lineXMaxIndicator])

    def remove_poly(self, poly):
        self.remove_child(poly)
        self.polyList.remove(poly)
        self.remove_child(poly.textXMin)
        self.remove_child(poly.textXMax)
        self.remove_child(poly.textYVal)

    def render(self):
        self.set_viewbox(-self.plot_inner_border, -self.plot_inner_border, self.width + self.plot_inner_border * 2,
                         self.height + self.plot_inner_border * 2)
        if len(self.polyList) < 1:
            return
        minX = min(self.polyList[0].plotData.coordsX)
        maxX = max(self.polyList[0].plotData.coordsX)
        minY = min(self.polyList[0].plotData.coordsY)
        maxY = max(self.polyList[0].plotData.coordsY)

        for poly in self.polyList:
            minX = min(minX, min(poly.plotData.coordsX))
            maxX = max(maxX, max(poly.plotData.coordsX))
            minY = min(minY, min(poly.plotData.coordsY))
            maxY = max(maxY, max(poly.plotData.coordsY))
        self.textYMin.set_text("min:%s" % minY)
        self.textYMax.set_text("max:%s" % maxY)

        i = 1
        for poly in self.polyList:
            scaledTranslatedYpos = (-poly.plotData.coordsY[-1] + maxY + (self.height-(maxY-minY))/2.0)

            textXpos = self.height / (len(self.polyList) + 1) * i

            poly.textXMin.set_text(str(min(poly.plotData.coordsX)))
            poly.textXMin.set_fill(poly.attributes['stroke'])

            poly.textXMin.set_position(-textXpos, (min(poly.plotData.coordsX) - minX) )
            poly.textXMin.attributes['transform'] = "rotate(%s)" % (-90)
            poly.textXMax.set_text(str(max(poly.plotData.coordsX)))
            poly.textXMax.set_fill(poly.attributes['stroke'])
            poly.textXMax.set_position(-textXpos, (max(poly.plotData.coordsX) - minX) )

            poly.textXMax.attributes['transform'] = "rotate(%s)" % (-90)
            poly.textYVal.set_text(str(poly.plotData.coordsY[-1]))
            poly.textYVal.set_fill(poly.attributes['stroke'])
            poly.textYVal.set_position(0, scaledTranslatedYpos)

            poly.lineYValIndicator.set_stroke(1, poly.attributes['stroke'])
            poly.lineXMinIndicator.set_stroke(1, poly.attributes['stroke'])
            poly.lineXMaxIndicator.set_stroke(1, poly.attributes['stroke'])
            poly.lineYValIndicator.set_coords(0, scaledTranslatedYpos, self.width, scaledTranslatedYpos)
            poly.lineXMinIndicator.set_coords((min(poly.plotData.coordsX) - minX), 0,
                                              (min(poly.plotData.coordsX) - minX), self.height)
            poly.lineXMaxIndicator.set_coords((max(poly.plotData.coordsX) - minX), 0,
                                              (max(poly.plotData.coordsX) - minX), self.height)
            poly.attributes['transform'] = ('translate(%s,%s)' % (-minX, maxY + (self.height-(maxY-minY))/2.0) + 
                                            ' scale(%s,%s)' % ((1.0), -(1.0)))
            i = i + 1


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        self.wid = gui.VBox(margin='0px auto')

        self.svgplot = SvgPlot(600, 600)
        self.svgplot.style['margin'] = '10px'
        self.plotData1 = SvgComposedPoly(0,0,60,2.0, 'rgba(255,0,0,0.8)')
        self.plotData2 = SvgComposedPoly(0,0,60,1.0, 'green')
        self.plotData3 = SvgComposedPoly(0,0,30,3.0, 'orange')
        self.svgplot.append_poly([self.plotData1, self.plotData2, self.plotData3])

        scale_factor_x = 1.0
        scale_factor_y = 200.0
        self.plotData1.scale(scale_factor_x, scale_factor_y)
        self.plotData2.scale(scale_factor_x, scale_factor_y)
        self.plotData3.scale(scale_factor_x, scale_factor_y)

        self.wid.append(self.svgplot)

        self.count = 0
        self.add_data()

        bt = gui.Button("Zoom - ")
        bt.onclick.connect(self.zoom_out)
        self.wid.append(bt)

        # returning the root widget
        return self.wid

    def zoom_out(self, emitter):
        scale_factor_x = 0.5
        scale_factor_y = 100.0
        self.plotData1.scale(scale_factor_x, scale_factor_y)
        self.plotData2.scale(scale_factor_x, scale_factor_y)
        self.plotData3.scale(scale_factor_x, scale_factor_y)

    def add_data(self):
        with self.update_lock:
            #the scale factors are used to adapt the values to the view
            self.plotData1.add_coord(self.count, math.atan(self.count / 180.0 * math.pi))
            self.plotData2.add_coord(self.count, math.cos(self.count / 180.0 * math.pi))
            self.plotData3.add_coord(self.count, math.sin(self.count / 180.0 * math.pi))
            self.svgplot.render()
            self.count += 10
            Timer(0.1, self.add_data).start()


if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=0, update_interval=0.1, multiple_instance=True)
