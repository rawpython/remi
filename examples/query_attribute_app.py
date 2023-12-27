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
        self.main_container = gui.Widget(
            width="50%", height=200, style={"margin": "0px auto"}
        )

        # returning the root widget
        return self.main_container

    def onpageshow(self, emitter, width, height):
        """WebPage Event that occurs on webpage gets shown"""
        super(MyApp, self).onpageshow(emitter, width, height)

        attribute_list = [
            "id",
            "title",
            "getBoundingClientRect().width",
            "getBoundingClientRect().top",
        ]
        style_property_list = ["width", "height"]

        # If a style property name is identical to an attribute name, call the query function twice
        # properly specifing the result listener.
        self.main_container.onquery_client_result.do(
            lambda emitter, kwargs: print(str(kwargs))
        )
        self.main_container.query_client(self, attribute_list, style_property_list)


if __name__ == "__main__":
    # starts the webserver
    start(
        MyApp,
        address="0.0.0.0",
        port=0,
        start_browser=True,
        username=None,
        password=None,
    )
