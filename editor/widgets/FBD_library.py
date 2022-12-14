
from . import FBD_view
from . import FBD_model
import remi
import remi.gui as gui
import time
import inspect
import types


class FBWrapper(FBD_view.FunctionBlockView):
    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Variable name of the object to be wrapped''', str, {})
    def obj_variable_name(self): 
        return self._obj_variable_name
    @obj_variable_name.setter
    def obj_variable_name(self, value): 
        self.update_io_interface()
        self._obj_variable_name = value

    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Method name of the object to be wrapped''', str, {})
    def method_name(self): 
        return self._method_name
    @method_name.setter
    def method_name(self, value): 
        self.update_io_interface()
        self._method_name = value

    _obj_variable_name = None
    _method_name = None
    method_bound = None

    def __init__(self, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, *args, **kwargs)
        
    @FBD_model.FunctionBlock.decorate_process([])
    def do(self, *args, **kwargs):
        if self.method_bound == None:
            self.update_io_interface()
            if self.method_bound == None:
                return

        #populate outputs
        results = self.method_bound(*args, **kwargs)
        results_count = 0        
        if not results is None: 
            if type(results) in [tuple,]:
                results_count = len(results)
            else:
                results_count = 1
        
        if results_count != len(self.outputs):
            for k in list(self.outputs.keys()):
                self.remove_output_widget(k)
            if results_count == 1:
                self.add_io_widget(FBD_view.OutputView(f"out:{str(type(results))}"))
            if results_count > 1:
                i = 0
                for res in results:
                    self.add_io_widget(FBD_view.OutputView(f"out:{str(type(res))}{i}"))
                    i += 1
            for OUT in self.outputs.values():
                OUT.onmousedown.do(self.get_parent().onselection_start, js_stop_propagation=True, js_prevent_default=True)
                OUT.onmouseup.do(self.get_parent().onselection_end, js_stop_propagation=True, js_prevent_default=True)
                
        return results

    def update_io_interface(self):
        for k in list(self.inputs.keys()):
            self.remove_input_widget(k)
        for k in list(self.outputs.keys()):
            self.remove_output_widget(k)
        
        if self._obj_variable_name == None:
            return
        if self._method_name == None:
            return
        app_instance = self.search_app_instance(self.get_parent())
        obj = self.select_instance(app_instance.root, self._obj_variable_name)
        self.method_bound = getattr(obj, self._method_name)
        signature = inspect.signature(self.method_bound)
        for arg in signature.parameters:
            self.add_io_widget(FBD_view.InputView(arg, default = signature.parameters[arg].default))

        for IN in self.inputs.values():
            IN.onmousedown.do(self.get_parent().onselection_start, js_stop_propagation=True, js_prevent_default=True)
            IN.onmouseup.do(self.get_parent().onselection_end, js_stop_propagation=True, js_prevent_default=True)

    def search_app_instance(self, node):
        if issubclass(node.__class__, remi.server.App):
            return node
        if not hasattr(node, "get_parent"):
            return None
        return self.search_app_instance(node.get_parent())

    def select_instance(self, node, variable_name):
        if not hasattr(node, 'attributes'):
            return None

        if node.variable_name == variable_name:
            return node

        for item in node.children.values():
            res = self.select_instance(item, variable_name)
            if not res is None:
                return res


def FBWrapObjectMethod(obj_name, method_bound):
    fb = FBD_view.FunctionBlockView()
    #if hasattr(self.do, "_outputs"):
    #for o in self.do._outputs:
    #    self.add_io_widget(OutputView(o))

    signature = inspect.signature(method_bound)
    for arg in signature.parameters:
        fb.add_io_widget(FBD_view.InputView(arg, default = signature.parameters[arg].default))

    def do(*args, **kwargs):
        return method_bound(*args, **kwargs)
        
    def pre_do(*args, **kwargs):
        #populate outputs
        results = method_bound(*args, **kwargs)
        for k in list(fb.outputs.keys()):
            fb.remove_output_widget(k)
        if not results is None: 
            if type(results) in [tuple,]:
                i = 0
                for res in results:
                    fb.add_io_widget(FBD_view.OutputView(f"out{i}"))
                    i += 1
            else:
                fb.add_io_widget(FBD_view.OutputView("out"))
        fb.do = do

    fb.do = pre_do
    return fb


class SUM(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['RESULT',])
    def do(self, IN1, IN2):
        return IN1 + IN2

class MUL(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['RESULT',])
    def do(self, IN1, IN2):
        return IN1 * IN2

