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

import time
import io

import remi.gui as gui
from remi import start, App
import random
from threading import Timer

class Cell(gui.Widget):
    """
    Represent a message from a client. 
    It contains:
        nick, 
        message body,
        personal reply control
    """
    def __init__(self, width, height, x, y, game):
        super(Cell, self).__init__(width, height)
        self.x = x
        self.y = y
        self.has_mine = False
        self.state = 0 #unknown - doubt - flag
        self.opened = False
        self.nearest_mine = 0
        self.game = game
        
        self.style['font-weight'] = 'bold'
        self.style['text-align'] = 'center'
        self.style['background-size'] = 'contain'
        self.EVENT_ONRIGHTCLICK = "oncontextmenu"
        self.attributes[self.EVENT_ONRIGHTCLICK] = "sendCallback('%s','%s');return false;" % (id(self), self.EVENT_ONRIGHTCLICK)
        self.set_on_click_listener( self, "check_mine" )
        
    def oncontextmenu(self):
        if self.opened: 
            return
        self.next_state()
        
    def next_state(self):
        self.state = (self.state + 1)%3
        self.set_icon()
        self.game.check_if_win()
        
    def check_mine(self, notify_game = True):
        if self.state == 1:
            return
        if self.opened: 
            return
        self.opened = True
        if self.has_mine and notify_game:
            self.game.explosion( self )
            self.set_icon()
            return
        if notify_game:
            self.game.no_mine( self )
        self.set_icon()
        
    def set_mine(self):
        self.has_mine = True
        
    def set_icon(self):
        self.style['background-image'] = "''"
        if self.opened:
            if self.has_mine:
                self.style['background-image'] = "url('/res/mine.png')"
            else:
                if self.nearest_mine > 0:
                    self.append( 'nearestbomb', "%s"%self.nearest_mine )
                else:
                    #self.append( 'nearestbomb', "%s"%self.nearest_mine )
                    self.style['background-color'] = 'rgb(200,255,100)'
            return
        if self.state == 0:
            self.style['background-image'] = "''"
        if self.state == 2:
            self.style['background-image'] = "url('/res/doubt.png')"
        if self.state == 1:
            self.style['background-image'] = "url('/res/flag.png')"
            
    def add_nearest_mine(self):
        self.nearest_mine = self.nearest_mine + 1
        #self.append( 'nearestbomb', "%s"%self.nearest_mine )

