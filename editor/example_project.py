import remi.gui as gui
from remi import start, App

class example_project(App):
    def __init__(self, *args):
        super(example_project, self).__init__(*args)

    @staticmethod
    def main(self, name='world'):
        # the arguments are	width - height - layoutOrientationOrizontal
        mainContainer = gui.Widget(120, 100, False, 10)
        mainContainer.attributes['editor_varname'] = "mainContainer"
        mainContainer.attributes['editor_newclass'] = "True"
        mainContainer.attributes['editor_constructor'] = "(120, 100, False, 10)"
        wid = gui.Widget(120, 100, False, 10)
        wid.attributes['editor_varname'] = "wid"
        wid.attributes['editor_newclass'] = "True"
        wid.attributes['editor_constructor'] = "(120, 100, False, 10)"
        self.lbl = gui.Label(100, 30, 'Hello %s!' % name)
        self.lbl.attributes['editor_varname'] = "lbl"
        self.lbl.attributes['editor_newclass'] = "False"
        self.lbl.attributes['editor_constructor'] = "(100, 30, 'Hello %s!' % name)"
        self.bt = gui.Button(100, 30, 'Press me!')
        self.bt.attributes['editor_varname'] = "bt"
        self.bt.attributes['editor_newclass'] = "False"
        self.bt.attributes['editor_constructor'] = "(100, 30, 'Press me!')"
        
        self.bt.set_on_click_listener(self, 'on_button_pressed')
        self.bt.set_on_contextmenu_listener(self, 'asd')
        # appending a widget to another, the first argument is a string key
        wid.append(self.lbl)
        wid.append(self.bt)
        mainContainer.append(wid)
        # returning the root widget
        return mainContainer

    # listener function
    def on_button_pressed(self):
        self.lbl.set_text('Button pressed')
        self.bt.set_text('Hi!')


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(example_project,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(example_project, debug=False)