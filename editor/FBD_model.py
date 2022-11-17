import inspect

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

    def unlink(self):
        self.link(None)


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

    def unlink(self):
        self.link(None)


class FunctionBlock():
    name = None
    inputs = None
    outputs = None

    def decorate_process(output_list):
        """ setup a method as a process FunctionBlock """
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


class Link():
    source = None
    destination = None
    def __init__(self, source_widget, destination_widget):
        self.source = source_widget
        self.source.onpositionchanged.do(self.update_path)
        self.destination = destination_widget
        self.destination.onpositionchanged.do(self.update_path)

        self.source.destinaton = self.destination
        self.destination.source = self.source
        self.update_path()

    def unlink(self):
        self.get_parent().remove_child(self.unlink_bt)
        self.get_parent().remove_child(self)


class Process():
    function_blocks = None
    def __init__(self):
        self.function_blocks = {}

    def add_function_block(self, function_block):
        self.function_blocks[function_block.name] = function_block

    def do(self):
        for function_block in self.function_blocks.values():
            parameters = {}
            all_inputs_connected = True

            function_block_default_inputs = inspect.signature(function_block.do).parameters
            
            for IN in function_block.inputs.values():
                if (not IN.is_linked()) and function_block_default_inputs[IN.name].default == inspect.Parameter.empty:
                    all_inputs_connected = False
                    continue
                parameters[IN.name] = IN.get_value() if IN.is_linked() else function_block_default_inputs[IN.name].default
            
            if not all_inputs_connected:
                continue
            output_results = function_block.do(**parameters)
            if output_results is None:
                continue
            i = 0
            for OUT in function_block.outputs.values():
                if type(output_results) in (tuple, list):
                    OUT.set_value(output_results[i])
                else:
                    OUT.set_value(output_results)
                i += 1
