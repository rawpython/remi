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

from remi.server import App
from remi.gui import Widget
from remi.gui import decorate_constructor_parameter_types


def _pixels_(amount):
    if isinstance(amount, int):
        return '%spx' % amount
    else:
        return amount


class Canvas(Widget):
    @decorate_constructor_parameter_types([tuple, App])
    def __init__(self, app_instance, resolution=(0, 0), **kwargs):
        kwargs['width'] = _pixels_(resolution[0])
        kwargs['height'] = _pixels_(resolution[1])
        super(Canvas, self).__init__(**kwargs)
        self._app = app_instance
        self.type = 'canvas'

    @property
    def id(self):
        return self.attributes['id']

    def draw(self, js_code):
        print js_code
        self._app.execute_javascript(js_code)
