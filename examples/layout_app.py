
import remi.gui as gui
from remi.gui import *
from remi import start, App


class untitled(App):
    def __init__(self, *args, **kwargs):
        if not 'editing_mode' in kwargs.keys():
            super(untitled, self).__init__(*args, static_file_path='./res/')

    def idle(self):
        #idle function called every update cycle
        pass
    
    def main(self):
        return untitled.construct_ui(self)
        
    @staticmethod
    def construct_ui(self):
        mainContainer = Widget()
        mainContainer.style['margin'] = "0px auto"
        mainContainer.style['left'] = "1px"
        mainContainer.style['position'] = "absolute"
        mainContainer.style['top'] = "1px"
        mainContainer.style['width'] = "706px"
        mainContainer.style['overflow'] = "auto"
        mainContainer.style['display'] = "block"
        mainContainer.style['height'] = "445px"
        subContainer = HBox()
        subContainer.style['order'] = "2"
        subContainer.style['-webkit-order'] = "-1"
        subContainer.style['position'] = "absolute"
        subContainer.style['width'] = "630px"
        subContainer.style['align-items'] = "center"
        subContainer.style['justify-content'] = "space-around"
        subContainer.style['display'] = "flex"
        subContainer.style['margin'] = "0px auto"
        subContainer.style['left'] = "40px"
        subContainer.style['background-color'] = "#b6b6b6"
        subContainer.style['overflow'] = "auto"
        subContainer.style['height'] = "277px"
        subContainer.style['top'] = "150px"
        subContainer.style['flex-direction'] = "row"
        vbox = VBox()
        vbox.style['order'] = "-1"
        vbox.style['-webkit-order'] = "-1"
        vbox.style['position'] = "static"
        vbox.style['width'] = "300px"
        vbox.style['justify-content'] = "space-around"
        vbox.style['display'] = "flex"
        vbox.style['margin'] = "0px auto"
        vbox.style['overflow'] = "auto"
        vbox.style['height'] = "250px"
        vbox.style['top'] = "64px"
        vbox.style['flex-direction'] = "column"
        bt1 = Button('bt1')
        bt1.style['order'] = "-1"
        bt1.style['margin'] = "0px auto"
        bt1.style['-webkit-order'] = "-1"
        bt1.style['position'] = "static"
        bt1.style['top'] = "1px"
        bt1.style['width'] = "100px"
        bt1.style['overflow'] = "auto"
        bt1.style['display'] = "block"
        bt1.style['height'] = "30px"
        vbox.append(bt1,'bt1')
        bt3 = Button('bt3')
        bt3.style['order'] = "-1"
        bt3.style['margin'] = "0px auto"
        bt3.style['-webkit-order'] = "-1"
        bt3.style['position'] = "static"
        bt3.style['top'] = "1px"
        bt3.style['width'] = "100px"
        bt3.style['overflow'] = "auto"
        bt3.style['display'] = "block"
        bt3.style['height'] = "30px"
        vbox.append(bt3,'bt3')
        bt2 = Button('bt2')
        bt2.style['order'] = "-1"
        bt2.style['margin'] = "0px auto"
        bt2.style['-webkit-order'] = "-1"
        bt2.style['position'] = "static"
        bt2.style['top'] = "1px"
        bt2.style['width'] = "100px"
        bt2.style['overflow'] = "auto"
        bt2.style['display'] = "block"
        bt2.style['height'] = "30px"
        vbox.append(bt2,'bt2')
        subContainer.append(vbox,'vbox')
        hbox = HBox()
        hbox.style['order'] = "-1"
        hbox.style['-webkit-order'] = "-1"
        hbox.style['width'] = "300px"
        hbox.style['align-items'] = "center"
        hbox.style['justify-content'] = "flex-start"
        hbox.style['display'] = "flex"
        hbox.style['margin'] = "0px auto"
        hbox.style['overflow'] = "auto"
        hbox.style['position'] = "static"
        hbox.style['height'] = "250px"
        hbox.style['top'] = "1px"
        hbox.style['flex-direction'] = "row"
        lbl1 = Label('lbl1')
        lbl1.style['order'] = "-1"
        lbl1.style['-webkit-order'] = "-1"
        lbl1.style['width'] = "50px"
        lbl1.style['display'] = "block"
        lbl1.style['margin'] = "0px auto"
        lbl1.style['overflow'] = "auto"
        lbl1.style['background-color'] = "#ffb509"
        lbl1.style['height'] = "50px"
        hbox.append(lbl1,'lbl1')
        lbl2 = Label('lbl2')
        lbl2.style['order'] = "-1"
        lbl2.style['margin'] = "0px auto"
        lbl2.style['-webkit-order'] = "-1"
        lbl2.style['width'] = "50px"
        lbl2.style['overflow'] = "auto"
        lbl2.style['background-color'] = "#40ff2b"
        lbl2.style['display'] = "block"
        lbl2.style['height'] = "50px"
        hbox.append(lbl2,'lbl2')
        lbl3 = Label('lbl3')
        lbl3.style['order'] = "-1"
        lbl3.style['margin'] = "0px auto"
        lbl3.style['-webkit-order'] = "-1"
        lbl3.style['width'] = "50px"
        lbl3.style['overflow'] = "auto"
        lbl3.style['background-color'] = "#e706ff"
        lbl3.style['display'] = "block"
        lbl3.style['height'] = "50px"
        hbox.append(lbl3,'lbl3')
        subContainer.append(hbox,'hbox')
        mainContainer.append(subContainer,'subContainer')
        comboJustifyContent = gui.DropDown.new_from_list(('flex-start','flex-end','center','space-between','space-around'))
        comboJustifyContent.style['margin'] = "0px auto"
        comboJustifyContent.style['left'] = "160px"
        comboJustifyContent.style['position'] = "absolute"
        comboJustifyContent.style['top'] = "60px"
        comboJustifyContent.style['width'] = "148px"
        comboJustifyContent.style['overflow'] = "auto"
        comboJustifyContent.style['display'] = "block"
        comboJustifyContent.style['height'] = "30px"
        mainContainer.append(comboJustifyContent,'comboJustifyContent')
        lblJustifyContent = Label('justify-content')
        lblJustifyContent.style['margin'] = "0px auto"
        lblJustifyContent.style['left'] = "40px"
        lblJustifyContent.style['position'] = "absolute"
        lblJustifyContent.style['top'] = "60px"
        lblJustifyContent.style['width'] = "100px"
        lblJustifyContent.style['overflow'] = "auto"
        lblJustifyContent.style['display'] = "block"
        lblJustifyContent.style['height'] = "30px"
        mainContainer.append(lblJustifyContent,'lblJustifyContent')
        comboAlignItems = gui.DropDown.new_from_list(('stretch','center','flex-start','flex-end','baseline'))
        comboAlignItems.style['margin'] = "0px auto"
        comboAlignItems.style['left'] = "160px"
        comboAlignItems.style['position'] = "absolute"
        comboAlignItems.style['top'] = "100px"
        comboAlignItems.style['width'] = "152px"
        comboAlignItems.style['overflow'] = "auto"
        comboAlignItems.style['display'] = "block"
        comboAlignItems.style['height'] = "30px"
        mainContainer.append(comboAlignItems,'comboAlignItems')
        lblAlignItems = Label('align-items')
        lblAlignItems.style['margin'] = "0px auto"
        lblAlignItems.style['left'] = "40px"
        lblAlignItems.style['position'] = "absolute"
        lblAlignItems.style['top'] = "100px"
        lblAlignItems.style['width'] = "100px"
        lblAlignItems.style['overflow'] = "auto"
        lblAlignItems.style['display'] = "block"
        lblAlignItems.style['height'] = "30px"
        mainContainer.append(lblAlignItems,'lblAlignItems')
        mainContainer.children['comboJustifyContent'].set_on_change_listener(self.onchange_comboJustifyContent,vbox,hbox)
        mainContainer.children['comboAlignItems'].set_on_change_listener(self.onchange_comboAlignItems,vbox,hbox)

        lblTitle = gui.Label("The following example shows the two main layout style properties for the VBox and HBox containers. Change the value of the two combo boxes.")
        lblTitle.style['position'] = "absolute"
        lblTitle.style['left'] = "0px"
        lblTitle.style['top'] = "0px"
        mainContainer.append(lblTitle)


        #In order to allow alignment we must remove the margin setting it to 0px
        for child in hbox.children.values():
            child.style['margin'] = '0px'

        #In order to allow alignment we must remove the margin setting it to 0px
        for child in vbox.children.values():
            child.style['margin'] = '0px'

        self.mainContainer = mainContainer
        return self.mainContainer
    
    def onchange_comboJustifyContent(self,emitter,new_value,vbox,hbox):
        vbox.style['justify-content'] = new_value
        hbox.style['justify-content'] = new_value

    def onchange_comboAlignItems(self,emitter,new_value,vbox,hbox):
        vbox.style['align-items'] = new_value
        hbox.style['align-items'] = new_value



#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 8081, 'config_address': '0.0.0.0', 'config_start_browser': True, 'config_project_name': 'untitled', 'config_resourcepath': './res/'}

if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(untitled, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
