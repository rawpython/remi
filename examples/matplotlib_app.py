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

import io

import remi.gui as gui
from remi import start, App

import matplotlib.pyplot as plt

class MatplotImageProvider(gui.Widget):

    """MatplotImageProvider widget.
       This widget will not be added graphically
       We inherit Widget class in order to receive events
    """

    ax = None

    def __init__(self, fig=None, ax=None):
        super(MatplotImageProvider, self).__init__(0, 0)
        self._buf = None
        if fig is None:
            fig,ax = plt.subplots()
        self._fig = fig
        self.ax = ax

    def redraw(self):
        if self._buf is not None:
            self._buf.close()
        self._buf = io.BytesIO()
        self._fig.savefig(self._buf, format='png')
        
    def get_address(self):
        return "/%s/serve_image" % id(self)

    def serve_image(self):
        if self._buf is None:
            self.redraw()
        self._buf.seek(0)
        headers = {'Content-type':'image/png'}
        return [self._buf.read(),headers]
        

class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):

        wid = gui.Widget(320, 320, False, 10)

        mpl = MatplotImageProvider()
        mpl.ax.plot([1, 2])
        mpl.ax.set_title("test")
        
        self.image = gui.Image(300, 300, mpl.get_address())

        # appending a widget to another, the first argument is a string key
        wid.append('1', self.image)

        # returning the root widget
        return wid


if __name__ == "__main__":
    start(MyApp)

