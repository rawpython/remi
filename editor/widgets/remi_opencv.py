# -*- coding: utf-8 -*-
import remi
import remi.gui as gui
import cv2


class OpencvImageWidget(gui.Image):
    @gui.decorate_constructor_parameter_types([str, int, int])
    def __init__(self, filename, **kwargs):
        self.app_instance = None
        super(OpencvImageWidget, self).__init__("/%s/get_image_data" % id(self), **kwargs)
        self.img = cv2.imread(filename, 0)
        self.frame_index = 0
        self.set_image(filename)

    def set_image(self, filename):
        self.img = cv2.imread(filename, cv2.IMREAD_COLOR) #cv2.IMREAD_GRAYSCALE)#cv2.IMREAD_COLOR)
        self.update(self.app_instance)

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
        ret, jpeg = cv2.imencode('.png', self.img)
        if ret:
            headers = {'Content-type': 'image/png'}
            return [jpeg.tostring(), headers]
        return None, None


class OpencvVideoWidget(gui.Image):
    @gui.decorate_constructor_parameter_types([int])
    def __init__(self, video_source=0, **kwargs):
        super(OpencvVideoWidget, self).__init__("/%s/get_image_data" % id(self), **kwargs)
        self.capture = cv2.VideoCapture(video_source)
        self.frame_index = 0
        self.app_instance = None

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

    def get_image_data(self, index=0):
        ret, frame = self.capture.read()
        if ret:
            ret, jpeg = cv2.imencode('.png', frame)
            if ret:
                headers = {'Content-type': 'image/png'}
                # tostring is an alias to tobytes, which wasn't added till numpy 1.9
                return [jpeg.tostring(), headers]
        return None, None