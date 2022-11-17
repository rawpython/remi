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
import time


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

    def is_linked(self):
        return self.source != None


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

    def is_linked(self):
        return self.destination != None
        

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


class SvgTitle(gui.Widget, gui._MixinTextualWidget):
    def __init__(self, text='svg text', *args, **kwargs):
        super(SvgTitle, self).__init__(*args, **kwargs)
        self.type = 'title'
        self.set_text(text)


class InputView(Input, gui.SvgSubcontainer, MixinPositionSize):
    placeholder = None
    label = None
    def __init__(self, name, *args, **kwargs):
        gui.SvgSubcontainer.__init__(self, 0, 0, 0, 0, *args, **kwargs)
        self.placeholder = gui.SvgRectangle(0, 0, 0, 0)
        self.placeholder.set_stroke(1, 'black')
        self.placeholder.set_fill("lightgray")
        self.placeholder.style['cursor'] = 'pointer'
        self.append(self.placeholder)

        self.label = gui.SvgText("0%", "50%", name)
        self.label.attr_dominant_baseline = 'middle'
        self.label.attr_text_anchor = "start"
        self.label.style['cursor'] = 'pointer'
        self.append(self.label)

        Input.__init__(self, name, "")

    def set_size(self, width, height):
        if self.placeholder:
            self.placeholder.set_size(width, height)
        return gui._MixinSvgSize.set_size(self, width, height)

    @gui.decorate_event
    def onpositionchanged(self):
        return ()


class OutputView(Output, gui.SvgSubcontainer, MixinPositionSize):
    placeholder = None
    label = None
    def __init__(self, name, *args, **kwargs):
        gui.SvgSubcontainer.__init__(self, 0, 0, 0, 0, *args, **kwargs)
        self.placeholder = gui.SvgRectangle(0, 0, 0, 0)
        self.placeholder.set_stroke(1, 'black')
        self.placeholder.set_fill("lightgray")
        self.placeholder.style['cursor'] = 'pointer'
        self.append(self.placeholder)

        self.label = gui.SvgText("100%", "50%", name)
        self.label.attr_dominant_baseline = 'middle'
        self.label.attr_text_anchor = "end"
        self.label.style['cursor'] = 'pointer'
        self.append(self.label)

        Output.__init__(self, name, "")

    def set_size(self, width, height):
        if self.placeholder:
            self.placeholder.set_size(width, height)
        return gui._MixinSvgSize.set_size(self, width, height)

    def set_value(self, value):
        if value == self.value:
            return
        if type(value) == bool:
            self.label.set_fill('white')
            self.placeholder.set_fill('blue' if value else 'BLACK')
        
        self.append(SvgTitle(str(value)), "title")

        self.label.attr_title = str(value)

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
        wsource_parent, hsource_parent = self.source._parent.get_size()

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
    label_font_size = 12

    outline = None

    io_font_size = 12
    io_left_right_offset = 10

    def __init__(self, name, container, x = 10, y = 10, *args, **kwargs):
        Subprocess.__init__(self, name)
        gui.SvgSubcontainer.__init__(self, x, y, self.calc_width(), self.calc_height(), *args, **kwargs)
        MoveableWidget.__init__(self, container, *args, **kwargs)

        self.outline = gui.SvgRectangle(0, 0, "100%", "100%")
        self.outline.set_fill('white')
        self.outline.set_stroke(2, 'black')
        self.append(self.outline)

        self.label = gui.SvgText("50%", 0, self.name)
        self.label.attr_text_anchor = "middle"
        self.label.attr_dominant_baseline = 'hanging'
        self.label.css_font_size = gui.to_pix(self.label_font_size)
        self.append(self.label)

        #for all the outputs defined by decorator on Subprocess.do
        #   add the related Outputs
        for o in self.do._outputs:
            self.add_io_widget(OutputView(o))

        signature = inspect.signature(self.do)
        for arg in signature.parameters:
            self.add_io_widget(InputView(arg))

    def calc_height(self):
        inputs_count = 0 if self.inputs == None else len(self.inputs)
        outputs_count = 0 if self.outputs == None else len(self.outputs)
        return self.label_font_size + (max(outputs_count, inputs_count)+2) * self.io_font_size

    def calc_width(self):
        max_name_len_input = 0
        if self.inputs != None:
            for inp in self.inputs.values():
                max_name_len_input = max(max_name_len_input, len(inp.name))

        max_name_len_output = 0
        if self.outputs != None:
            for o in self.outputs.values():
                max_name_len_output = max(max_name_len_output, len(o.name))

        return max((len(self.name) * self.label_font_size), (max(max_name_len_input, max_name_len_output)*self.io_font_size) * 2) + self.io_left_right_offset

    def add_io_widget(self, widget):
        widget.label.css_font_size = gui.to_pix(self.io_font_size)
        widget.set_size(len(widget.name) * self.io_font_size, self.io_font_size)

        Subprocess.add_io(self, widget)
        self.append(widget)
        widget.onmousedown.do(self.container.onselection_start, js_stop_propagation=True, js_prevent_default=True)
        widget.onmouseup.do(self.container.onselection_end, js_stop_propagation=True, js_prevent_default=True)

        self.adjust_geometry()

    def adjust_geometry(self):
        gui._MixinSvgSize.set_size(self, self.calc_width(), self.calc_height())
        w, h = self.get_size()

        i = 1
        for inp in self.inputs.values():
            inp.set_position(0, self.label_font_size + self.io_font_size*i)
            i += 1

        i = 1
        for o in self.outputs.values():
            ow, oh = o.get_size()
            o.set_position(w - ow, self.label_font_size + self.io_font_size*i)
            i += 1

    def set_position(self, x, y):
        if self.inputs != None:
            for inp in self.inputs.values():
                inp.onpositionchanged()

            for o in self.outputs.values():
                o.onpositionchanged()
        return super().set_position(x, y)

    def set_name(self, name):
        self.name = name
        self.label.set_text(name)
        self.adjust_geometry()


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
                continue
            output_results = subprocesses.do(**parameters)
            if output_results is None:
                continue
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
            if self.selected_input.is_linked():
                return
            link = Link(self.selected_output, self.selected_input)
            self.append(link)

    def add_subprocess(self, subprocess):
        self.append(subprocess)
        Process.add_subprocess(self, subprocess)


