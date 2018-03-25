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

from remi.game.canvas import Canvas
from remi.game.color import Color

def rect(canvas, color, rect, width=0):
    canvas.draw('''var canvas = document.getElementById('%s');
var ctx = canvas.getContext('2d');
%s
ctx.%s(%s);%s''' % (
        canvas.id,
        ('ctx.fillStyle = "%s";' % color) if width == 0 else (
            'ctx.lineWidth = "%spx"; ctx.strokeStyle = "%s"' % (width, color)),
        'fillRect' if width == 0 else 'rect',
        rect,
        '' if width == 0 else 'ctx.stroke();'
    ))
    
def line(canvas, color, start_pos, end_pos, width=1):
    canvas.draw('''var canvas = document.getElementById('%s');
var ctx = canvas.getContext('2d');
ctx.lineWidth = "%spx";
ctx.strokeStyle = "%s";
ctx.beginPath();
ctx.moveTo(%s, %s);
ctx.lineTo(%s, %s);
ctx.stroke();''' % (canvas.id, width, color,
                    start_pos[0], start_pos[1],
                    end_pos[0], end_pos[1]))
    
def lines(canvas, color, pointlist, width=1):
    start = pointlist[0]
    pointlist = pointlist[1:]
    js = '''var canvas = document.getElementById('%s');
var ctx = canvas.getContext('2d');
ctx.lineWidth = "%spx";
ctx.strokeStyle = "%s";
ctx.beginPath();
ctx.moveTo(%s, %s);
''' % (canvas.id, width, color, start[0], start[1])
    for point in pointlist:
        js += 'ctx.lineTo(%s, %s);' % (point[0], point[1])
    js += 'ctx.stroke();'
    canvas.draw(js)

def circle(canvas, color, pos, radius, width=0):
    canvas.draw('''var canvas = document.getElementById('%s');
var ctx = canvas.getContext('2d');
ctx.lineWidth = "%spx";
ctx.strokeStyle = "%s";%s
ctx.beginPath();
ctx.arc(%s, %s, %s, 0, 6.30);%s
ctx.stroke();''' % (
    canvas.id,
    width, color,
    ('ctx.fillStyle="%s";' % color) if (width == 0) else '',
    pos[0], pos[1], radius,
    'ctx.fill();' if (width == 0) else ''))
