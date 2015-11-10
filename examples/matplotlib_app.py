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
This simple example shows how to display a matplotlib plot image
"""


import remi.gui as gui
from remi import start, App
import io
import matplotlib.pyplot as plt


class MatplotImageProvider(gui.Widget):

    """MatplotImageProvider widget.
       This widget will not be added graphically
       We inherit Widget class in order to receive events
    """

    def __init__(self):
        super(MatplotImageProvider, self).__init__(0, 0)
        self.buf = None

    def set_plot(self, plt):
        if self.buf is not None:
            self.buf.close()
        self.buf = io.BytesIO()
        plt.savefig(self.buf, format='png')
        
    def get_address(self):
        return "/%s/serve_image" % id(self)

    def serve_image(self):
        self.buf.seek(0)
        headers = {'Content-type':'image/png'}
        return [self.buf.read(),headers]
        

class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        # the arguments are	width - height - layoutOrientationOrizontal
        wid = gui.Widget(320, 320, False, 10)
        
        matplot = MatplotImageProvider()
        plt.figure()
        plt.plot([1, 2])
        plt.title("test")
        matplot.set_plot(plt)
        
        self.image = gui.Image(300, 300, matplot.get_address())

        # appending a widget to another, the first argument is a string key
        wid.append('1', self.image)

        # returning the root widget
        return wid


if __name__ == "__main__":
	# setting up remi debug level 
	#       2=all debug messages   1=error messages   0=no messages
	#import remi.server
	#remi.server.DEBUG_MODE = 2 

	# starts the webserver
	# optional parameters   
	#       start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp)
