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
import threading
from threading import Timer
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

import base64
import ssl

class HalconMsgHandler(socketserver.BaseRequestHandler, object):
    def __init__(self, *args, **kvargs):
        super(HalconMsgHandler, self).__init__(*args, **kvargs)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        #print("{} wrote:".format(self.client_address[0]))
        print("msg from halcon:" + self.data)
        self.server.app_instance.new_halcon_code(self.data)


class ImageGrabber(gui.Tag, gui.EventSource):

    def __init__(self, app_instance, width, height, **kwargs):
        super(ImageGrabber, self).__init__(_type='script', **kwargs)
        gui.EventSource.__init__(self)
        self.app = app_instance
        self.add_child("javascript", """
            var video = null;
            var canvas = null;
            var localMediaStream = null;
            var mediaStreamTrack = null;
            var flash_on = false;


            function snapshot() {
                if (localMediaStream) {
                    var ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0);
                    canvas.toBlob(function(blob){
                        var xhr = new XMLHttpRequest();
                        var fd = new FormData();
                        xhr.open("POST", "/", true);
                        xhr.setRequestHeader('filename', "test");
                        xhr.setRequestHeader('listener', '%(id)s');
                        xhr.setRequestHeader('listener_function', '%(evt_foto)s');
                        xhr.onreadystatechange = function() {
                            if (xhr.readyState == 4 && xhr.status == 200) {
                                console.log('upload success: ');
                            }else if(xhr.status == 400){
                                console.log('upload failed: ');
                            }
                        };
                        fd.append('upload_file', blob);
                        xhr.send(fd);

                        /*
                        var reader = new FileReader();
                        reader.readAsDataURL(blob); 
                        reader.onloadend = function() {
                            base64data = reader.result;                
                            var params={};
                            params['img_data']=base64data.split(',')[1];
                            sendCallbackParam('%(id)s','new_blob',params);
                        }
                        */
                    }, "image/png");
                    if(flash_on){
                        flashlight();
                        //flash_on=false;
                    }

                }
            }

            function flashlight(){
                mediaStreamTrack.applyConstraints({advanced: [{torch: true}]});
            }

            function get_available_videoinputs(){
                //looking for available video input devices
                navigator.mediaDevices.enumerateDevices().then(function(devices) {
                    // devices is an array of accessible audio and video inputs. deviceId is the property I used to switch cameras
                    for(var i = 0; i < devices.length; i++){
                        if( devices[i].kind == 'videoinput'){
                            var params={};params['device_id']=devices[i].deviceId;
                            params['device_kind']=devices[i].kind;
                            params['device_label']=devices[i].label;
                            sendCallbackParam('%(id)s','%(evt_videodevice)s',params);
                        }
                    }
                });
            }

            function getUserMedia(constraints, successCallback, failureCallback) {
                /*var api = navigator.getUserMedia || navigator.webkitGetUserMedia ||
                    navigator.mozGetUserMedia || navigator.msGetUserMedia;
                if (api) {
                    return api.bind(navigator)(constraints, successCallback, failureCallback);
                }*/

                navigator.mediaDevices.getUserMedia(constraints).then(successCallback);
            }
            
            function startGrab(device_id, use_flash){
                flash_on = use_flash;
                try{
                    localMediaStream = null;
                    mediaStreamTrack.stop();
                }catch(e){}

                var constraints = {
                        video: {deviceId: {exact: device_id}, width: { ideal: %(width)s }, height: { ideal: %(height)s } }
                    };
                
                getUserMedia(constraints
                    , function (stream) {
                        mediaStreamTrack = stream.getVideoTracks()[0];
                        //var imageCapture = new ImageCapture(mediaStreamTrack);
                        
                        video = document.querySelector('video');
                        canvas = document.querySelector('canvas');

                        if (navigator.mozGetUserMedia) {
                            video.mozSrcObject = stream;
                        } else {
                            video.srcObject = stream;
                            video.src = (window.URL || window.webkitURL).createObjectURL(stream);
                        }
                        video.play();
                        localMediaStream = stream;
                        snapshot();
                    }, function (err) {
                        alert('Error: ' + err);
                    });
            }
            
            """% {'width':width, 'height':height, 'id': self.identifier,'evt_foto': self.EVENT_ONCHANGE,'evt_videodevice': self.EVENT_ONNEWVIDEODEVICE}) # on new image available

    @gui.decorate_event
    def onchange(self, image_data, filename):
        return (image_data,)

    @gui.decorate_event
    def onnewvideodevice(self, device_id, device_kind, device_label):
        print("new video device: " + device_id + "  kind: " + device_kind + "  label: " + device_label )
        return (device_id, device_kind, device_label)

    def get_available_videoinputs(self):
        self.app.execute_javascript('get_available_videoinputs();')

    def startGrab(self, device_id='default', use_flash="false"):
        self.app.execute_javascript('startGrab("%s", %s);'%(device_id, use_flash))

    def nextFrame(self):
        self.app.execute_javascript('snapshot();')

    def new_blob(self, img_data):
        img_data = base64.b64decode(img_data)
        f = open("./img.png",'wb')
        f.write(img_data)
        f.close()



