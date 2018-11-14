# This my first app done using REMI and Python. Probably there is a better way to do it.
# This app is a simple scoreboard. I use it when I play pool/biliard.
# In the app is possible set-up how many Games one has to win, to win a Match.
# Example: the program starts with 5 games to win for a match. The background color of the window of each player is normally green, when one player arrives
# to 4 games won his background becomes orange (it's a sign that he needs only one more game to win the match). When you arrive to 5 your background
# becomes red for 3 seconds and then it goes back to green, the games score goes back to 0 and your "matches won" increase of one.

import remi.gui as gui
from remi import start, App
import os
import time
import threading

class MyApp(App):
   
    # I modified the original CSS file adding a "Button:hover" property and other color schemes; the main configuraton of the program has been done directly in the code.
    # Add the new CSS file in a /RES folder. 
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
        super(MyApp, self).__init__(*args, static_file_path=res_path)
    
    
    def idle(self):
        pass

    # This is the function called as a new thread that updates the Number displayed, change the background color to red for 3 seconds, reset the game variables,
    # change the background color back to green.
    def ChangeColor(self, Text, Side, Num, BtUp, BtDn):
        self.In = 1
        with self.update_lock:
            Text.set_text(str(Num))
            Side.style['background-color'] = 'red'
            BtUp.attributes['class']='up80red'
            BtDn.attributes['class']='dn80red'
        time.sleep(3)    # I tried to make this function without use the thread but the "sleep" here frozen the interface update and I wasn't able to change
                         # the background to red. Remi's guys helped me to solve this.
        with self.update_lock:
            Side.style['background-color'] = 'green'
            BtUp.attributes['class']='up80'
            BtDn.attributes['class']='dn80'
            self.LeftNum = 0
            self.RightNum = 0
        self.In = 0
        self.check_score()

    def main(self):
        self.In = 0   # Used to disable all buttons when in thread function, otherwise strange things happen if you press a button when the app is in the thread
        self.LeftNum = 0    # Left player game won
        self.RightNum = 0    # Right player game won
        self.MatchNum = 5    # Number of game to win for each match
        self.LeftMatchNum = 0    # Left player match won
        self.RightMatchNum = 0    # Right player match won
        self.Name1 = 'LEFT'    # Name left player
        self.Name2 = 'RIGHT'    # Name right player
        
        
        # Main container configuration page
        widMenu = gui.Widget(width=480, height=610, layout_orientation=gui.Widget.LAYOUT_VERTICAL, style={'margin':'0px auto', 'background':'black'})
        # Configuration menu
        self.lblMenu = gui.Label('SCOREBOARD', width='100%', height='45px', style={'margin':'0px 0px 0px', 'padding-top':'10px', 'font-size':'40px', 'font-weight':'bold', 'color':'green', 'line-height':'45px', 'text-align':'center'})
        self.lblMenu2 = gui.Label('Setup players name:', width='100%', height='45px', style={'margin':'0px 0px 0px', 'padding-top':'10px', 'font-size':'30px', 'font-weight':'bold', 'line-height':'45px', 'text-align':'left'})
        self.lblName1 = gui.Label('PLAYER 1 NAME:', width='100%', height='35px', style={'margin':'0px 0px 0px', 'padding-top':'20px', 'font-size':'20px', 'line-height':'25px', 'text-align':'left'})
        self.txtName1 = gui.TextInput(width='96%', height='35px', style={'margin':'0px auto', 'padding-top':'20px', 'padding-left':'5px', 'font-size':'30px', 'line-height':'20px', 'text-align':'left', 'border':'1px solid white', 'background':'black'})
        self.txtName1.set_text('P1')
        self.lblName2 = gui.Label('PLAYER 2 NAME:', width='100%', height='35px', style={'margin':'0px 0px 0px', 'padding-top':'20px', 'font-size':'20px', 'line-height':'25px', 'text-align':'left'})
        self.txtName2 = gui.TextInput(width='96%', height='35px', style={'margin':'0px auto', 'padding-top':'20px', 'padding-left':'5px', 'font-size':'30px', 'line-height':'20px', 'text-align':'left', 'border':'1px solid white', 'background':'black'})
        self.txtName2.set_text('P2')
