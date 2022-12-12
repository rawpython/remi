import inspect


class Linkable():
    """ This class represents a Linkable object
            an object that can be connected to 'linked_nodes_max_count' other elements
    """
    name = None
    linked_nodes = None
    linked_nodes_max_count = 0

    def __init__(self, name, linked_nodes_max_count = 1, *args, **kwargs):
        """Args:
            name (str): the object string identifier.
            linked_nodes_max_count: the maximum number of nodes that can link to.
        """
        
        self.name = name
        self.linked_nodes_max_count = linked_nodes_max_count
        self.linked_nodes = []

    def link(self, node):
        """Creates a new link.

        Args:
            node (Linkable): The node to link to.
        """
        if not self.is_linked_to(node):
            if self.linked_nodes_max_count > len(self.linked_nodes):
                self.linked_nodes.append(node)
                return True

        return False

    def is_linked(self):
        """Check whether this object is linked to something.

        Returns:
            result (bool): If the node is linked to something.
        """
        return len(self.linked_nodes) > 0

    def is_linked_to(self, node):
        """Check whether this object is linked to the given node.

        Args:
            node (Linkable): The node to be checked if linked to.
        
        Returns:
            result (bool): If this node is linked to the given node.
        """
        return node in self.linked_nodes

    def unlink(self, node = None):
        """Removes a link to a specific node.
            If the given node is null, removes all the links.

        Args:
            node (Linkable): The node to be unlinked. None to remove all links. 
        """
        if node is None:
            self.linked_nodes = []
            return
        self.linked_nodes.remove(node)


class Input(Linkable):
    """An input element of a FunctionBlock.
    """
    default = None
    typ = None
    
    def __init__(self, name, default = inspect.Parameter.empty, typ = None):
        """Args:
            name (str): The name of the input. 
            default (any): The default value of the input.
            type (type): The input type.
        """
        Linkable.__init__(self, name, linked_nodes_max_count=1)
        self.default = default
        self.typ = typ

    def get_value(self):
        """Returns the input value.
        The value is the default one if the Input is not linked, 
            or the value given from the link.

        Returns:
            result (any): The input value.
        """
        if not self.is_linked():
            return self.default
        return self.linked_nodes[0].get_value()
    
    def has_default(self):
        """Returns whether there is a default value.
            
        Returns:
            result (bool): True if this input has a default value.
        """
        return not (self.default == inspect.Parameter.empty)


class Output(Linkable):
    """An output value of a FunctionBlock
    """
    name = None
    typ = None
    value = None

    def __init__(self, name, typ = None):
        """Args:
            name (str): The name of the output. 
            type (type): The output type.
        """
        Linkable.__init__(self, name, linked_nodes_max_count=0xff)
        self.name = name
        self.typ = typ

    def get_value(self):
        """Returns the output value.
        The value given from the FunctionBlock processing.

        Returns:
            result (any): The output value.
        """
        return self.value

    def set_value(self, value):
        """Sets the output value.
        
        Args:
            value (any): the value to be assigned.
        """
        self.value = value


class FunctionBlock():
    """A FunctionBlock represents a processing unit with its own logic.
    The function block must implement the 'do' method that executes the algorithm.
    A function block has N inputs, that are the parameters of the 'do' method,
        and M outputs that are the result values of the 'do' method.
    A function block can have an enabling input to enable or disable the logic exection.
    A function block gets executed among the others, in the order given by the execution_priority member.
    """
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

    def __init__(self, execution_priority = 0):
        """Args:
            execution_priority (int): the order number.
        """
        self.set_execution_priority(execution_priority)
        self.inputs = {}
        self.outputs = {}

    def set_execution_priority(self, execution_priority):
        """Sets the execution order.

        Args:
            execution_priority (int): The priority value.
        """
        self.execution_priority = execution_priority

    def add_io(self, io):
        """Adds an Input or Output to the function block.

        Args:
            io (Input/Output): The io instance.
        """
        if issubclass(type(io), Input):
            self.inputs[io.name] = io
        else:
            self.outputs[io.name] = io

    def add_enabling_input(self):
        """Adds an enabling input.
        """
        self.add_io(Input('EN', False))

    def remove_enabling_input(self):
        """Removes the enabling input and the eventual link.
        """
        self.inputs['EN'].unlink()
        del self.inputs['EN']

    @decorate_process([])
    def do(self):
        """Implements the FunctionBlock logic.
        Inputs are passed to this function as parameters by the Process.
        Results are assigned to the Outputs by the Process.

        Returns:
            result (any): The result value.
        """
        return None


class Link():
    """Represents the link between two Linkable nodes.
    """
    source = None
    destination = None
    def __init__(self, source_widget, destination_widget):
        """Args:
            source_widget (Linkable): a node participating to the link.
            destination_widget (Linkable): a node participating to the link.
        """
        self.source = source_widget
        self.destination = destination_widget

    def unlink(self):
        """Deletes the link.
        """
        self.source.unlink(self.destination)
        self.destination.unlink()


class Process():
    """A Process is a collection of FunctionBlocks in which I/O are linked.
    FunctionBlocks in a Process gets executed sequentially in the order given by the FunctionBlock priority.
    The priority takes places by the order of function_blocks in the dictionary. 
    Such order can be adjusted by reordering elements in the dictionary.
    """
    function_blocks = None

    def __init__(self):
        self.function_blocks = {}

    def add_function_block(self, function_block):
        """Adds a function block to the process.

        Args:
            function_block (FunctionBlock): the function block to be added.
        """
        self.function_blocks[function_block.identifier] = function_block
    
    def remove_function_block(self, function_block):
        """Removes a function block from the process.
        
        Args:
            function_block (FunctionBlock): the function block to be removed.
        """
        del self.function_blocks[function_block.identifier]

    def do(self):
        """Executed the FunctionBlocks.
        Before to call a function block, all its Inputs are gethered by the linked outputs.
            If the input is not linked, the corresponding parameter takes the default value, whether available.
        The function block gets executed if all the parameters are available.
        Once the function block is executed, the results are assigned to its Outputs.
        """
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

