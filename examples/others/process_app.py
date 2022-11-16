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
import remi.server
from remi import start, App
import os #for path handling
import inspect


class MixinPositionSize():
    def get_position(self):
        return float(self.attr_x), float(self.attr_y)

    def get_size(self):
        return float(self.attr_width), float(self.attr_height)


class MoveableWidget(gui.EventSource, MixinPositionSize):
    container = None
    def __init__(self, container, *args, **kwargs):
        gui.EventSource.__init__(self)
        self.container = container
        self.active = False
        self.onmousedown.do(self.start_drag, js_stop_propagation=True, js_prevent_default=True)
            
    def start_drag(self, emitter, x, y):
        self.active = True
        self.container.onmousemove.do(self.on_drag, js_stop_propagation=True, js_prevent_default=True)
        self.container.onmouseup.do(self.stop_drag)
        self.container.onmouseleave.do(self.stop_drag, 0, 0)

    @gui.decorate_event
    def stop_drag(self, emitter, x, y):
        self.active = False
        return (x, y)

    @gui.decorate_event
    def on_drag(self, emitter, x, y):
        if self.active:
            self.set_position(float(x) - float(self.attr_width)/2.0, float(y) - float(self.attr_height)/2.0)
        return (x, y)


class Input():
    name = None
    typ = None
    source = None #has to be an Output

    def __init__(self, name, typ = None):
        self.name = name
        self.typ = typ

    def get_value(self):
        return self.source.get_value()
    
    def link(self, output):
        self.source = output


class Output():
    name = None
    typ = None
    destination = None #has to be an Input
    value = None

    def __init__(self, name, typ = None):
        self.name = name
        self.typ = typ

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def link(self, input):
        self.destination = input
        

class Subprocess():
    name = None
    inputs = None
    outputs = None

    def decorate_process(output_list):
        """ setup a method as a process Subprocess """
        """
            input parameters can be obtained by introspection
            outputs values (return values) are to be described with decorator
        """
        def add_annotation(method):
            setattr(method, "_outputs", output_list)
            return method
        return add_annotation

    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.outputs = {}

    def add_io(self, io):
        if issubclass(type(io), Input):
            self.inputs[io.name] = io
        else:
            self.outputs[io.name] = io
    
    @decorate_process([])
    def do(self):
        return True, 28


class InputView(Input, gui.SvgSubcontainer, MixinPositionSize):
    placeholder = None
    label = None
    def __init__(self, name, *args, **kwargs):
        width = 10 * len(name)
        height = 20
        gui.SvgSubcontainer.__init__(self, 0, 0, width, height, *args, **kwargs)
        self.placeholder = gui.SvgRectangle(0, 0, width, height)
        self.placeholder.set_stroke(1, 'black')
        self.placeholder.set_fill("lightgray")
        self.append(self.placeholder)

        self.label = gui.SvgText("0%", "50%", name)
        self.label.attr_dominant_baseline = 'middle'
        self.label.attr_text_anchor = "start"
        self.append(self.label)

        Input.__init__(self, name, "")

    def set_size(self, width, height):
        if self.placeholder:
            self.placeholder.set_size(width, height)
        return super().set_size(width, height)

    @gui.decorate_event
    def onpositionchanged(self):
        return ()


class OutputView(Output, gui.SvgSubcontainer, MixinPositionSize):
    placeholder = None
    label = None
    def __init__(self, name, *args, **kwargs):
        width = 10 * len(name)
        height = 20
        gui.SvgSubcontainer.__init__(self, 0, 0, width, height, *args, **kwargs)
        self.placeholder = gui.SvgRectangle(0, 0, width, height)
        self.placeholder.set_stroke(1, 'black')
        self.placeholder.set_fill("lightgray")
        self.append(self.placeholder)

        self.label = gui.SvgText("100%", "50%", name)
        self.label.attr_dominant_baseline = 'middle'
        self.label.attr_text_anchor = "end"
        self.append(self.label)

        Output.__init__(self, name, "")

    def set_size(self, width, height):
        if self.placeholder:
            self.placeholder.set_size(width, height)
        return super().set_size(width, height)

    def set_value(self, value):
        if type(value) == bool:
            self.label.set_fill('white')
            self.placeholder.set_fill('blue' if value else 'BLACK')
        else:
            self.label.set_text(self.name + " : " + str(value))

        Output.set_value(self, value)

    @gui.decorate_event
    def onpositionchanged(self):
        return ()


