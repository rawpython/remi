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

import time
import io

import cv2
import remi.gui as gui
from remi import start, App


class OpencvVideoWidget(gui.Image):
    def __init__(self, video_source=0, fps=5, **kwargs):
        super(OpencvVideoWidget, self).__init__("/%s/get_image_data" % id(self), **kwargs)
        self.fps = fps
        self.capture = cv2.VideoCapture(video_source)

        javascript_code = gui.Tag()
        javascript_code.type = 'script'
        javascript_code.attributes['type'] = 'text/javascript'
        javascript_code.add_child('code', """
            function update_image%(id)s(){
                if(document.getElementById('%(id)s').getAttribute('play')=='False')
                    return;

                var url = '/%(id)s/get_image_data';
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url, true);
                xhr.responseType = 'blob'
                xhr.onload = function(e){
                    var urlCreator = window.URL || window.webkitURL;
                    var imageUrl = urlCreator.createObjectURL(this.response);
                    document.getElementById('%(id)s').src = imageUrl;
                }
                xhr.send();
            };

            setInterval( update_image%(id)s, %(update_rate)s );
            """ % {'id': id(self), 'update_rate': 1000.0 / self.fps})

        self.add_child('javascript_code', javascript_code)
        self.play()

    def play(self):
        self.attributes['play'] = True

    def stop(self):
        self.attributes['play'] = False

    def get_image_data(self):
        ret, frame = self.capture.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                headers = {'Content-type': 'image/jpeg'}
                # tostring is an alias to tobytes, which wasn't added till numpy 1.9
                return [jpeg.tostring(), headers]
        return None, None


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        # the arguments are	width - height - layoutOrientationOrizontal
        wid = gui.Widget(width=640, height=600)
        self.opencvideo_widget = OpencvVideoWidget(0, 10, width=620, height=530)
        self.opencvideo_widget.style['margin'] = '10px'
        menu = gui.Menu(width=620, height=30)
        m1 = gui.MenuItem('Video', width=100, height=30)
        m11 = gui.MenuItem('Play', width=100, height=30)
        m12 = gui.MenuItem('Stop', width=100, height=30)
        m11.set_on_click_listener(self, 'menu_play_clicked')
        m12.set_on_click_listener(self, 'menu_stop_clicked')

        menu.append(m1)
        m1.append(m11)
        m1.append(m12)

        wid.append(menu)
        wid.append(self.opencvideo_widget)

        # returning the root widget
        return wid

    def menu_play_clicked(self):
        self.opencvideo_widget.play()

    def menu_stop_clicked(self):
        self.opencvideo_widget.stop()


if __name__ == "__main__":
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp)
