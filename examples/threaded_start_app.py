"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

"""
    This example shows how to start the application as a thread, 
     without stopping the main thread.
    A label is accessed from the main thread. 
    NOTE:
        It is important to run the server with parameter multiple_instance=False
"""

import remi
import remi.gui as gui
from remi import App
import time

# here will be stored the application instance once a client connects to.
global_app_instance = None


class MyApp(App):
    label = None

    def main(self):
        global global_app_instance
        global_app_instance = self

        # creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width=300, height=200, style={"margin": "0px auto"})
        self.label = gui.Label("a label")

        main_container.append(self.label)

        # returning the root widget
        return main_container


if __name__ == "__main__":
    # create the server with parameter start=False to prevent server autostart
    server = remi.Server(
        MyApp,
        start=False,
        address="0.0.0.0",
        port=0,
        start_browser=True,
        multiple_instance=False,
    )
    # start the server programmatically
    server.start()

    index = 0
    # loop the main thread
    while True:
        # checks that the app instance is created
        if global_app_instance is not None:
            # the update lock is important to sync the app thread
            with global_app_instance.update_lock:
                # set the label value
                global_app_instance.label.set_text("%s" % index)
                index = index + 1
        time.sleep(1)
