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

import os.path
import random
import threading

import remi.gui as gui
from remi import start, App


class Cell(gui.TableItem):
    """
    Represent a cell in the minefield map
    """

    def __init__(self, width, height, x, y, game):
        super(Cell, self).__init__('')
        self.set_size(width, height)
        self.x = x
        self.y = y
        self.has_mine = False
        self.state = 0  # unknown - doubt - flag
        self.opened = False
        self.nearest_mine = 0  # number of mines adjacent with this cell
        self.game = game

        self.style['font-weight'] = 'bold'
        self.style['text-align'] = 'center'
        self.style['background-size'] = 'contain'
        if ((x + y) % 2) > 0:
            self.style['background-color'] = 'rgb(255,255,255)'
        else:
            self.style['background-color'] = 'rgb(245,245,240)'
        self.oncontextmenu.do(self.on_right_click)
        self.onclick.do(self.check_mine)

    def on_right_click(self, widget):
        """ Here with right click the change of cell is changed """
        if self.opened:
            return
        self.state = (self.state + 1) % 3
        self.set_icon()
        self.game.check_if_win()

    def check_mine(self, widget, notify_game=True):
        if self.state == 1:
            return
        if self.opened:
            return
        self.opened = True
        if self.has_mine and notify_game:
            self.game.explosion(self)
            self.set_icon()
            return
        if notify_game:
            self.game.no_mine(self)
        self.set_icon()

    def set_icon(self):
        self.style['background-image'] = "''"
        if self.opened:
            if self.has_mine:
                self.style['background-image'] = "url('/my_resources:mine.png')"
            else:
                if self.nearest_mine > 0:
                    self.set_text(str(self.nearest_mine))
                else:
                    self.style['background-color'] = 'rgb(200,255,100)'
            return
        if self.state == 2:
            self.style['background-image'] = "url('/my_resources:doubt.png')"
        if self.state == 1:
            self.style['background-image'] = "url('/my_resources:flag.png')"

    def add_nearest_mine(self):
        self.nearest_mine += 1


