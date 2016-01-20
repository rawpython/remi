
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
        button = Widget()
        button.attributes['editor_newclass'] = "False"
        button.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"
        button.attributes['ondragover'] = "event.preventDefault();"
        button.attributes['ondrop'] = "event.preventDefault();return false;"
        button.attributes['editor_constructor'] = "(200,200,0,0)"
        button.attributes['style'] = "top:130px;float:left;height:200px;width:200px;position:absolute;overflow:auto;margin:0px 0px;left:177px"
        button.attributes['class'] = "Widget"
        button.attributes['draggable'] = "true"
        button.attributes['editor_tag_type'] = "widget"
        button.attributes['onclick'] = "sendCallback('81881968','onclick');event.stopPropagation();event.preventDefault();"
        button.attributes['editor_varname'] = "button"
        button.attributes['tabindex'] = "0"
        button.style['top'] = "130px"
        button.style['float'] = "left"
        button.style['height'] = "200px"
        button.style['width'] = "200px"
        button.style['position'] = "absolute"
        button.style['overflow'] = "auto"
        button.style['margin'] = "0px 0px"
        button.style['left'] = "177px"
        bt = Button('pulsante')
        bt.attributes['editor_newclass'] = "False"
        bt.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"
        bt.attributes['ondragover'] = "event.preventDefault();"
        bt.attributes['ondrop'] = "event.preventDefault();return false;"
        bt.attributes['editor_constructor'] = "(150,70,'pulsante')"
        bt.attributes['style'] = "top:103px;height:88px;width:113px;position:absolute;overflow:auto;margin:0px 0px;left:31px"
        bt.attributes['class'] = "Button"
        bt.attributes['draggable'] = "true"
        bt.attributes['editor_tag_type'] = "widget"
        bt.attributes['onclick'] = "sendCallback('35278096','onclick');event.stopPropagation();event.preventDefault();"
        bt.attributes['editor_varname'] = "bt"
        bt.attributes['tabindex'] = "1"
        bt.style['top'] = "103px"
        bt.style['height'] = "88px"
        bt.style['width'] = "113px"
        bt.style['position'] = "absolute"
        bt.style['overflow'] = "auto"
        bt.style['margin'] = "0px 0px"
        bt.style['left'] = "31px"
        button.append(bt,'35278096')
        
        return button
    

    
if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(untitled, debug=False)
