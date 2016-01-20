
import remi.gui as gui
from remi.gui import *
from remi import start, App


class untitled(App):
    def __init__(self, *args):
        super(untitled, self).__init__(*args, static_paths=('',))
    
    def main(self):
        return untitled.construct_ui()
        
    @staticmethod
    def construct_ui():
        widget = Widget()
        widget.attributes['style'] = "top:197px;height:229px;width:271px;position:absolute;overflow:auto;margin:0px auto;display:block;left:230px"
        widget.attributes['editor_newclass'] = "False"
        widget.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"
        widget.attributes['ondragover'] = "event.preventDefault();"
        widget.attributes['ondrop'] = "event.preventDefault();return false;"
        widget.attributes['editor_constructor'] = "()"
        widget.attributes['class'] = "Widget"
        widget.attributes['draggable'] = "true"
        widget.attributes['editor_tag_type'] = "widget"
        widget.attributes['onclick'] = "sendCallback('74473200','onclick');event.stopPropagation();event.preventDefault();"
        widget.attributes['editor_varname'] = "widget"
        widget.attributes['tabindex'] = "0"
        widget.style['height'] = "229px"
        widget.style['width'] = "271px"
        widget.style['position'] = "relative"
        widget.style['overflow'] = "auto"
        widget.style['margin'] = "0px auto"
        widget.style['display'] = "block"
        button = Button('button')
        button.attributes['style'] = "top:108px;height:100px;width:100px;position:absolute;overflow:auto;margin:0px auto;display:block;left:87px"
        button.attributes['editor_newclass'] = "False"
        button.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"
        button.attributes['ondragover'] = "event.preventDefault();"
        button.attributes['ondrop'] = "event.preventDefault();return false;"
        button.attributes['editor_constructor'] = "('button')"
        button.attributes['class'] = "Button"
        button.attributes['draggable'] = "true"
        button.attributes['editor_tag_type'] = "widget"
        button.attributes['onclick'] = "sendCallback('73512080','onclick');event.stopPropagation();event.preventDefault();"
        button.attributes['editor_varname'] = "button"
        button.attributes['tabindex'] = "1"
        button.style['top'] = "108px"
        button.style['height'] = "100px"
        button.style['width'] = "100px"
        button.style['position'] = "absolute"
        button.style['overflow'] = "auto"
        button.style['margin'] = "0px auto"
        button.style['display'] = "block"
        button.style['left'] = "87px"
        widget.append(button,'73512080')
        
        return widget
    

    
if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(untitled, debug=False)
