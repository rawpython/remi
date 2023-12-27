import remi.gui as gui
from remi import start, App
from remi_ext import TreeTable


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.wid = gui.VBox(style={"margin": "5px auto", "padding": "10px"})
        table = [
            ("", "#ff9", "cable", "1", "2", "3"),
            ("cable", "#ff9", "1-core cable", "1", "2", "3"),
            ("cable", "#ff9", "multi core cable", "1", "2", "3"),
            ("multi core cable", "#ff9", "2-core cable", "1", "2", "3"),
            ("multi core cable", "#ff9", "3-core cable", "1", "2", "3"),
            ("3-core cable", "#ff9", "3-core armoured cable", "1", "2", "3"),
            ("cable", "#ff9", "armoured cable", "1", "2", "3"),
            ("armoured cable", "#ff9", "3-core armoured cable", "1", "2", "3"),
        ]
        heads_color = "#dfd"
        uoms_color = "#ffd"
        heads = ["heads", heads_color, "object", "one", "two", "three"]
        uoms = ["uom", uoms_color, "", "mm", "cm", "dm"]
        self.My_TreeTable(table, heads, heads2=uoms)
        return self.wid

    def My_TreeTable(self, table, heads, heads2=None):
        """Define and display a table
        in which the values in first column form one or more trees.
        """
        self.Define_TreeTable(heads, heads2)
        self.Display_TreeTable(table)

    def Define_TreeTable(self, heads, heads2=None):
        """Define a TreeTable with a heading row
        and optionally a second heading row.
        """
        display_heads = []
        display_heads.append(tuple(heads[2:]))
        self.tree_table = TreeTable()
        self.tree_table.append_from_list(display_heads, fill_title=True)
        if heads2 is not None:
            heads2_color = heads2[1]
            row_widget = gui.TableRow()
            for index, field in enumerate(heads2[2:]):
                row_item = gui.TableItem(
                    text=field, style={"background-color": heads2_color}
                )
                row_widget.append(row_item, field)
            self.tree_table.append(row_widget, heads2[0])
        self.wid.append(self.tree_table)

    def Display_TreeTable(self, table):
        """Display a table in which the values in first column form one or more trees.
        The table has row with fields that are strings of identifiers/names.
        First convert each row into a row_widget and item_widgets
        that are displayed in a TableTree.
        Each input row shall start with a parent field (field[0])
        that determines the tree hierarchy but that is not displayed on that row.
        The parent widget becomes an attribute of the first child widget.
        Field[1] is the row color, field[2:] contains the row values.
        Top child(s) shall have a parent field value that is blank ('').
        The input table rows shall be in the correct sequence.
        """
        parent_names = []
        hierarchy = {}
        indent_level = 0
        for row in table:
            parent_name = row[0]
            row_color = row[1]
            child_name = row[2]
            row_widget = gui.TableRow(style={"background-color": row_color})
            # Determine whether hierarchy of sub_sub concepts shall be open or not
            openness = "true"
            row_widget.attributes["treeopen"] = openness
            # widget_dict[child_name] = row_widget
            for index, field in enumerate(row[2:]):
                # Determine field color
                field_color = "#ffff99"
                row_item = gui.TableItem(
                    text=field,
                    style={"text-align": "left", "background-color": field_color},
                )
                row_widget.append(row_item, field)
                if index == 0:
                    row_item.parent = parent_name

            # The root of each tree has a parent that is blank ('').
            # Each row with childs has as attribute openness, which by default is 'true'.
            # The fields can be given other attributes, such as color.

            # Verify whether the parent_name (child.parent)
            # is present or is in the list of parent_names.
            print("parent-child:", parent_name, child_name)
            if parent_name == "":
                hierarchy[child_name] = 0
                parent_names.append(child_name)
                target_level = 0
            elif parent_name in parent_names:
                hierarchy[child_name] = hierarchy[parent_name] + 1
                target_level = hierarchy[child_name]
            else:
                # Parent not in parent_names
                print(
                    'Error: Parent name "{}" does not appear in network'.format(
                        parent_name
                    )
                )
                return
            print(
                "indent, target-pre:",
                indent_level,
                target_level,
                parent_name,
                child_name,
            )
            # Indentation
            if target_level > indent_level:
                self.tree_table.begin_fold()
                indent_level += 1
            if target_level < indent_level:
                while target_level < indent_level:
                    indent_level += -1
                    self.tree_table.end_fold()
            print(
                "indent, target-post:",
                indent_level,
                target_level,
                parent_name,
                child_name,
            )
            if child_name not in parent_names:
                parent_names.append(child_name)
            self.tree_table.append(row_widget, child_name)


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    start(
        MyApp,
        address="127.0.0.1",
        port=8081,
        multiple_instance=False,
        enable_file_cache=True,
        update_interval=0.1,
        start_browser=True,
    )
    # start(MyApp, debug=True, address='0.0.0.0', port=0 )
