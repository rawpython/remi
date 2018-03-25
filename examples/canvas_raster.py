#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

import os
import remi.gui as gui
from remi.game import Color, Rect
from remi.game.canvas import Canvas
from remi.game.raster import load_image, draw
from remi import start, App


class MyApp(App):
    canvas = None
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        #margin 0px auto allows to center the app to the screen
        container = gui.Widget(width=600, height=600)
        self.canvas = Canvas(self, resolution=(600, 400), margin='0px auto')
        button = gui.Button('Go!')
        button.set_on_click_listener(self.draw)
        container.append(self.canvas)
        container.append(button)
        # returning the root widget
        return container

    def draw(self, widget):
        image = load_image('example.png')
        draw(image, self.canvas, position=(10, 10))
        
if __name__ == "__main__":
    print 'Starting with pid: %s' % os.getpid()
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True)
