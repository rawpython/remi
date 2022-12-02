
import FBD_view
import FBD_model
import remi
import remi.gui as gui
import time
import inspect
import types


class PRINT(FBD_view.FunctionBlockView):
    @FBD_model.FunctionBlock.decorate_process([])
    def do(self, IN):
        print(IN)

class STRING(FBD_view.FunctionBlockView):
    @property
    @gui.editor_attribute_decorator("WidgetSpecific",'''Defines the actual value''', str, {})
    def value(self): 
        if len(self.outputs) < 1:
            return ""
        return self.outputs['OUT'].get_value()
    @value.setter
    def value(self, value): self.outputs['OUT'].set_value(value)

    def __init__(self, name, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, name, *args, **kwargs)
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

    def __init__(self, name, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, name, *args, **kwargs)
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
    def __init__(self, name, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, name, *args, **kwargs)
        self.outputs['OUT'].set_value(False)
        self.tstart = time.time()

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        OUT = (int((time.time() - self.tstart)*1000) % (self.ton + self.toff)) < self.ton
        return OUT

