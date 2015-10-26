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
HTTP_PORT_NUMBER = 8081
IP_ADDR = '127.0.0.1'
BASE_ADDRESS = 'http://' + IP_ADDR + ':' + str(HTTP_PORT_NUMBER) + '/'
MULTIPLE_INSTANCE = False
# this will enable the caching of images, css, and other local resources.
ENABLE_FILE_CACHE = True
runtimeInstances = list()
UPDATE_INTERVAL = 0.1
AUTOMATIC_START_BROWSER = True #when true opens automatically the browser
DEBUG_MODE = 0 #0 - NO DEBUG  1 - ALERTS AND ERRORS  2 - MESSAGES