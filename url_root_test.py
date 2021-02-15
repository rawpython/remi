
import sys
sys.path=["/home/francois/Documents/Micro-entreprise/projets/chute_blocs/dev_tests/remi_rootdir/remi"]+sys.path

from remi import server,gui
gui.url_root="/foo"

from remi import start, App


############################## BEGIN REMI TWEAKS ###############################


############################## END REMI TWEAKS   ###############################


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(
            *args,
            url_root=gui.url_root,
            static_file_path={"res2":"/home/francois/Documents/Micro-entreprise/projets/chute_blocs/PlatRock-WebUI/platrock_webui/res"}
        )

    def main(self):
        #creating a container VBox type, vertical
        wid = gui.VBox(width=300, height=200)

        #creating a text label, "white-space":"pre" preserves newline
        self.lbl = gui.Label('Hello\n test', width='80%', height='50%', style={"white-space":"pre"})

        #a button for simple interaction
        bt = gui.Button('Press me!', width=200, height=30)

        #setting up the listener for the click event
        bt.onclick.do(self.on_button_pressed)
        
        #adding the widgets to the main container
        wid.append(self.lbl)
        wid.append(bt)
        wid.append(gui.Image("/res:folder.png"))
        # returning the root widget
        self.page.children["head"].set_icon_file("/res:folder.png")
        return wid

    # listener function
    def on_button_pressed(self, emitter):
        self.lbl.set_text('Hello World!')
        

if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True, address='0.0.0.0', port=8080, start_browser=False)
