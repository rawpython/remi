
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
        mainContainer = Widget(width=706, height=445, margin='0px auto', style="position: relative")
        subContainer = HBox(width=630, height=277, style='position: absolute; left: 40px; top: 150px; background-color: #b6b6b6')
        vbox = VBox(width=300, height=250)
        bt1 = Button('bt1', width=100, height=30)
        vbox.append(bt1,'bt1')
        bt3 = Button('bt3', width=100, height=30)
        vbox.append(bt3,'bt3')
        bt2 = Button('bt2', width=100, height=30)
        vbox.append(bt2,'bt2')
        subContainer.append(vbox,'vbox')
        hbox = HBox(width=300, height=250)
        lbl1 = Label('lbl1', width=50, height=50, style='background-color: #ffb509')
        hbox.append(lbl1,'lbl1')
        lbl2 = Label('lbl2', width=50, height=50, style='background-color: #40ff2b')
        hbox.append(lbl2,'lbl2')
        lbl3 = Label('lbl3', width=50, height=50, style='background-color: #e706ff')
        hbox.append(lbl3,'lbl3')
        subContainer.append(hbox,'hbox')
        mainContainer.append(subContainer,'subContainer')
        comboJustifyContent = gui.DropDown.new_from_list(('flex-start','flex-end','center','space-between','space-around'),
                                    style='left: 160px; position: absolute; top: 60px; width: 148px; height: 30px')
        mainContainer.append(comboJustifyContent,'comboJustifyContent')
        lblJustifyContent = Label('justify-content', style='left: 40px; position: absolute; top: 60px; width: 100px; height: 30px')
        mainContainer.append(lblJustifyContent,'lblJustifyContent')
        comboAlignItems = gui.DropDown.new_from_list(('stretch','center','flex-start','flex-end','baseline'),
                                    style='left:160px; position:absolute; top:100px; width:152px; height: 30px')
        mainContainer.append(comboAlignItems,'comboAlignItems')
        lblAlignItems = Label('align-items', style='left:40px; position:absolute; top:100px; width:100px; height:30px')
        mainContainer.append(lblAlignItems,'lblAlignItems')
        mainContainer.children['comboJustifyContent'].set_on_change_listener(self.onchange_comboJustifyContent,vbox,hbox)
        mainContainer.children['comboAlignItems'].set_on_change_listener(self.onchange_comboAlignItems,vbox,hbox)

        lblTitle = gui.Label("The following example shows the two main layout style properties for the VBox and HBox containers. Change the value of the two combo boxes.",
                                    style='position:absolute; left:0px; top:0px')
        mainContainer.append(lblTitle)

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

	#on linux generate server.pen with
	#openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

    start(untitled, address=configuration['config_address'], port=configuration['config_port'], multiple_instance=configuration['config_multiple_instance'], enable_file_cache=configuration['config_enable_file_cache'],start_browser=configuration['config_start_browser'], https=True, certfile="./server.pem")