class STRING(SubprocessView):
    def __init__(self, name, *args, **kwargs):
        SubprocessView.__init__(self, name, *args, **kwargs)
        self.outputs['OUT'].set_value("A STRING VALUE")

    @Subprocess.decorate_process(['OUT'])
    def do(self):
        OUT = self.outputs['OUT'].get_value()
        return OUT

class STRING_SWAP_CASE(SubprocessView):
    def __init__(self, name, *args, **kwargs):
        SubprocessView.__init__(self, name, *args, **kwargs)

    @Subprocess.decorate_process(['OUT'])
    def do(self, EN, IN):
        if not EN:
            return
        OUT = IN.swapcase()
        return OUT

class BOOL(SubprocessView):
    def __init__(self, name, *args, **kwargs):
        SubprocessView.__init__(self, name, *args, **kwargs)
        self.outputs['OUT'].set_value(False)

    @Subprocess.decorate_process(['OUT'])
    def do(self):
        OUT = self.outputs['OUT'].get_value()
        return OUT

class RISING_EDGE(SubprocessView):
    previous_value = None

    @Subprocess.decorate_process(['OUT'])
    def do(self, IN):
        OUT = (self.previous_value != IN) and IN
        self.previous_value = IN
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
        OUT = IN1 or IN2
        return OUT

class XOR(SubprocessView):
    @Subprocess.decorate_process(['OUT'])
    def do(self, IN1, IN2):
        OUT = IN1 != IN2
        return OUT

class PULSAR(SubprocessView):
    ton = 1000
    toff = 1000
    tstart = 0
    def __init__(self, name, *args, **kwargs):
        SubprocessView.__init__(self, name, *args, **kwargs)
        self.outputs['OUT'].set_value(False)
        self.tstart = time.time()

    @Subprocess.decorate_process(['OUT'])
    def do(self):
        OUT = (int((time.time() - self.tstart)*1000) % (self.ton + self.toff)) < self.ton
        return OUT


class Toolbox(gui.VBox):
    process_view = None

    index_added_tool = 0

    def __init__(self, process_view, *args, **kwargs):
        gui.VBox.__init__(self, *args, **kwargs)
        self.process_view = process_view
        self.append(gui.Label("Toolbox", width="100%", height="auto", style={'outline':'1px solid black'}))

        self.container = gui.VBox(width="100%", height="auto", style={'outline':'1px solid black'})
        self.container.css_justify_content = 'flex-start'
        self.container.style['row-gap'] = '10px'
        self.append(self.container)

        self.css_justify_content = 'flex-start'

    def add_tool(self, tool_class):
        tool_class_widget = gui.Label(tool_class.__name__, style={'outline':'1px solid black'})
        tool_class_widget.tool_class = tool_class 
        tool_class_widget.onclick.do(self.on_tool_selected)
        tool_class_widget.style['cursor'] = 'pointer'
        self.container.append(tool_class_widget)

    def on_tool_selected(self, tool_class_widget):
        tool_class = tool_class_widget.tool_class
        tool_instance = tool_class(tool_class.__name__ , self.process_view)
        tool_instance.set_name(tool_instance.name + "_" + str(self.index_added_tool)) 
        self.index_added_tool += 1
        self.process_view.add_subprocess(tool_instance)


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
        self.main_container = gui.AsciiContainer(width=800, height=800, margin='0px auto')
        self.main_container.set_from_asciiart(
            """
            |toolbox|process_view               |
            """, 0, 0
        )

        self.process = ProcessView(width=600, height=600)
        self.toolbox = Toolbox(self.process)
        self.toolbox.add_tool(BOOL)
        self.toolbox.add_tool(NOT)
        self.toolbox.add_tool(AND)
        self.toolbox.add_tool(OR)
        self.toolbox.add_tool(XOR)
        self.toolbox.add_tool(PULSAR)
        self.toolbox.add_tool(STRING)
        self.toolbox.add_tool(STRING_SWAP_CASE)
        self.toolbox.add_tool(RISING_EDGE)
        
        self.main_container.append(self.toolbox, 'toolbox')
        self.main_container.append(self.process, 'process_view')
        
        """
        y = 10
        m = BOOL("BOOL", False, self.process, 100, y)
        self.process.add_subprocess(m)

        y += 110
        m = BOOL("BOOL 2", True, self.process, 100, y)
        self.process.add_subprocess(m)

        y += 110
        m = NOT("NOT 0", self.process, 100, y)
        self.process.add_subprocess(m)

        y += 110
        m = AND("AND", self.process, 100, y)
        self.process.add_subprocess(m)

        y += 110
        m = OR("OR", self.process, 100, y)
        self.process.add_subprocess(m)
        """

        # returning the root widget
        return self.main_container


    
if __name__ == "__main__":
    start(MyApp, debug=False, address='0.0.0.0', port=0, update_interval=0.01)
