
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
        mainContainer = Widget(300,300,0,0)
        mainContainer.attributes['style'] = "top:52px;float:left;height:262px;width:300px;position:absolute;overflow:auto;margin:0px 0px;left:120px"
        mainContainer.attributes['editor_newclass'] = "False"
        mainContainer.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"
        mainContainer.attributes['ondragover'] = "event.preventDefault();"
        mainContainer.attributes['ondrop'] = "event.preventDefault();return false;"
        mainContainer.attributes['editor_constructor'] = "(300,300,0,0)"
        mainContainer.attributes['class'] = "Widget"
        mainContainer.attributes['draggable'] = "true"
        mainContainer.attributes['editor_tag_type'] = "widget"
        mainContainer.attributes['onclick'] = "sendCallback('99238288','onclick');event.stopPropagation();event.preventDefault();"
        mainContainer.attributes['editor_varname'] = "mainContainer"
        mainContainer.attributes['tabindex'] = "0"
        mainContainer.style['top'] = "52px"
        mainContainer.style['float'] = "left"
        mainContainer.style['height'] = "262px"
        mainContainer.style['width'] = "300px"
        mainContainer.style['position'] = "absolute"
        mainContainer.style['overflow'] = "auto"
        mainContainer.style['margin'] = "0px 0px"
        mainContainer.style['left'] = "120px"
        button = Button(200,30,'button')
        button.attributes['style'] = "top:84px;height:106px;width:206px;position:absolute;overflow:auto;margin:0px 0px;left:52px"
        button.attributes['editor_newclass'] = "False"
        button.attributes['ondragstart'] = "this.style.cursor='move'; event.dataTransfer.dropEffect = 'move';   event.dataTransfer.setData('application/json', JSON.stringify([event.target.id,(event.clientX),(event.clientY)]));"
        button.attributes['ondragover'] = "event.preventDefault();"
        button.attributes['ondrop'] = "event.preventDefault();return false;"
        button.attributes['editor_constructor'] = "(200,30,'button')"
        button.attributes['class'] = "Button"
        button.attributes['draggable'] = "true"
        button.attributes['editor_tag_type'] = "widget"
        button.attributes['onclick'] = "sendCallback('99241584','onclick');event.stopPropagation();event.preventDefault();"
        button.attributes['editor_varname'] = "button"
        button.attributes['tabindex'] = "1"
        button.style['top'] = "84px"
        button.style['height'] = "106px"
        button.style['width'] = "206px"
        button.style['position'] = "absolute"
        button.style['overflow'] = "auto"
        button.style['margin'] = "0px 0px"
        button.style['left'] = "52px"
        mainContainer.append(button,'99241584')
        
        return mainContainer
    

    
if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(untitled, debug=False)
