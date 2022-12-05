import inspect


class Linkable():
    name = None
    linked_nodes = None
    linked_nodes_max_count = 0

    def __init__(self, name, linked_nodes_max_count = 1, *args, **kwargs):
        self.name = name
        self.linked_nodes_max_count = linked_nodes_max_count
        self.linked_nodes = []

    def link(self, node):
        if not self.is_linked_to(node):
            if self.linked_nodes_max_count > len(self.linked_nodes):
                self.linked_nodes.append(node)
                return True

        return False

    def is_linked(self):
        return len(self.linked_nodes) > 0

    def is_linked_to(self, node):
        return node in self.linked_nodes

    def unlink(self, node = None):
        if node is None:
            self.linked_nodes = []
            return
        self.linked_nodes.remove(node)


class Input(Linkable):
    default = None
    typ = None
    
    def __init__(self, name, default = inspect.Parameter.empty, typ = None):
        Linkable.__init__(self, name, linked_nodes_max_count=1)
        self.default = default
        self.typ = typ

    def get_value(self):
        if not self.is_linked():
            return self.default
        return self.linked_nodes[0].get_value()
    
    def has_default(self):
        return not (self.default == inspect.Parameter.empty)


class Output(Linkable):
    name = None
    typ = None
    value = None

    def __init__(self, name, typ = None):
        Linkable.__init__(self, name, linked_nodes_max_count=0xff)
        self.name = name
        self.typ = typ

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class FunctionBlock():
    name = None
    inputs = None
    outputs = None

    execution_priority = 0

    has_enabling_input = False #This property gets overloaded in FBD_view.FunctionBlockView

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

    def __init__(self, name, execution_priority = 0):
        self.name = name
        self.set_execution_priority(execution_priority)
        self.inputs = {}
        self.outputs = {}

    def set_execution_priority(self, execution_priority):
        self.execution_priority = execution_priority

    def add_io(self, io):
        if issubclass(type(io), Input):
            self.inputs[io.name] = io
        else:
            self.outputs[io.name] = io

    def add_enabling_input(self):
        self.add_io(Input('EN', False))

    def remove_enabling_input(self):
        self.inputs['EN'].unlink()
        del self.inputs['EN']

    @decorate_process([])
    def do(self):
        return None


class Link():
    source = None
    destination = None
    def __init__(self, source_widget, destination_widget):
        self.source = source_widget
        self.destination = destination_widget

    def unlink(self):
        self.source.unlink(self.destination)
        self.destination.unlink()


class Process():
    function_blocks = None

    def __init__(self):
        self.function_blocks = {}

    def add_function_block(self, function_block):
        self.function_blocks[function_block.name] = function_block
    
    def remove_function_block(self, function_block):
        del self.function_blocks[function_block.name]

    def do(self):
        execution_priority = 0
        for function_block in self.function_blocks.values():
            parameters = {}
            all_inputs_connected = True

            function_block.set_execution_priority(execution_priority)
            execution_priority += 1

            for IN in function_block.inputs.values():
                if (not IN.is_linked()) and (not IN.has_default()):
                    all_inputs_connected = False
                    continue
                parameters[IN.name] = IN.get_value()
            
            if not all_inputs_connected:
                continue

            if function_block.has_enabling_input:
                if not parameters['EN']:
                    continue
                else:
                    del parameters['EN']

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

