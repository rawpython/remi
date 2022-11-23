import inspect

class Input():
    name = None
    default = None
    typ = None
    source = None #has to be an Output

    def __init__(self, name, default = inspect.Parameter.empty, typ = None):
        self.name = name
        self.default = default
        self.typ = typ

    def get_value(self):
        if not self.is_linked():
            return self.default
        return self.source.get_value()
    
    def has_default(self):
        return not (self.default == inspect.Parameter.empty)

    def link(self, output):
        self.source = output

    def is_linked(self):
        return self.source != None

    def unlink(self):
        Input.link(self, None)


class Output():
    name = None
    typ = None
    destinations = None #has to be an Input
    value = None

    def __init__(self, name, typ = None):
        self.name = name
        self.typ = typ
        self.destinations = []

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def link(self, destination):
        self.destinations.append(destination)

    def is_linked(self):
        return len(self.destinations) > 0

    def unlink(self, destination = None):
        if not destination is None:
            self.destinations.remove(destination)
            return
        self.destinations = []


class ObjectBlock():
    name = None
    FBs = None #this is the list of member functions

    def __init__(self, name):
        self.name = name
        self.FBs = {}


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
        self.destination = destination_widget

        self.source.destinaton = self.destination
        self.destination.source = self.source

    def unlink(self):
        self.source.unlink(self.destination)
        self.destination.unlink()


class Process():
    function_blocks = None
    object_blocks = None

    def __init__(self):
        self.function_blocks = {}
        self.object_blocks = {}

    def add_function_block(self, function_block):
        self.function_blocks[function_block.name] = function_block

    def add_object_block(self, object_block):
        self.object_blocks[object_block.name] = object_block

    def do(self):
        sub_function_blocks = []
        for object_block in self.object_blocks.values():
            for function_block in object_block.FBs.values():
                sub_function_blocks.append(function_block)

        for function_block in (*self.function_blocks.values(), *sub_function_blocks):
            parameters = {}
            all_inputs_connected = True

            for IN in function_block.inputs.values():
                if (not IN.is_linked()) and (not IN.has_default()):
                    all_inputs_connected = False
                    continue
                parameters[IN.name] = IN.get_value()
            
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

