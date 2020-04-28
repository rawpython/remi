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

import remi.gui as gui
from remi import start, App


class RemoteLabel(gui.Label):
    def __init__(self, text, **kwargs):
        super(RemoteLabel, self).__init__(text, **kwargs)

    # api function
    def api_set_text(self, value1, value2):
        self.set_text('parameters: %s - %s' % (value1, value2))
        headers = {'Content-type': 'text/plain'}
        return ['OK', headers]


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        wid = gui.VBox()

        # the 'id' param allows to have an alias in the url to refer to the widget that will manage the call
        self.lbl = RemoteLabel(
            'type in other page url "http://127.0.0.1:8082/label/api_set_text?value1=text1&value2=text2" !',
            width='80%', height='50%', attributes={'id': 'label'})
        self.lbl.style['margin'] = 'auto'

        # appending a widget to another, the first argument is a string key
        wid.append(self.lbl)

        # returning the root widget
        return wid


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1,
    # start_browser=True)
    start(MyApp, debug=True, address='127.0.0.1', port=8082)