class Link(gui.SvgPolyline):
    source = None
    destination = None
    def __init__(self, source_widget, destination_widget, *args, **kwargs):
        gui.SvgPolyline.__init__(self, 2, *args, **kwargs)
        self.set_stroke(1, 'black')
        self.set_fill('transparent')
        self.attributes['stroke-dasharray'] = "4 2"
        self.source = source_widget
        self.source.onpositionchanged.do(self.update_path)
        self.destination = destination_widget
        self.destination.onpositionchanged.do(self.update_path)

        self.source.destinaton = self.destination
        self.destination.source = self.source
        self.update_path()

    def update_path(self, emitter=None):
        self.attributes['points'] = ''

        x,y = self.source.get_position()
        w,h = self.source.get_size()
        xsource_parent, ysource_parent = self.source._parent.get_position()
        wsource_parent, hsource_parent = self.destination._parent.get_size()

        xsource = xsource_parent + wsource_parent
        ysource = ysource_parent + y + h/2.0
        self.add_coord(xsource, ysource)

        x,y = self.destination.get_position()
        w,h = self.destination.get_size()
        xdestination_parent, ydestination_parent = self.destination._parent.get_position()
        wdestination_parent, hdestination_parent = self.destination._parent.get_size()

        xdestination = xdestination_parent
        ydestination = ydestination_parent + y + h/2.0

        offset = 10

        if xdestination - xsource < offset*2:
            self.maxlen = 6
            """
                    [   source]---,
                                  |
                        __________|
                        |
                        '----[destination   ]
            """
            self.add_coord(xsource + offset, ysource)

            if ydestination > ysource:
                #self.add_coord(xsource + offset, ysource + (ydestination - ysource)/2.0)
                #self.add_coord(xdestination - offset, ysource + (ydestination - ysource)/2.0)
                self.add_coord(xsource + offset, (ysource_parent + hsource_parent)  + (ydestination_parent - (ysource_parent + hsource_parent))/2.0)
                self.add_coord(xdestination - offset, (ysource_parent + hsource_parent)  + (ydestination_parent - (ysource_parent + hsource_parent))/2.0)
            else:
                self.add_coord(xsource + offset, (ydestination_parent + hdestination_parent)  + (ysource_parent - (ydestination_parent + hdestination_parent))/2.0)
                self.add_coord(xdestination - offset, (ydestination_parent + hdestination_parent)  + (ysource_parent - (ydestination_parent + hdestination_parent))/2.0)
            self.add_coord(xdestination - offset, ydestination)

        else:
            self.maxlen = 4
            """
                    [   source]---,
                                  |
                                  '------[destination   ]
            """
            self.add_coord(xsource + (xdestination-xsource)/2.0, ysource)
            self.add_coord(xdestination - (xdestination-xsource)/2.0, ydestination)

        self.add_coord(xdestination, ydestination)


class SubprocessView(Subprocess, gui.SvgSubcontainer, MoveableWidget):

    label = None
    outline = None

    def __init__(self, name, container, x, y, w, h, *args, **kwargs):
        gui.SvgSubcontainer.__init__(self, x, y, w, h, *args, **kwargs)
        MoveableWidget.__init__(self, container, *args, **kwargs)
        Subprocess.__init__(self, name)

        self.outline = gui.SvgRectangle(0, 0, "100%", "100%")
        self.outline.set_fill('white')
        self.outline.set_stroke(2, 'black')
        self.append(self.outline)

        self.label = gui.SvgText("50%", 0, self.name)
        self.label.attr_text_anchor = "middle"
        self.label.attr_dominant_baseline = 'hanging'
        self.append(self.label)

        #for all the outputs defined by decorator on Subprocess.do
        #   add the related Outputs
        for o in self.do._outputs:
            self.add_io_widget(OutputView(o))

        signature = inspect.signature(self.do)
        for arg in signature.parameters:
            self.add_io_widget(InputView(arg))

    def add_io_widget(self, widget):
        Subprocess.add_io(self, widget)
        self.append(widget)
        widget.onmousedown.do(self.container.onselection_start, js_stop_propagation=True, js_prevent_default=True)
        widget.onmouseup.do(self.container.onselection_end, js_stop_propagation=True, js_prevent_default=True)

        w_width, w_height = widget.get_size()
        w, h = self.get_size()
        h = w_height * (max(len(self.outputs), len(self.inputs))+2)
        gui._MixinSvgSize.set_size(self, w, h)

        i = 1
        for inp in self.inputs.values():
            w_width, w_height = inp.get_size()
            inp.set_position(0, (h/(len(self.inputs)+1))*i-w_height/2.0)
            i += 1

        i = 1
        for o in self.outputs.values():
            w_width, w_height = o.get_size()
            o.set_position(w - w_width, (h/(len(self.outputs)+1))*i-w_height/2.0)
            i += 1

    def set_position(self, x, y):
        if self.inputs != None:
            for inp in self.inputs.values():
                inp.onpositionchanged()

            for o in self.outputs.values():
                o.onpositionchanged()
        return super().set_position(x, y)