##        self.lblMatchSet = gui.Label('RACE TO:', width='100%', height='35px', style={'margin':'0px 0px 0px', 'padding-top':'20px', 'font-size':'20px', 'line-height':'25px', 'text-align':'left'})
##        self.txtMatchSet = gui.TextInput(width='100%', height='35px', style={'margin':'0px 0px 0px', 'padding-top':'20px', 'font-size':'30px', 'line-height':'20px', 'text-align':'left', 'border':'1px solid white', 'background':'black'})
##        self.txtMatchSet.set_text('5')
        # Start button
        btMenu = gui.Button('START', width='40%', height='40px', style={'margin':'50px 20% 20px', 'font-size':'30px', 'line-height':'30px', 'text-align':'center'}) 
##        widMenu.append([self.lblMenu, self.lblMenu2, self.lblName1, self.txtName1, self.lblName2, self.txtName2, self.lblMatchSet, self.txtMatchSet, btMenu])
        widMenu.append([self.lblMenu, self.lblMenu2, self.lblName1, self.txtName1, self.lblName2, self.txtName2, btMenu])
        # Buttons function call
        btMenu.onclick.connect(self.on_button_pressed_menu)
        
        
        # Main container scoreboard page
        wid = gui.Widget(width=480, height=610, style={'margin':'0px auto', 'background':'black'})
        # Title
        self.lbl = gui.Label('SCOREBOARD', width='100%', height='35px', style={'margin':'0px 0px 0px', 'padding-top':'10px', 'font-size':'30px', 'line-height':'35px', 'text-align':'center'})
        # Containers for games counters
        # Horizontal container
        wid1 = gui.Widget(width='100%', height=600, layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, style={'background':'black'})
        # Container for left side
        self.wid2 = gui.Widget(width=230, height=350, margin='5px', style={'background':'green'})
        # Container for right side
        self.wid3 = gui.Widget(width=230, height=350, margin='5px', style={'background':'green'})
        # Left side interface
        self.lblLeftName = gui.Label(self.Name1, width='95%', height='60px', style={'margin':'20px 2px 0px', 'font-size':'40px', 'line-height':'60px', 'text-align':'center', 'overflow':'hidden'})
        self.lblLeftNum = gui.Label(str(self.LeftNum), width='100%', height='130px', style={'margin':'0px 0px 10px', 'font-size':'140px', 'line-height':'130px', 'text-align':'center'})
        self.btLeftPlus = gui.Button('', width='80px', height='80px', style={'margin':'0px 10px 20px', 'font-size':'50px', 'line-height':'50px', 'text-align':'center'})
        self.btLeftPlus.attributes['class']='up80'
        self.btLeftMinus = gui.Button('', width='80px', height='80px', style={'margin':'0px 10px 20px', 'font-size':'50px', 'line-height':'50px', 'text-align':'center'})
        self.btLeftMinus.attributes['class']='dn80'
        lblLeftMatch = gui.Label('MATCHES WON:', width=150, height='30px', style={'margin':'0px 5px', 'font-size':'20px', 'line-height':'30px', 'text-align':'left', 'display':'inline'})
        self.lblLeftMatches = gui.Label(str(self.LeftMatchNum), width=30, height='30px', style={'margin':'0px 5px', 'font-size':'20px', 'line-height':'30px', 'text-align':'left', 'display':'inline'})
        # Right side interface
        self.lblRightName = gui.Label(self.Name2, width='95%', height='60px', style={'margin':'20px 2px 0px', 'font-size':'40px', 'line-height':'60px', 'text-align':'center', 'overflow':'hidden'})
        self.lblRightNum = gui.Label(str(self.LeftNum), width='100%', height='130px', style={'margin':'0px 0px 10px', 'font-size':'140px', 'line-height':'130px', 'text-align':'center'})
        self.btRightPlus = gui.Button('', width='80px', height='80px', style={'margin':'0px 10px 20px', 'font-size':'50px', 'line-height':'50px', 'text-align':'center'})
        self.btRightPlus.attributes['class']='up80'
        self.btRightMinus = gui.Button('', width='80px', height='80px', style={'margin':'0px 10px 20px', 'font-size':'50px', 'line-height':'50px', 'text-align':'center'})
        self.btRightMinus.attributes['class']='dn80'
        lblRightMatch = gui.Label('MATCHES WON:', width=150, height='30px', style={'margin':'0px 5px', 'font-size':'20px', 'line-height':'30px', 'text-align':'left', 'display':'inline'})
        self.lblRightMatches = gui.Label(str(self.RightMatchNum), width=30, height='30px', style={'margin':'0px 5px', 'font-size':'20px', 'line-height':'30px', 'text-align':'left', 'display':'inline'})
        # Appends all the widgets to create the interface
        self.wid2.append([self.lblLeftName, self.lblLeftNum, self.btLeftPlus, self.btLeftMinus, lblLeftMatch, self.lblLeftMatches])
        self.wid3.append([self.lblRightName, self.lblRightNum, self.btRightPlus, self.btRightMinus, lblRightMatch, self.lblRightMatches])
        wid1.append(self.wid2)
        wid1.append(self.wid3)
        # Extra labels and button to manage:
        # The number of games to win, to win a match
        lblMatch = gui.Label('GAMES FOR MATCH:', width='50%', height='50px', style={'margin':'15px 2px 0px 10px', 'font-size':'25px', 'line-height':'35px', 'text-align':'center'})
        self.lblMatches = gui.Label(str(self.MatchNum), width='8%', height='50px', style={'margin':'15px 2px 0px', 'font-size':'25px', 'line-height':'35px', 'text-align':'center'})
        btMatchPlus = gui.Button('', width='50px', height='50px', style={'margin':'5px 2px 0px 20px', 'font-size':'30px', 'line-height':'30px', 'text-align':'center'})
        btMatchPlus.attributes['class']='up50'
        btMatchMinus = gui.Button('', width='50px', height='50px', style={'margin':'5px 2px', 'font-size':'30px', 'line-height':'30px', 'text-align':'center'})
        btMatchMinus.attributes['class']='dn50'
        wid1.append([lblMatch, btMatchPlus, self.lblMatches, btMatchMinus])
        # Reset buttons for Score and Matches won
        btReset = gui.Button('RESET SCORE', width='50%', height='35px', style={'margin':'10px 25% 10px', 'font-size':'25px', 'line-height':'30px', 'text-align':'center'}) 
        wid1.append(btReset)
        btResetMatch = gui.Button('RESET MATCH', width='50%', height='35px', style={'margin':'10px 25% 10px', 'font-size':'25px', 'line-height':'30px', 'text-align':'center'}) 
        wid1.append(btResetMatch)
        btSetting = gui.Button('SETTINGS', width='50%', height='35px', style={'margin':'10px 25% 20px', 'font-size':'25px', 'line-height':'30px', 'text-align':'center'}) 
        wid1.append(btSetting)
        # Buttons function call
        # 'LT', 'RT', 'PLUS', 'MINUS' are used to identify the button pressed; in this way I created a single function for Left and Right buttons.
        self.btLeftPlus.onclick.connect(self.on_button_pressed_plus, 'LT')
        self.btLeftMinus.onclick.connect(self.on_button_pressed_minus, 'LT')
        self.btRightPlus.onclick.connect(self.on_button_pressed_plus, 'RT')
        self.btRightMinus.onclick.connect(self.on_button_pressed_minus, 'RT')
        btMatchPlus.onclick.connect(self.on_button_pressed_match, 'PLUS')
        btMatchMinus.onclick.connect(self.on_button_pressed_match, 'MINUS')
        btReset.onclick.connect(self.on_button_pressed_reset)
        btResetMatch.onclick.connect(self.on_button_pressed_reset_match)
        btSetting.onclick.connect(self.on_button_setting)
        # Append the Titleand the interface to the main container
        wid.append(self.lbl)
        wid.append(wid1)
        
        self.wid = wid
        self.widMenu = widMenu
        # Returning the configuration page
        return self.widMenu
    
    #Used to change the size of the font based on the number of characters of the name
    @staticmethod
    def name_length(Name):
        if len(Name) <= 6:
            return (Name, 40)
        elif len(Name) <= 8:
            return (Name, 30)
        elif len(Name) <= 10:
            return (Name, 22)
        else:
            Name = Name[:14]  #always cuts the name at 14 characters
            return (Name, 22)
    
    #Used to setup the name typed in setting window in the scoreboard, and activate the main widget
    def on_button_pressed_menu(self, emitter):
        # left name
        Name = self.txtName1.get_text()
        Name, FntSize = MyApp.name_length(Name)
        FntSize = str(FntSize) + "px"
        self.lblLeftName.style['font-size'] = FntSize
        self.lblLeftName.set_text(Name)
        # right name
        Name = self.txtName2.get_text()
        Name, FntSize = MyApp.name_length(Name)
        FntSize = str(FntSize) + "px"
        self.lblRightName.style['font-size'] = FntSize
        self.lblRightName.set_text(Name)

