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
import remi.server
from remi import start, App
import os #for path handling



class ResizeHelper(gui.Widget, gui.EventSource):
    EVENT_ONDRAG = "on_drag"

    def __init__(self, project, **kwargs):
        super(ResizeHelper, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.style['float'] = 'none'
        self.style['background-color'] = "transparent"
        self.style['border'] = '1px dashed black'
        self.style['position'] = 'absolute'
        self.style['left']='0px'
        self.style['top']='0px'
        self.project = project
        self.parent = None
        self.refWidget = None
        self.active = False
        self.onmousedown.connect(self.start_drag)

        self.origin_x = -1
        self.origin_y = -1
        
    def setup(self, refWidget, newParent):
        #refWidget is the target widget that will be resized
        #newParent is the container
        if self.parent:
            try:
                self.parent.remove_child(self)
            except:
                #there was no ResizeHelper placed
                pass
        if newParent==None:
            return
        self.parent = newParent
        self.refWidget = refWidget
        try:
            self.parent.append(self)
        except:
            #the selected widget's parent can't contain a ResizeHelper
            pass
        #self.refWidget.style['position'] = 'relative'
        self.update_position()
            
    def start_drag(self, emitter, x, y):
        self.active = True
        self.project.onmousemove.connect(self.on_drag)
        self.project.onmouseup.connect(self.stop_drag)
        self.project.onmouseleave.connect(self.stop_drag, 0, 0)
        self.origin_x = -1
        self.origin_y = -1

    def stop_drag(self, emitter, x, y):
        self.active = False
        self.update_position()

    @gui.decorate_event
    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = float(x)
                self.origin_y = float(y)
                self.refWidget_origin_w = gui.from_pix(self.refWidget.style['width'])
                self.refWidget_origin_h = gui.from_pix(self.refWidget.style['height'])
            else:
                self.refWidget.style['width'] = gui.to_pix(self.refWidget_origin_w + float(x) - self.origin_x )
                self.refWidget.style['height'] = gui.to_pix(self.refWidget_origin_h + float(y) - self.origin_y)
                self.update_position()
            return ()

    def update_position(self):
        self.style['position']='absolute'
        self.style['left']=gui.to_pix(gui.from_pix(self.refWidget.style['left']) + gui.from_pix(self.refWidget.style['width']) - gui.from_pix(self.style['width'])/2)
        self.style['top']=gui.to_pix(gui.from_pix(self.refWidget.style['top']) + gui.from_pix(self.refWidget.style['height']) - gui.from_pix(self.style['height'])/2)



class DragHelper(gui.Widget, gui.EventSource):
    EVENT_ONDRAG = "on_drag"

    def __init__(self, project, **kwargs):
        super(DragHelper, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.style['float'] = 'none'
        self.style['background-color'] = "transparent"
        self.style['border'] = '1px dashed black'
        self.style['position'] = 'absolute'
        self.style['left']='0px'
        self.style['top']='0px'
        self.project = project
        self.parent = None
        self.refWidget = None
        self.active = False
        self.onmousedown.connect(self.start_drag)

        self.origin_x = -1
        self.origin_y = -1
        
    def setup(self, refWidget, newParent):
        #refWidget is the target widget that will be resized
        #newParent is the container
        if self.parent:
            try:
                self.parent.remove_child(self)
            except:
                #there was no ResizeHelper placed
                pass
        if newParent==None:
            return
        self.parent = newParent
        self.refWidget = refWidget
        try:
            self.parent.append(self)
        except:
            #the selected widget's parent can't contain a ResizeHelper
            pass
        #self.refWidget.style['position'] = 'relative'
        self.update_position()
            
    def start_drag(self, emitter, x, y):
        self.active = True
        self.project.onmousemove.connect(self.on_drag)
        self.project.onmouseup.connect(self.stop_drag)
        self.project.onmouseleave.connect(self.stop_drag, 0, 0)
        self.origin_x = -1
        self.origin_y = -1
    
    def stop_drag(self, emitter, x, y):
        self.active = False
        self.update_position()

    @gui.decorate_event
    def on_drag(self, emitter, x, y):
        if self.active:
            if self.origin_x == -1:
                self.origin_x = float(x)
                self.origin_y = float(y)
                self.refWidget_origin_x = gui.from_pix(self.refWidget.style['left'])
                self.refWidget_origin_y = gui.from_pix(self.refWidget.style['top'])
            else:
                self.refWidget.style['left'] = gui.to_pix(self.refWidget_origin_x + float(x) - self.origin_x )
                self.refWidget.style['top'] = gui.to_pix(self.refWidget_origin_y + float(y) - self.origin_y)
                self.update_position()
            return ()

    def update_position(self):
        self.style['position']='absolute'
        self.style['left']=gui.to_pix(gui.from_pix(self.refWidget.style['left']) - gui.from_pix(self.style['width'])/2)
        self.style['top']=gui.to_pix(gui.from_pix(self.refWidget.style['top']) - gui.from_pix(self.style['height'])/2)


class FloatingPanesContainer(gui.Widget):

    def __init__(self, **kwargs):
        super(FloatingPanesContainer, self).__init__(**kwargs)
        self.resizeHelper = ResizeHelper(self, width=16, height=16)
        self.dragHelper = DragHelper(self, width=15, height=15)
        self.resizeHelper.on_drag.connect(self.on_helper_dragged_update_the_latter_pos, self.dragHelper)
        self.dragHelper.on_drag.connect(self.on_helper_dragged_update_the_latter_pos, self.resizeHelper)

        self.style['position'] = 'relative'    
        self.style['overflow'] = 'auto'

        self.append(self.resizeHelper)
        self.append(self.dragHelper)

    def add_pane(self, pane, x, y):
        pane.style['left'] = gui.to_pix(x)
        pane.style['top'] = gui.to_pix(y)
        pane.onclick.connect(self.on_pane_selection)
        pane.style['position'] = 'absolute'
        self.append(pane)
        self.on_pane_selection(pane)

    def on_pane_selection(self, emitter):
        print('on pane selection')
        self.resizeHelper.setup(emitter,self)
        self.dragHelper.setup(emitter,self)
        self.resizeHelper.update_position()
        self.dragHelper.update_position()

    def on_helper_dragged_update_the_latter_pos(self, emitter, widget_to_update):
        widget_to_update.update_position()
        
        
class MyApp(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(__file__), 'res')
        super(MyApp, self).__init__(*args, static_file_path=res_path)

    def idle(self):
        pass

    def main(self):
        self.floatingPaneContainer = FloatingPanesContainer(width=800, height=600, margin='0px auto')
        self.floatingPaneContainer.append(gui.Label("Click a panel to select, than drag and stretch"))

        pane1 = gui.Widget(width=100, height=200)
        pane1.style['background-color'] = 'yellow'
        self.floatingPaneContainer.add_pane(pane1, 10, 100)
        pane1.append(gui.Label("Panel1, drag and stretch"))

        pane2 = gui.VBox(width=100, height=200)
        pane2.style['background-color'] = 'green'
        self.floatingPaneContainer.add_pane(pane2, 150, 100)
        pane2.append(gui.Label("Panel2, drag and stretch"))
        

        # returning the root widget
        return self.floatingPaneContainer


    
if __name__ == "__main__":
    start(MyApp, debug=False, address='0.0.0.0', port=0, update_interval=0.01)