class Process():
    subprocesses = None
    def __init__(self):
        self.subprocesses = {}

    def add_subprocess(self, subprocess):
        self.subprocesses[subprocess.name] = subprocess

    def do(self):
        for subprocesses in self.subprocesses.values():
            parameters = {}
            all_inputs_connected = True
            for IN in subprocesses.inputs.values():
                if IN.source == None:
                    all_inputs_connected = False
                    continue
                parameters[IN.name] = IN.get_value()
            
            if not all_inputs_connected:
                return
            output_results = subprocesses.do(**parameters)
            i = 0
            for OUT in subprocesses.outputs.values():
                if type(output_results) in (tuple, list):
                    OUT.set_value(output_results[i])
                else:
                    OUT.set_value(output_results)
                i += 1


class ProcessView(gui.Svg, Process):
    selected_input = None
    selected_output = None

    def __init__(self, *args, **kwargs):
        gui.Svg.__init__(self, *args, **kwargs)
        Process.__init__(self)
        self.css_border_color = 'black'
        self.css_border_width = '1'
        self.css_border_style = 'solid'
        self.style['background-color'] = 'lightyellow'

    def onselection_start(self, emitter, x, y):
        self.selected_input = self.selected_output = None
        print("selection start: ", type(emitter))
        if type(emitter) == InputView:
            self.selected_input = emitter
        else:
            self.selected_output = emitter

    def onselection_end(self, emitter, x, y):
        print("selection end: ", type(emitter))
        if type(emitter) == InputView:
            self.selected_input = emitter
        else:
            self.selected_output = emitter

        if self.selected_input != None and self.selected_output != None:
            link = Link(self.selected_output, self.selected_input)
            self.append(link)

    def add_subprocess(self, subprocess):
        self.append(subprocess)
        Process.add_subprocess(self, subprocess)


class BOOL(SubprocessView):
    def __init__(self, name, initial_value, *args, **kwargs):
        SubprocessView.__init__(self, name, *args, **kwargs)
        self.outputs['OUT'].set_value(initial_value)

    @Subprocess.decorate_process(['OUT'])
    def do(self):
        OUT = self.outputs['OUT'].get_value()
        return OUT

class NOT(SubprocessView):
    @Subprocess.decorate_process(['OUT'])
    def do(self, IN):
        OUT = not IN
        return OUT

class AND(SubprocessView):
    @Subprocess.decorate_process(['OUT'])
    def do(self, IN1, IN2):
        OUT = IN1 and IN2
        return OUT

class OR(SubprocessView):
    @Subprocess.decorate_process(['OUT'])
    def do(self, IN1, IN2):
        OUT = IN1 and IN2
        return OUT


class MyApp(App):
    process = None

    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(MyApp, self).__init__(*args, static_file_path=res_path)

    def idle(self):
        if self.process is None:
            return
        self.process.do()

    def main(self):
        self.main_container = gui.VBox(width=800, height=800, margin='0px auto')
        
        self.process = ProcessView(width=600, height=600)
        self.main_container.append(self.process)
        
        y = 10
        m = BOOL("BOOL", False, self.process, 100, y, 200, 100)
        self.process.add_subprocess(m)

        y += 110
        m = BOOL("BOOL 2", True, self.process, 100, y, 200, 100)
        self.process.add_subprocess(m)

        y += 110
        m = NOT("NOT 0", self.process, 100, y, 200, 100)
        self.process.add_subprocess(m)

        y += 110
        m = AND("AND", self.process, 100, y, 200, 100)
        self.process.add_subprocess(m)

        y += 110
        m = OR("OR", self.process, 100, y, 200, 100)
        self.process.add_subprocess(m)

        # returning the root widget
        return self.main_container


    
if __name__ == "__main__":
    start(MyApp, debug=False, address='0.0.0.0', port=0, update_interval=0.01)
