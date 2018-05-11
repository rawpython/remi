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


class GeolocationAPI(gui.Tag):

    def __init__(self, **kwargs):
        super(GeolocationAPI, self).__init__(_type='script', **kwargs)
        self.eventManager = gui._EventManager(self)
        self.EVENT_ONCHANGE = 'onchange'
        self.add_child("javascript", """
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            var params={};
            params['latitude']=lat;
            params['longitude']=lon;
            sendCallbackParam('%(id)s','%(evt)s',params);
        });
        """% {'id': self.identifier,'evt': self.EVENT_ONCHANGE})

    def onchange(self, latitude, longitude):
        return self.eventManager.propagate(self.EVENT_ONCHANGE, (latitude,longitude,))

    def set_on_change_listener(self, callback, *userdata):
        self.eventManager.register_listener(self.EVENT_ONCHANGE, callback, *userdata)


class OrientationAPI(gui.Tag):

    def __init__(self, **kwargs):
        super(OrientationAPI, self).__init__(_type='script', **kwargs)
        self.eventManager = gui._EventManager(self)
        self.EVENT_ONCHANGE = 'onchange'
        self.add_child("javascript", """
        if (window.DeviceOrientationEvent) {
            window.addEventListener('deviceorientation', function(event) {
                var gamma = event.gamma;
                var beta = event.beta;
                var alpha = event.alpha;
                var params={};
                params['gamma']=gamma;
                params['beta']=beta;
                params['alpha']=alpha;
                sendCallbackParam('%(id)s','%(evt)s',params);
            });
        }
        """% {'id': self.identifier,'evt': self.EVENT_ONCHANGE})

    def onchange(self, gamma, beta, alpha):
        return self.eventManager.propagate(self.EVENT_ONCHANGE, (gamma,beta,alpha,))

    def set_on_change_listener(self, callback, *userdata):
        self.eventManager.register_listener(self.EVENT_ONCHANGE, callback, *userdata)


class AccelerometerAPI(gui.Tag):

    def __init__(self, **kwargs):
        super(AccelerometerAPI, self).__init__(_type='script', **kwargs)
        self.eventManager = gui._EventManager(self)
        self.EVENT_ONCHANGE = 'onchange'
        self.add_child("javascript", """
        window.ondevicemotion = function(event) {
            var accelerationX = event.accelerationIncludingGravity.x;
            var accelerationY = event.accelerationIncludingGravity.y;
            var accelerationZ = event.accelerationIncludingGravity.z;
            var params={};
            params['accelerationX']=accelerationX;
            params['accelerationY']=accelerationY;
            params['accelerationZ']=accelerationZ;
            sendCallbackParam('%(id)s','%(evt)s',params);
        }
        """% {'id': self.identifier,'evt': self.EVENT_ONCHANGE})

    def onchange(self, accelerationX, accelerationY, accelerationZ):
        return self.eventManager.propagate(self.EVENT_ONCHANGE, (accelerationX,accelerationY,accelerationZ,))

    def set_on_change_listener(self, callback, *userdata):
        self.eventManager.register_listener(self.EVENT_ONCHANGE, callback, *userdata)


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        wid = gui.VBox(width=300, height=300, margin='0px auto')
        lblGeolocation = gui.Label('Geolocation:' , width='80%', height='50%')
        lblOrientation = gui.Label('Orientation:' , width='80%', height='50%')
        lblAccelerometer = gui.Label('Accelerometer:' , width='80%', height='50%')
        wid.append(lblGeolocation)
        wid.append(lblOrientation)
        wid.append(lblAccelerometer)

        geoApi = GeolocationAPI()
        oriApi = OrientationAPI()
        accApi = AccelerometerAPI()
        wid.add_child("javascript_geo", geoApi)
        wid.add_child("javascript_ori", oriApi)
        wid.add_child("javascript_acc", accApi)

        geoApi.set_on_change_listener(self.onGeolocation, lblGeolocation)
        oriApi.set_on_change_listener(self.onOrientation, lblOrientation)
        accApi.set_on_change_listener(self.onAccelerometer, lblAccelerometer)

        # returning the root widget
        return wid

    # listener function
    def onGeolocation(self, widget, latitude, longitude, label):
        label.set_text("lat: %s, lon:%s"%(latitude, longitude))

    def onOrientation(self, widget, gamma, beta, alpha, label):
        label.set_text("gamma: %s, beta:%s, alpha:%s"%(gamma, beta, alpha))

    def onAccelerometer(self, widget, accelerationX, accelerationY, accelerationZ, label):
        label.set_text("accX: %s, accY:%s, accZ:%s"%(accelerationX, accelerationY, accelerationZ))


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True, address='0.0.0.0', multiple_instance=True, certfile="server.crt", keyfile="server.key", ssl_version=ssl.PROTOCOL_TLSv1_2)
