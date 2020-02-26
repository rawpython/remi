#main program code prototype
proto_code_program = """
# -*- coding: utf-8 -*-

%(imports)s
from remi import start, App

%(code_classes)s

#Configuration
configuration = %(configuration)s

if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(%(classname)s, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
"""

#typical widget class prototype
proto_code_class = """
class %(classname)s( %(superclassname)s ):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( %(classname)s, self ).__init__(*args, **kwargs)
        %(nested_code)s
"""

#function prototype
proto_code_function = "    def %(funcname)s%(parameters)s:\n        pass\n\n"

#here the prototype of the main class
proto_code_main_class = """
class %(classname)s(App):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            super(%(classname)s, self).__init__(*args, static_file_path={'my_res':'%(config_resourcepath)s'})

    def idle(self):
        #idle function called every update cycle
        pass
    
    def main(self):
        return %(classname)s.construct_ui(self)
        
    @staticmethod
    def construct_ui(self):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        %(code_nested)s

        self.%(mainwidgetname)s = %(mainwidgetname)s
        return self.%(mainwidgetname)s
    
"""

proto_export_app_template = """
import core.globals
import remi        # This doesn't work with files from remi
from remi.gui import *
from remi import start, App

class %(classname)s( %(superclassname)s ):
# The name of the class has to be identical with the name of the file (view_template.py), but with capital first letter!
# Files which have a Underscore at first place in filename will not be loaded (by renaming you can take them out for development easily).

    def __init__(self, AppInst=None, *args, **kwargs):

        super().__init__(*args, **kwargs)       # Initializes the Parent Object remi.gui.Container
        self.AppInst = AppInst                  # Holds the Instance of the App. We need it to access uiControl
        self.shownInMenu = 'My Example Menu'          # Use None if it should not be visible in any Menu
        self.menuTitle = 'from REMI Editor container rel'
        self.style.update({'width': '100%%', 'margin': 'auto', 'border': '1px solid black', 'padding': '10px', 'margin-top': '20px'})
        self.append(self.constructUI())
        self.registerEventHandlers()

    def constructUI(self):

        %(nested_code)s

    def registerEventHandlers(self):
        %(events_registration)s

    def updateView(self):
        # Here you can update the view if it needs updates
        pass
"""

proto_widget_allocation = "%(varname)s = %(classname)s()\n        "

proto_attribute_setup = """%(varname)s.attributes.update({%(attr_dict)s})\n        """

proto_property_setup = """%(varname)s.%(property)s = %(value)s\n        """

proto_style_setup = """%(varname)s.style.update({%(style_dict)s})\n        """

proto_layout_append = "%(parentname)s.append(%(varname)s)\n        "

proto_set_listener = "%(sourcename)s.%(register_function)s.do(%(listenername)s.%(listener_function)s)\n        "