class DIV(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['RESULT',])
    def do(self, IN1, IN2):
        return IN1 / IN2

class DIFFERENCE(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['RESULT',])
    def do(self, IN1, IN2):
        return IN1 - IN2

class COUNTER(FBD_view.FunctionBlockView):
    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Defines the actual value''', int, {'possible_values': '', 'min': 0, 'max': 0xffffffff, 'default': 1, 'step': 1})
    def value(self): 
        if len(self.outputs) < 1:
            return 0
        return self.outputs['OUT'].get_value()
    @value.setter
    def value(self, value): self.outputs['OUT'].set_value(value)

    def __init__(self, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, *args, **kwargs)
        self.outputs['OUT'].set_value(0)

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, reset=False):
        if reset:
            self.value = 0
            return 0
        self.value += 1
        return self.value

class INT(FBD_view.FunctionBlockView):
    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Defines the actual value''', int, {'possible_values': '', 'min': 0, 'max': 0xffffffff, 'default': 1, 'step': 1})
    def value(self): 
        if len(self.outputs) < 1:
            return False
        return self.outputs['OUT'].get_value()
    @value.setter
    def value(self, value): self.outputs['OUT'].set_value(value)

    def __init__(self, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, *args, **kwargs)
        self.outputs['OUT'].set_value(False)

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        OUT = self.outputs['OUT'].get_value()
        return OUT

class GREATER_THAN(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['RESULT',])
    def do(self, IN1, IN2):
        return IN1 > IN2

class LESS_THAN(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['RESULT',])
    def do(self, IN1, IN2):
        return IN1 < IN2

class EQUAL_TO(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['RESULT',])
    def do(self, IN1, IN2):
        return IN1 == IN2

class PRINT(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process([])
    def do(self, IN):
        print(IN)

class NONE(FBD_view.FunctionBlockView):
    def __init__(self, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, *args, **kwargs)

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        return None

class STRING(FBD_view.FunctionBlockView):
    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Defines the actual value''', str, {})
    def value(self): 
        if len(self.outputs) < 1:
            return ""
        return self.outputs['OUT'].get_value()
    @value.setter
    def value(self, value): self.outputs['OUT'].set_value(value)

    def __init__(self, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, *args, **kwargs)
        self.outputs['OUT'].set_value("A STRING VALUE")

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        OUT = self.outputs['OUT'].get_value()
        return OUT

class STRING_SWAP_CASE(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, IN, EN = True):
        if not EN:
            return
        OUT = IN.swapcase()
        return OUT

class BOOL(FBD_view.FunctionBlockView):
    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Defines the actual value''', bool, {})
    def value(self): 
        if len(self.outputs) < 1:
            return False
        return self.outputs['OUT'].get_value()
    @value.setter
    def value(self, value): self.outputs['OUT'].set_value(value)

    def __init__(self, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, *args, **kwargs)
        self.outputs['OUT'].set_value(False)

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        OUT = self.outputs['OUT'].get_value()
        return OUT

class RISING_EDGE(FBD_view.FunctionBlockView):
    previous_value = None

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, IN):
        OUT = (self.previous_value != IN) and IN
        self.previous_value = IN
        return OUT

class FALLING_EDGE(FBD_view.FunctionBlockView):
    previous_value = None

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, IN):
        OUT = (self.previous_value != IN) and not IN
        self.previous_value = IN
        return OUT

class NOT(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, IN):
        OUT = not IN
        return OUT

class AND(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, IN1, IN2):
        OUT = IN1 and IN2
        return OUT

class OR(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, IN1, IN2):
        OUT = IN1 or IN2
        return OUT

class XOR(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self, IN1, IN2):
        OUT = IN1 != IN2
        return OUT

class PULSAR(FBD_view.FunctionBlockView):
    _ton = 1000
    _toff = 1000

    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Defines the actual TON value''', int, {'possible_values': '', 'min': 0, 'max': 65535, 'default': 0, 'step': 1})
    def ton(self): 
        return self._ton
    @ton.setter
    def ton(self, value): self._ton = value

    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Defines the actual TOFF value''', int, {'possible_values': '', 'min': 0, 'max': 65535, 'default': 0, 'step': 1})
    def toff(self): 
        return self._toff
    @toff.setter
    def toff(self, value): self._toff = value

    tstart = 0
    def __init__(self, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, *args, **kwargs)
        self.outputs['OUT'].set_value(False)
        self.tstart = time.time()

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        OUT = (int((time.time() - self.tstart)*1000) % (self.ton + self.toff)) < self.ton
        return OUT