class MyApp(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
        super(MyApp, self).__init__(*args, static_file_path={'my_resources': res_path})

    def display_time(self):
        self.lblTime.set_text('Play time: ' + str(self.time_count))
        self.time_count += 1
        if not self.stop_flag:
            threading.Timer(1, self.display_time).start()

    def main(self):
        # the arguments are    width - height - layoutOrientationOrizontal
        self.main_container = gui.Container(margin='0px auto')
        self.main_container.set_size(1020, 600)
        self.main_container.set_layout_orientation(gui.Container.LAYOUT_VERTICAL)

        self.title = gui.Label('Mine Field GAME')
        self.title.set_size(1000, 30)
        self.title.style['margin'] = '10px'
        self.title.style['font-size'] = '25px'
        self.title.style['font-weight'] = 'bold'

        self.info = gui.Label('Collaborative minefiled game. Enjoy.')
        self.info.set_size(400, 30)
        self.info.style['margin'] = '10px'
        self.info.style['font-size'] = '20px'

        self.lblMineCount = gui.Label('Mines')
        self.lblMineCount.set_size(100, 30)
        self.lblFlagCount = gui.Label('Flags')
        self.lblFlagCount.set_size(100, 30)

        self.time_count = 0
        self.lblTime = gui.Label('Time')
        self.lblTime.set_size(100, 30)

        self.btReset = gui.Button('Restart')
        self.btReset.set_size(100, 30)
        self.btReset.onclick.do(self.new_game)

        self.horizontal_container = gui.Container()
        self.horizontal_container.style['display'] = 'block'
        self.horizontal_container.style['overflow'] = 'auto'
        self.horizontal_container.set_layout_orientation(gui.Container.LAYOUT_HORIZONTAL)
        self.horizontal_container.style['margin'] = '10px'
        self.horizontal_container.append(self.info)
        imgMine = gui.Image('/my_resources:mine.png')
        imgMine.set_size(30, 30)
        self.horizontal_container.append([imgMine, self.lblMineCount])
        imgFlag = gui.Image('/my_resources:flag.png')
        imgFlag.set_size(30, 30)
        self.horizontal_container.append([imgFlag, self.lblFlagCount, self.lblTime, self.btReset])

        self.minecount = 0  # mine number in the map
        self.flagcount = 0  # flag placed by the players

        self.link = gui.Link("https://github.com/dddomodossola/remi",
                             "This is an example of REMI gui library.")
        self.link.set_size(1000, 20)
        self.link.style['margin'] = '10px'

        self.main_container.append([self.title, self.horizontal_container, self.link])

        self.new_game(self)

        self.stop_flag = False
        self.display_time()
        # returning the root widget
        return self.main_container

    def on_close(self):
        self.stop_flag = True
        super(MyApp, self).on_close()

    def coord_in_map(self, x, y, w=None, h=None):
        w = len(self.mine_matrix[0]) if w is None else w
        h = len(self.mine_matrix) if h is None else h
        return not (x > w - 1 or y > h - 1 or x < 0 or y < 0)

    def new_game(self, widget):
        self.time_count = 0
        self.mine_table = gui.Table(margin='0px auto')  # 900, 450
        self.mine_matrix = self.build_mine_matrix(8, 8, 5)
        self.mine_table.empty()

        for x in range(0, len(self.mine_matrix[0])):
            row = gui.TableRow()
            for y in range(0, len(self.mine_matrix)):
                row.append(self.mine_matrix[y][x])
                self.mine_matrix[y][x].onclick.do(self.mine_matrix[y][x].check_mine)
            self.mine_table.append(row)

        # self.mine_table.append_from_list(self.mine_matrix, False)
        self.main_container.append(self.mine_table, key="mine_table")
        self.check_if_win()
        self.set_root_widget(self.main_container)

    def build_mine_matrix(self, w, h, minenum):
        """random fill cells with mines and increments nearest mines num in adiacent cells"""
        self.minecount = 0
        matrix = [[Cell(30, 30, x, y, self) for x in range(w)] for y in range(h)]
        for i in range(0, minenum):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            if matrix[y][x].has_mine:
                continue

            self.minecount += 1
            matrix[y][x].has_mine = True
            for coord in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                _x, _y = coord
                if not self.coord_in_map(x + _x, y + _y, w, h):
                    continue
                matrix[y + _y][x + _x].add_nearest_mine()
        return matrix

    def no_mine(self, cell):
        """opens nearest cells that are not near a mine"""
        if cell.nearest_mine > 0:
            return
        self.fill_void_cells(cell)

    def check_if_win(self):
        """Here are counted the flags. Is checked if the user win."""
        self.flagcount = 0
        win = True
        for x in range(0, len(self.mine_matrix[0])):
            for y in range(0, len(self.mine_matrix)):
                if self.mine_matrix[y][x].state == 1:
                    self.flagcount += 1
                    if not self.mine_matrix[y][x].has_mine:
                        win = False
                elif self.mine_matrix[y][x].has_mine:
                    win = False
        self.lblMineCount.set_text("%s" % self.minecount)
        self.lblFlagCount.set_text("%s" % self.flagcount)
        if win:
            self.dialog = gui.GenericDialog(title='You Win!', message='Game done in %s seconds' % self.time_count)
            self.dialog.confirm_dialog.do(self.new_game)
            self.dialog.cancel_dialog.do(self.new_game)
            self.dialog.show(self)

    def fill_void_cells(self, cell):
        checked_cells = [cell, ]
        while len(checked_cells) > 0:
            for cell in checked_cells[:]:
                checked_cells.remove(cell)
                if (not self.mine_matrix[cell.y][cell.x].has_mine) and \
                        (self.mine_matrix[cell.y][cell.x].nearest_mine == 0):
                    for coord in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                        _x, _y = coord
                        if not self.coord_in_map(cell.x + _x, cell.y + _y):
                            continue

                        if not self.mine_matrix[cell.y + _y][cell.x + _x].opened:
                            self.mine_matrix[cell.y + _y][cell.x + _x].check_mine(None, False)
                            checked_cells.append(self.mine_matrix[cell.y + _y][cell.x + _x])

    def explosion(self, cell):
        print("explosion")
        self.mine_table = gui.Table(margin='0px auto')
        self.main_container.append(self.mine_table, key="mine_table")
        for x in range(0, len(self.mine_matrix[0])):
            for y in range(0, len(self.mine_matrix)):
                self.mine_matrix[y][x].style['background-color'] = 'red'
                self.mine_matrix[y][x].check_mine(None, False)
        self.mine_table.empty()

        # self.mine_table.append_from_list(self.mine_matrix, False)
        for x in range(0, len(self.mine_matrix[0])):
            row = gui.TableRow()
            for y in range(0, len(self.mine_matrix)):
                row.append(self.mine_matrix[y][x])
                self.mine_matrix[y][x].onclick.do(self.mine_matrix[y][x].check_mine)
            self.mine_table.append(row)


if __name__ == "__main__":
    start(MyApp, multiple_instance=True, address='0.0.0.0', port=0, debug=True, start_browser=True)
