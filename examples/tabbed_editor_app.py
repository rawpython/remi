#! /usr/bin/env python
import remi.gui as gui
from remi import start, App

# *****************************************
#  Main page version of add_field_with_label
# *****************************************

def append_with_label(parent,text,field,button,width=300,key=''):
    fields_spacing = 5   #horizontal spacing
    field_height = int(gui.from_pix(field.style['height']))
    field_width = int(gui.from_pix(field.style['width']))
    label = gui.Label(text,width=width-field_width - 3*fields_spacing-20, height=field_height)
    _container = gui.Widget(width=width, height=field_height)
    _container.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)
    _container.style['margin']='4px'
    _container.append(label,key='lbl' + str(key))
    _container.append(field,key='field'+str(key))
    if button is not None:
        _container.append(button,key='button'+str(key))
    parent.append(_container,key=key)


# *****************************************
#  Simple Dialogs
# *****************************************

class OKCancelDialog(gui.GenericDialog):

    def __init__(self, title, text,callback,width=500, height=200):
        self.ok_cancel_callback=callback
        super(OKCancelDialog, self).__init__(width=width, height=height, title='<b>'+title+'</b>', message=text)
        self.set_on_confirm_dialog_listener(self,'confirm_it')
        self.set_on_cancel_dialog_listener(self,'cancel_it')

        
    def confirm_it(self):
        self.ok_cancel_callback(True)


    def cancel_it(self):
        self.ok_cancel_callback(False)

        

class OKDialog(gui.GenericDialog):

    def __init__(self, title, message,width=500, height=200):
        super(OKDialog, self).__init__(width=width, height=height, title='<b>'+title+'</b>', message=message,display_cancel=False)
        self.set_on_confirm_dialog_listener(self,'confirm_it')

    def confirm_it(self):
        pass

#  ****************************************************
# TabView - a framework for a Tabbed Editor
#  ****************************************************

"""
The TabView constucts a container.
The container has a tab bar, tab title and a frame (self.tab_frame).
The tab_frame can contain one of many panels depending on the tab selected
add_tab adds a button to the tab bar, and creates and returns a panel 

"""

class TabView(gui.Widget):
    def __init__(self, frame_width,frame_height,bar_height,**kwargs):
        super(TabView, self).__init__(**kwargs)
        
        self.bar_width=0
        self.bar_height=bar_height
        self.frame_width=frame_width
        self.frame_height=frame_height
        
        self.set_layout_orientation(gui.Widget.LAYOUT_VERTICAL)

        
        #dictionary to  lookup panel object given key
        self.panel_obj=dict()
        self.tab_titles=dict()
        
        #tab bar
        self.tab_bar=gui.Widget(width=self.bar_width,height=self.bar_height)
        self.tab_bar.set_layout_orientation(gui.Widget.LAYOUT_HORIZONTAL)


        # frame to which the panel overwriting the previous. needed to make formatting work?

    # Adds a tab to the Tab Bar, constucts a panel and returns the panel's object
    def add_tab(self, w,key,title):
        tab_button = self._tab_button(w, self.bar_height, title,'button',key)
        self.bar_width+=w
        self.tab_bar.append(tab_button,key=key)
        panel_obj=gui.Widget(width=self.frame_width,height=self.frame_height) #0
        panel_obj.set_layout_orientation(gui.Widget.LAYOUT_VERTICAL)
        self.panel_obj[key]=panel_obj
        self.tab_titles[key]=title
        # print 'add tab',title,key,panel_obj
        return panel_obj

    def construct_tabview(self):
        # make tab bar as wide as the frame
        if self.bar_width<self.frame_width:
            blank_width=self.frame_width-self.bar_width
            but=gui.Button('',width=blank_width,height=self.bar_height)
            self.tab_bar.append(but,key='xxblank')
            self.bar_width=self.frame_width
            
        self.tab_bar.style['width']=gui.to_pix(self.bar_width)
        self.tab_title=gui.Label('fred',width=self.frame_width-30,height=20)
        self.tab_title.style['margin']='2px'
        
        # frame for the tab panel, different tabs are switched into this frame.
        self.tab_frame=gui.Widget(width=self.frame_width,height=self.frame_height) #0
        self.tab_frame.set_layout_orientation(gui.Widget.LAYOUT_VERTICAL)
        
        # add the bar, panels and title to the subclassed Widget
        self.append(self.tab_bar,key='tab_bar')
        self.append(self.tab_title,key='tab_title')
        self.append(self.tab_frame,key='tab_frame')
        self.set_size(self.bar_width,self.frame_height + 100)
        return self

    # only valid after contruct_tabview
    def get_width(self):
        return self.bar_width

    def _tab_button(self,w,h,label,base_name,key):
        # create a button that returns the key to on_click_listener
        bname=base_name+key
        but=gui.Button(label,width=w,height=h)
        f = lambda  _bname=key: self.show( _bname)
        fname=base_name+'_'+key
        setattr(self, fname, f)
        but.set_on_click_listener(self, fname)
        return but


    # show a tab, also internal callback for button presses
    def show(self,key):
        panel_obj=self.panel_obj[key]
        # print 'switch tab',key,panel_obj
        self.tab_frame.append(panel_obj,key='tab_frame')
        self.tab_title.set_text('<b>'+self.tab_titles[key]+'</b>')
        



