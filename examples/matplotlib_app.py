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
import time
import threading
import random

import remi.gui as gui
from remi import start, App

import matplotlib.pyplot as plt


class MatplotImage(gui.Image):

    ax = None

    def __init__(self, width, height, fig=None, ax=None):
        super(MatplotImage, self).__init__(width, height, "/%s/get_image_data?update_index=0" % id(self))
        self._buf = None
        self._buflock = threading.Lock()

        if fig is None:
            fig,ax = plt.subplots()
        self._fig = fig
        self.ax = ax

        self.redraw()

    def redraw(self):
        buf = io.BytesIO()
        self._fig.savefig(buf, format='png')
        with self._buflock:
            if self._buf is not None:
                self._buf.close()
            self._buf = buf

        i = int(time.time()*1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self),i)

        super(MatplotImage, self).redraw()

    def get_image_data(self,update_index):
        with self._buflock:
            if self._buf is None:
                return None
            self._buf.seek(0)
            data = self._buf.read()

        return [data, {'Content-type':'image/png'}]


class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):

        wid = gui.Widget(320, 320, False, 10)

        bt = gui.Button(100, 30, 'Data')
        bt.set_on_click_listener(self, 'on_button_pressed')

        self.plot_data = [0,1]
        self.mpl = MatplotImage(250,250)
        self.mpl.ax.set_title("test")
        self.mpl.ax.plot(self.plot_data)
        self.mpl.redraw()

        # appending a widget to another, the first argument is a string key
        wid.append('1', bt)
        wid.append('2', self.mpl)

        return wid

    def on_button_pressed(self):
        self.plot_data.append(random.random())
        self.mpl.ax.plot(self.plot_data)
        self.mpl.redraw()

if __name__ == "__main__":
    start(MyApp, debug=True)