##        self.lblMatches.set_text(self.txtMatchSet.get_text())
##        self.MatchNum = int(self.txtMatchSet.get_text())
        self.set_root_widget(self.wid)
        
    #Used to activate the setting widget
    def on_button_setting(self, emitter):
        self.set_root_widget(self.widMenu)

    def check_score(self):
        # Here the software update automatically any number you can see in the app
        if (self.LeftNum < self.MatchNum) and (self.RightNum < self.MatchNum):
            self.lblLeftNum.set_text(str(self.LeftNum))
            self.lblRightNum.set_text(str(self.RightNum))
            self.lblLeftMatches.set_text(str(self.LeftMatchNum))
            self.lblRightMatches.set_text(str(self.RightMatchNum))
            self.lblMatches.set_text(str(self.MatchNum))
        # Here the software check if a background needs to be green or orange.
        if (self.LeftNum < self.MatchNum - 1):
            self.wid2.style['background-color'] = 'green'
            self.btLeftPlus.attributes['class']='up80'
            self.btLeftMinus.attributes['class']='dn80'
        if (self.RightNum < self.MatchNum - 1):
            self.wid3.style['background-color'] = 'green'
            self.btRightPlus.attributes['class']='up80'
            self.btRightMinus.attributes['class']='dn80'
        if (self.LeftNum == self.MatchNum - 1):
            self.wid2.style['background-color'] = 'orange'
            self.btLeftPlus.attributes['class']='up80org'
            self.btLeftMinus.attributes['class']='dn80org'
        if (self.RightNum == self.MatchNum - 1):
            self.wid3.style['background-color'] = 'orange'
            self.btRightPlus.attributes['class']='up80org'
            self.btRightMinus.attributes['class']='dn80org'
        # When one of the player win the match a thread is called to temporary convert the background to red and then move it back to green.
        # The thread is required to don't stop the automatic update of the graphics in the app.
        # The app passes to the thread three parameters: lblLeftNum (used as text field to show the number in the app), the widget where the information are on the interface,
        # LeftNum that is the varible to check the games won fro the left player). For right player is the same but instead of left in the varible I used right :-).

        # Left side
        if (self.LeftNum >= self.MatchNum): 
            Side = [self.lblLeftNum, self.wid2, self.LeftNum, self.btLeftPlus, self.btLeftMinus]
            t = threading.Thread(target=self.ChangeColor, args = (Side))
            t.start()
            self.LeftMatchNum = self.LeftMatchNum + 1
        # Right side
        elif (self.RightNum >= self.MatchNum):
            Side = [self.lblRightNum, self.wid3, self.RightNum, self.btRightPlus, self.btRightMinus]
            t = threading.Thread(target=self.ChangeColor, args = (Side))
            t.start()
            self.RightMatchNum = self.RightMatchNum + 1

    # Each function use the Side parameter to identify who called the function and conseguently what update (maybe there is a different way to manage this).
    # Increase the number of the games won
    def on_button_pressed_plus(self, emitter, Side):
        if not self.In:
            if Side == 'LT':
                if self.LeftNum < self.MatchNum:
                   self.LeftNum = self.LeftNum + 1
            elif Side == 'RT':
                if self.RightNum < self.MatchNum:
                   self.RightNum = self.RightNum + 1
            self.check_score()

    # Decrease the number of the games won
    def on_button_pressed_minus(self, emitter, Side):
        if not self.In:
            if Side == 'LT':
                if self.LeftNum != 0:
                    self.LeftNum = self.LeftNum - 1
            elif Side == 'RT':
                if self.RightNum != 0:
                    self.RightNum = self.RightNum - 1
            self.check_score()

    # Increase or decrease the Matches number
    def on_button_pressed_match(self, emitter, Side):
        if not self.In:
            if Side == 'PLUS':
                self.MatchNum = self.MatchNum + 1
            elif Side == 'MINUS':
                # When the user decrease the number of Matches to win, in case this became lower than the actual games won by each player, automatically the number of games
                # won decrease too. It's a way to never have a number of games won bigger than the number of matches needed to win.
                # Try this in the app to better understand my explanation. With Match set-up to five, increase the game won of one player to three and then go down
                # with the Matches button to 1 and see what happen.
                if self.MatchNum > 1:
                    if self.MatchNum - 1 <= self.LeftNum:
                        self.LeftNum = self.LeftNum - 1
                    if self.MatchNum - 1 <= self.RightNum:
                        self.RightNum = self.RightNum - 1
                    self.MatchNum = self.MatchNum - 1
            self.check_score()

    def on_button_pressed_reset(self, emitter):
        if not self.In:
            self.LeftNum = 0
            self.RightNum = 0
            self.check_score()
        
    def on_button_pressed_reset_match(self, emitter):
        if not self.In:
            self.LeftMatchNum = 0
            self.RightMatchNum = 0
            self.check_score()
        

if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    start(MyApp,address='', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    # start(MyApp, debug=True)
