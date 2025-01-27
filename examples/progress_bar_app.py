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


class MyApp(App):

    def main(self):
        # creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.VBox(width=300, height=200, style={'margin': '0px auto'})

        # creating a progress bar and appending it to the main layout
        self.progress = gui.Progress(0,100)
        main_container.append(self.progress)

        # creating the file uploader
        self.file_uploader = gui.FileUploader()
        main_container.append(self.file_uploader)

        # linking events 
        self.file_uploader.onprogress.do(self.onprogress_listener)
        self.file_uploader.onsuccess.do(self.fileupload_on_success)
        
        # returning the root widget
        return main_container
    
    def onprogress_listener(self, emitter, filename, loaded, total):
        self.progress.set_value(loaded*100.0/total)
        print(filename, loaded, total)

    def fileupload_on_success(self, emitter, filename):
        print('File upload success: ' + filename)


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='0.0.0.0', port=0, start_browser=True, username=None, password=None)