# *****************************************
# Test App to show a TabView in a dialog
# *****************************************

class Tabbed(App):

    def __init__(self, *args):
        super(Tabbed, self).__init__(*args)


    def main(self):

        # trivial main page
        # ********************
        root = gui.VBox(width=600,height=200) #1

        # button 
        button_tabbed_dialog = gui.Button( 'Open Tabbed Editor',width=250, height=30)
        button_tabbed_dialog.set_on_click_listener(self, 'on_tabbed_dialog_button_clicked')
        root.append(button_tabbed_dialog)

        # and fields in main page    
        self.t1f1_field=gui.Label('Tab1 Field 1: ',width=400,height=30)
        root.append(self.t1f1_field)
        
        self.t2f1_field=gui.Label('Tab2 Field 1: ',width=400,height=30)
        root.append(self.t2f1_field)


        # dialog to contain the TabView
        # ***********************************
        self.tabbed_dialog=gui.GenericDialog(width=450,height=300,title='<b>Tabbed Editor</b>',
                                             message='',autohide_ok=False)
        self.tabbed_dialog.set_on_confirm_dialog_listener(self,'tabbed_dialog_confirm')

        # construct a Tabview - frame_width,frame_height,bar height
        frame_width=400
        self.tabview=TabView(frame_width,100,30)

        # add tabs - tab width,key,title
        self.panel1=self.tabview.add_tab(100,'tab1','Tab 1')
        self.panel2=self.tabview.add_tab(100,'tab2','Tab 2')

        # and finish building the tabview
        self.tabview.construct_tabview()

        # add some fields to the tab panels
        self.t1field1=gui.TextInput(width=300, height=35)
        self.t1field1.set_text('Content of Tab 1 field 1')
        append_with_label(self.panel1,'Field 1',self.t1field1,None,width=frame_width)
 
        self.t2field1=gui.TextInput(width=250, height=30)
        self.t2field1.set_text('Content of Tab 2 field 1')
        self.panel2.append(self.t2field1)

        # add the tabview to the dialog
        self.tabbed_dialog.add_field('tab_view',self.tabview)
        
        return root


    def on_tabbed_dialog_button_clicked(self):
        self.tabbed_dialog.show(self)
        self.tabview.show('tab1')


    def tabbed_dialog_confirm(self):
        OKCancelDialog('Tabbed Editor','Really  save the changes',self.conf_continue).show(self)

    def conf_continue(self,result):
        if result is True:
            # print 'dialog confirm'
            result=self.t1field1.get_value()
            self.t1f1_field.set_text('Tab1 Field1: '+result)
            
            result=self.t2field1.get_value()
            self.t2f1_field.set_text('Tab2 Field1: '+result)
            self.tabbed_dialog.hide()
            OKDialog('Tabbed Editor','Saved').show(self)
        else:
            OKDialog('Tabbed Editor','Not Saved').show(self)
           


#
# ***************************************
# MAIN
# ***************************************

if __name__  ==  "__main__":
    # setting up remi debug level 
    #       2=all debug messages   1=error messages   0=no messages
    import remi.server
    remi.server.DEBUG_MODE = 2

    # start the web server to serve the App
    start(Tabbed,address='127.0.0.1', port=8082,
          multiple_instance=False,enable_file_cache=True,
          update_interval=0.1, start_browser=False)
