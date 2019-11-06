# -*- coding: utf-8 -*-
import remi
import remi.gui as gui
import cv2


class OpencvImageWidget(gui.Image):
    @gui.decorate_constructor_parameter_types([str])
    def __init__(self, filename, **kwargs):
        self.app_instance = None
        super(OpencvImageWidget, self).__init__("/%s/get_image_data" % id(self), **kwargs)
        self.img = cv2.imread(filename, 0)
        self.frame_index = 0
        self.set_image(filename)

    @gui.decorate_set_on_listener("(self, emitter, image_data_as_numpy_array)")
    @gui.decorate_event
    def set_image(self, filename):
        return self.set_image_data(cv2.imread(filename, cv2.IMREAD_COLOR)) #cv2.IMREAD_GRAYSCALE)#cv2.IMREAD_COLOR)

    @gui.decorate_set_on_listener("(self, emitter, image_data_as_numpy_array)")
    @gui.decorate_event
    def set_image_data(self, image_data_as_numpy_array):
        self.img = image_data_as_numpy_array
        self.update(self.app_instance)
        return (self.img,)

    def search_app_instance(self, node):
        if issubclass(node.__class__, remi.server.App):
            return node
        if not hasattr(node, "get_parent"):
            return None
        return self.search_app_instance(node.get_parent()) 

    def update(self, *args):
        if self.app_instance==None:
            self.app_instance = self.search_app_instance(self)
            if self.app_instance==None:
                return
        self.frame_index = self.frame_index + 1
        self.app_instance.execute_javascript("""
            url = '/%(id)s/get_image_data?index=%(frame_index)s';
            
            xhr = null;
            xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'blob'
            xhr.onload = function(e){
                urlCreator = window.URL || window.webkitURL;
                urlCreator.revokeObjectURL(document.getElementById('%(id)s').src);
                imageUrl = urlCreator.createObjectURL(this.response);
                document.getElementById('%(id)s').src = imageUrl;
            }
            xhr.send();
            """ % {'id': id(self), 'frame_index':self.frame_index})

    def refresh(self, opencv_img=None):
        self.img = opencv_img
        self.update(self.app_instance)

    def get_image_data(self, index=0):
        try:
            ret, png = cv2.imencode('.png', self.img)
            if ret:
                headers = {'Content-type': 'image/png'}
                return [png.tostring(), headers]
        except:
            pass
        return None, None


class OpencvCropImageWidget(OpencvImageWidget):
    @gui.decorate_constructor_parameter_types([int, int, int, int])
    def __init__(self, x, y, w, h, **kwargs):
        self.app_instance = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        super(OpencvCropImageWidget, self).__init__("/%s/get_image_data" % id(self), **kwargs)

    @gui.decorate_set_on_listener("(self, emitter, image_data_as_numpy_array)")
    @gui.decorate_event
    def crop(self, emitter, image_data_as_numpy_array):
        self.img = image_data_as_numpy_array[self.x:self.x+self.w, self.y:self.y+self.h]
        self.update(self.app_instance)
        return (self.img,)


class OpencvVideoWidget(OpencvImageWidget):
    @gui.decorate_constructor_parameter_types([int])
    def __init__(self, video_source=0, **kwargs):
        super(OpencvVideoWidget, self).__init__("/%s/get_image_data" % id(self), **kwargs)
        self.capture = cv2.VideoCapture(video_source)
        self.frame_index = 0
        self.app_instance = None
        self.last_frame = None

    def search_app_instance(self, node):
        if issubclass(node.__class__, remi.server.App):
            return node
        if not hasattr(node, "get_parent"):
            return None
        return self.search_app_instance(node.get_parent()) 

    def update(self, *args):
        if self.app_instance==None:
            self.app_instance = self.search_app_instance(self)
            if self.app_instance==None:
                print("no app instance")
                return
        self.frame_index = self.frame_index + 1
        self.app_instance.execute_javascript("""
            var url = '/%(id)s/get_image_data?index=%(frame_index)s';
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'blob'
            xhr.onload = function(e){
                var urlCreator = window.URL || window.webkitURL;
                urlCreator.revokeObjectURL(document.getElementById('%(id)s').src);
                var imageUrl = urlCreator.createObjectURL(this.response);
                document.getElementById('%(id)s').src = imageUrl;
            }
            xhr.send();
            """ % {'id': id(self), 'frame_index':self.frame_index})

    @gui.decorate_set_on_listener("(self, emitter, image_data_as_numpy_array)")
    @gui.decorate_event
    def set_image_data(self, image_data_as_numpy_array):
        self.img = image_data_as_numpy_array
        return (self.img,)

    def get_image_data(self, index=0):
        ret, frame = self.capture.read()
        if ret:
            self.set_image_data(frame)
            ret, png = cv2.imencode('.png', frame)
            if ret:
                headers = {'Content-type': 'image/png'}
                # tostring is an alias to tobytes, which wasn't added till numpy 1.9
                return [png.tostring(), headers]
        return None, None