class MyApp(App):
    ON_LOG = "onlog"

    def __init__(self, *args):
        super(MyApp, self).__init__(*args, static_file_path='./res/')

    def onlog(self, msg):
        print("LOG LOG LOG")
        print("CONSOLE LOG: " + msg)

    def main(self):
        wid = gui.VBox(width='100%', margin='0px auto')

        width = '300' #'2048'
        height = '300' #'1152'
        self.video = gui.Widget(width=300, height=300, _type='video')
        self.video.attributes['autoplay'] = 'true'
        self.video.style['overflow'] = 'hidden'
        self.video.attributes['width'] = width
        self.video.attributes['height'] = height

        self.canvas = gui.Widget(_type='canvas')
        self.canvas.style['display'] = 'none'
        self.canvas.attributes['width'] = width
        self.canvas.attributes['height'] = height

        self.imgGrabber = ImageGrabber(self, width, height)
        
        self.imgGrabber.onchange.connect(self.on_new_image)
        self.imgGrabber.onnewvideodevice.connect(self.new_video_device)
        getVideoInputsButton = gui.Button("Get cameras", margin='10px')
        getVideoInputsButton.onclick.connect(self.on_get_video_inputs)
        captureButton = gui.Button("Start", margin='10px')
        captureButton.onclick.connect(self.on_start_grab, None)

        self.check_flash = gui.CheckBoxLabel('Flashlight', False, width=200, height=30, margin='10px')
        self.check_flash.onchange.connect(self.on_start_grab)

        self.label = gui.Label('Image capture')
        self.label.style['font-size'] = '18px'

        self.device_list = gui.DropDown(width=100)

        wid.append(self.label)
        wid.append(self.video)
        wid.append(self.canvas)
        wid.append(getVideoInputsButton)
        wid.append(self.device_list)
        wid.append(captureButton)
        wid.append(self.check_flash)
        

        #javascript_log_override = gui.Tag(_type='script')
        #javascript_log_override.add_child("javascript", """ console.log = function(message) { alert(message);}; console.error = console.debug = console.info =  console.log;""")
        #wid.add_child("javascript_log_override",javascript_log_override)
        

        self.halcon_msg_handler_server = socketserver.TCPServer(('localhost', 0), HalconMsgHandler)
        self.halcon_msg_handler_server.app_instance = self #in order to pass app instance to req handler
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        threading.Thread(target=self.halcon_msg_handler_server.serve_forever).start()


        wid.add_child("javascript_image_grabber", self.imgGrabber)

        self.dialog = None

        # returning the root widget
        return wid

    def on_get_video_inputs(self, emitter):
        self.imgGrabber.get_available_videoinputs()
    
    def new_video_device(self, emitter, device_id, device_kind, device_label):
        item = gui.DropDownItem(device_label)
        item.device_id = device_id
        self.device_list.append(item,device_id)
        self.device_list.select_by_key(device_id)

    def on_start_grab(self, emitter, _):
        self.grab()

    def grab(self):
        print("DEVICE ID: " + str(self.device_list.children[self.device_list.get_key()].device_id))
        flash = self.check_flash.get_value()
        self.imgGrabber.startGrab(self.device_list.children[self.device_list.get_key()].device_id, str(flash).lower())

    def on_new_image(self, widget, img_data):
        ip, port = self.halcon_msg_handler_server.server_address
        f = open("./%s.png"%str(port),'wb')
        f.write(img_data)
        f.close()

    def new_halcon_code(self, data):
        if self.dialog == None:
            if data=='nocode':
                self.imgGrabber.nextFrame()
            else:
                self.dialog = gui.GenericDialog(title='DECODE OK', message=data, width='200px')
                self.dialog.confirm_dialog.connect(self.on_dialog_confirm)
                self.dialog.show(self)

    def on_dialog_confirm(self, emitter):
        self.grab()
        self.dialog=None


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True, address='0.0.0.0', multiple_instance=True, port=8081, start_browser=False, certfile="server.crt", keyfile="server.key", ssl_version=ssl.PROTOCOL_TLSv1_2)#, https=True, certfile="./server.pem")
