
import FBD_view
import FBD_model
import remi
import remi.gui as gui
import time

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
        FBD_view.FunctionBlockViewFunctionBlockView.__init__(self, name, *args, **kwargs)
        self.outputs['OUT'].set_value("A STRING VALUE")

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        OUT = self.outputs['OUT'].get_value()
        return OUT

class STRING_SWAP_CASE(FBD_view.FunctionBlockView):
    def __init__(self, name, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, name, *args, **kwargs)

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
    ton = 1000
    toff = 1000
    tstart = 0
    def __init__(self, name, *args, **kwargs):
        FBD_view.FunctionBlockView.__init__(self, name, *args, **kwargs)
        self.outputs['OUT'].set_value(False)
        self.tstart = time.time()

    @FBD_model.FunctionBlock.decorate_process(['OUT'])
    def do(self):
        OUT = (int((time.time() - self.tstart)*1000) % (self.ton + self.toff)) < self.ton
        return OUT

