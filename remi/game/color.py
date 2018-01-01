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

def _hex_(c):
    return hex(c)[2:].zfill(2)

class Color(object):
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return '#%s%s%s' % (_hex_(self.r), _hex_(self.g), _hex_(self.b))
    
    