class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args, static_paths=('./res/',))

    def display_time(self):
        self.lblTime.set_text('Play time: ' + str(self.time_count))
        self.time_count+=1
        Timer(1,self.display_time).start()   

    def main(self):
        # the arguments are	width - height - layoutOrientationOrizontal
        self.main_container = gui.Widget(1020, 520, False, 10)
        
        self.title = gui.Label( 1000, 30, 'Mine Field GAME' )
        self.title.style['font-size'] = '25px'
        self.title.style['font-weight'] = 'bold'
        
        self.horizontal_container = gui.Widget(1000, 30, True, 0)
        
        self.info = gui.Label( 500, 30, 'Collaborative minefiled game. Enjoy.' )
        self.info.style['font-size'] = '20px'
        
        self.icon_mine = gui.Image(30,30,'/res/mine.png')
        self.icon_flag = gui.Image(30,30,'/res/flag.png')
        
        self.lblMineCount = gui.Label( 100, 30, 'Mines' )
        self.lblFlagCount = gui.Label( 100, 30, 'Flags' )
        
        self.time_count = 0
        self.lblTime = gui.Label( 100, 30, 'Time' )
        
        self.horizontal_container.append( 'info', self.info )
        self.horizontal_container.append( 'icon_mine', self.icon_mine )
        self.horizontal_container.append( 'info_mine', self.lblMineCount )
        self.horizontal_container.append( 'icon_flag', self.icon_flag )
        self.horizontal_container.append( 'info_flag', self.lblFlagCount )
        self.horizontal_container.append( 'info_time', self.lblTime )
        
        self.minecount = 0 #mine number in the map
        self.flagcount = 0 #flag placed by the players
        
        self.mine_table = gui.Table( 1000, 400 )
        
        self.main_container.append('title', self.title)
        self.main_container.append('horizontal_container', self.horizontal_container)
        self.main_container.append('mine_table', self.mine_table)
       
        self.new_game()
         
        self.display_time()
        # returning the root widget
        return self.main_container

    def new_game(self):
        self.time_count = 0
        self.mine_matrix = self.build_mine_matrix(20,50,3)
        self.mine_table.from_2d_matrix( self.mine_matrix, False )
        self.check_if_win()

    def build_mine_matrix(self, w, h, minenum):
        """random fill cells with mines and increments nearest mines num in adiacent cells"""
        matrix = [[Cell(20, 20, x, y, self) for y in range(h)] for x in range(w)]
        for i in range(0,minenum):
            x = random.randint(0,w-1)
            y = random.randint(0,h-1)
            if matrix[x][y].has_mine:
                continue 
                
            self.minecount = self.minecount + 1
            matrix[x][y].set_mine()
            for _x in range(-1,2):
                for _y in range(-1,2):
                    if _x!=0 or _y!=0:
                        if (x + _x) > w-1 or (y + _y) > h-1 or  (x + _x) < 0 or (y + _y) < 0 :
                            continue
                        matrix[x+_x][y+_y].add_nearest_mine()
        return matrix

    def no_mine(self, cell):
        """opens nearest cells that are not near a mine"""
        print("cell x: %s   y:%s"%(cell.x, cell.y))
        if cell.nearest_mine > 0:
            return
        self.fill_void_cells(cell)

    def check_if_win(self):
        """Here are counted the flags. Is checked if the user win."""
        self.flagcount = 0
        win = True
        for x in range(0,len(self.mine_matrix)):
            for y in range(0,len(self.mine_matrix[0])):
                if self.mine_matrix[x][y].state == 1:
                    self.flagcount = self.flagcount + 1
                    if self.mine_matrix[x][y].has_mine == False:
                        win = False
                elif self.mine_matrix[x][y].has_mine == True:
                    win = False
        self.lblMineCount.set_text("%s"%self.minecount)
        self.lblFlagCount.set_text("%s"%self.flagcount)
        if win:
            self.new_game()
                    
    def fill_void_cells(self, cell):
        fill_color_voidcells = random.randint(0,0xffffff)
        terminated = False
        cell.fillcolor = fill_color_voidcells
        checked_cells = [cell,]
        while not terminated:
            terminated = True
            for cell in checked_cells[:]:
                checked_cells.remove(cell)
                x = cell.x
                y = cell.y
                if hasattr(self.mine_matrix[x][y],'fillcolor') and self.mine_matrix[x][y].has_mine == False and self.mine_matrix[x][y].nearest_mine==0:
                    for _x in range(-1,2):
                        for _y in range(-1,2):
                            if (_x+x < 0) or (_y+y < 0) or (_x+x>len(self.mine_matrix)-1) or (_y+y>len(self.mine_matrix[0])-1):
                                continue
                                    
                            if not hasattr(self.mine_matrix[x + _x][y + _y],'fillcolor'):
                                self.mine_matrix[x + _x][y + _y].check_mine(False)
                                self.mine_matrix[x + _x][y + _y].fillcolor = fill_color_voidcells
                                terminated = False
                                checked_cells.append(self.mine_matrix[x + _x][y + _y])
        
    def explosion(self, cell):
        print("explosion")
        for x in range(0,len(self.mine_matrix)):
            for y in range(0,len(self.mine_matrix[0])):
                self.mine_matrix[x][y].style['background-color'] = 'red'
                self.mine_matrix[x][y].check_mine(False)


if __name__ == "__main__":
    start(MyApp,multiple_instance=False)
