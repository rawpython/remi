#!/usr/bin/python
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

""" Started: 08.06.2019
    This example shows the use of the following Widget methods:
        Widget.set_enabled(mode) : to deactivate widgets in page
        Widget.set_hidden(mode) : to hide a widgets in page
"""

import remi.gui as gui
from remi import start, App
import os


class MyApp(App):
        def main(self):
                self._counter_ok = 1
                self._counter_user = 1

                main_widget = gui.VBox(width=1000, height=380, style={'margin':'0px auto'})

                child_widget0 = gui.HBox(width=960, height=50, style={'margin':'0px auto; background-color: #bdc'})
                label0 = gui.Label("Control ->", width=80, height=20, style={'margin':'3px'})
                check_enable_single_1 = gui.CheckBoxLabel("enable in 1, 3, 4", True, height=20, style={'margin':'3px'})
                check_enable_single_1.onchange.do(self.on_enable_single_widget, None)
                check_hide_single_2 = gui.CheckBoxLabel("visible widgets in 2, 3, 4", True, height=20, style={'margin':'3px'})
                check_hide_single_2.onchange.do(self.on_hide_single_widget, None)
                check_hide_group_3 = gui.CheckBoxLabel("visible containers & widgets in 2, 3, 4", True, height=20, style={'margin':'3px'})
                check_hide_group_3.onchange.do(self.on_hide_group_widget, None)
                self._label_counter = gui.Label("Counter", width=120, height=20, style={'margin':'3px'})
                child_widget0.append([label0, check_enable_single_1, check_hide_single_2, check_hide_group_3, self._label_counter])

                child_widget1 = gui.HBox(width=960, height=50, style={'margin':'0px auto; background-color: #cdc'})
                title1 = gui.Label("Block 1 ->", width=80, height=20, style={'margin':'3px'})
                self._label1 = gui.Label("Hello", width=50, height=20, style={'margin':'3px'})
                self._check1 = gui.CheckBoxLabel("CheckBox 1", True, width=140, height=20, style={'margin':'3px'})
                self._button1 = gui.Button("OK", width=50, height=20, style={'margin':'3px'})
                self._button1.onclick.do(self.on_ok_pressed)
                self._box1 = self._make_box(1, 400, 28, 4)
                child_widget1.append([title1, self._label1, self._check1, self._button1, self._box1])

                child_widget2 = gui.HBox(width=960, height=50, style={'margin':'0px auto; background-color: #cdc'})
                title2 = gui.Label("Block 2 ->", width=80, height=20, style={'margin':'3px'})
                self._label2 = gui.Label("World", width=50, height=20, style={'margin':'3px'})
                self._check2 = gui.CheckBoxLabel("CheckBox 2", True, width=140, height=20, style={'margin':'3px'})
                self._button2 = gui.Button("OK", width=50, height=20, style={'margin':'3px'})
                self._button2.onclick.do(self.on_ok_pressed)
                self._box2 = self._make_box(2, 400, 28, 4)
                child_widget2.append([title2, self._label2, self._check2, self._button2, self._box2])

                self._child_widget3 = gui.GridBox(width=960, height=90, style={'margin':'0px auto; background-color: #cdc'})
                self._child_widget3.define_grid([
                        ('a0', 'a1', 'a2', 'a3'),
                        ('b0', 'b1', 'b2', 'b3'),
                ])
                title3 = gui.Label("Block 3->", width=80, height=20, style={'margin':'3px'})
                label3 = gui.Label("Label 3", width=50, height=20, style={'margin':'3px'})
                self._check3 = gui.CheckBoxLabel("CheckBox 3", True, width=150, height=20, style={'margin':'3px'})
                self._dropdown3 = gui.DropDown.new_from_list(('apple','banana'), width=150, height=20, style={'margin':'3px'})
                self._box3_1 = self._make_box(3, 400, 28, 4)
                box3_2 = gui.HBox(width=50, height=30, style={'margin':'0px auto; background-color: #b6b6b6'})
                spin3_2 = gui.SpinBox(1, 0, 100, width=40, height=20, margin='10px')
                progress3_2 = gui.Progress(1, 100, width='94%', height=5, margin='3px')
                progress3_2.set_value(50)
                box3_2.append(spin3_2)
                self._child_widget3.append({
                                'a0': title3,
                                'a1': box3_2,
                                'a2': self._check3, 'a3': progress3_2,
                                'b2': self._dropdown3, 'b3': self._box3_1,
                })

                self._child_widget4 = gui.HBox(width=960, height=60, style={'margin':'0px auto; background-color: #cdc'})
                title4 = gui.Label("Block 4->", width=80, height=20, style={'margin':'3px'})
                self._listview4 = listview4 = gui.ListView.new_from_list(('Danny Young','Christine Holand'), width=300, height=50, margin='3px')
                self._listview4.onselection.do(self.on_user_selected)
                self._table4 = table4 = gui.Table.new_from_list([
                                ('ID', 'First Name', 'Last Name'),
                                ('101', 'Danny', 'Young'),
                                ('102', 'Christine', 'Holand')], width=300, margin='3px')
                table4.on_table_row_click.do(self.on_table_row_click)
                self._child_widget4.append([title4, listview4, table4])

                main_widget.append([child_widget0, child_widget1, child_widget2, self._child_widget3, self._child_widget4])

                # returning the root widget
                return main_widget

        def on_enable_single_widget(self, emitter, value, _):
                self._label1.set_enabled(value)
                self._check1.set_enabled(value)
                self._button1.set_enabled(value)
                self._box1.set_enabled(value)
                self._child_widget3.set_enabled(value)
                self._child_widget4.set_enabled(value)

        def on_hide_single_widget(self, emitter, value, _):
                self._hide_widgets(not value, False)

        def on_hide_group_widget(self, emitter, value, _):
                self._hide_widgets(not value, True)

        def _hide_widgets(self, hided, bygroup):
                # hide widgets and containers
                self._label2.set_hidden(hided, bygroup)
                self._check2.set_hidden(hided, bygroup)
                self._button2.set_hidden(hided, bygroup)
                self._box2.set_hidden(hided, bygroup)
                self._child_widget3.set_hidden(hided, bygroup)
                self._listview4.set_hidden(hided, bygroup)
                # self._table4 (gui.Table) not present in self._listview4 after add. Error?
                self._table4.set_hidden(hided, bygroup)

        def on_ok_pressed(self, emitter):
                self._label_counter.set_text('OK: %i' % self._counter_ok)
                self._counter_ok +=1

        def on_user_selected(self, emitter, _):
                self._label_counter.set_text('List: %i' % self._counter_user)
                self._counter_user += 1

        def on_table_row_click(self, table, row, item):
                self._label_counter.set_text('Table: ' + item.get_text())

        def _make_box(self, num, width, height, margin=4):
                box = gui.HBox(width=width, height=height, style={'margin':'0px auto; background-color: #b6b6b6'})
                button1 = gui.Button("OK", width=width/4, height=height-2*margin, style={'margin':'3px'})
                button1.onclick.do(self.on_ok_pressed)
                check1 = gui.CheckBoxLabel("CheckBox %i_1" % num, True, width=width/2, height=height-2*margin, style={'margin':'3px'})
                input1 = gui.Input('enter text', width=width/4, height=height-2*margin, style={'margin':'3px'})
                box.append([button1, check1, input1])
                return box


if __name__ == "__main__":
        start(MyApp)
