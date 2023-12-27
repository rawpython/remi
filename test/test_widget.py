#!/usr/bin/env python

import unittest
import remi.gui as gui

try:
    from html_validator import SimpleParser, assertValidHTML
except ValueError:
    from .html_validator import SimpleParser, assertValidHTML


# tests start here
class TestTag(unittest.TestCase):
    def test_init(self):
        widget = gui.Tag()
        assertValidHTML(widget.repr())


class TestWidget(unittest.TestCase):
    def test_init(self):
        widget = gui.Widget()
        assertValidHTML(widget.repr())


class TestHTML(unittest.TestCase):
    def test_init(self):
        widget = gui.HTML()
        assertValidHTML(widget.repr())


class TestHEAD(unittest.TestCase):
    def test_init(self):
        widget = gui.HEAD(title="my remi app")
        self.assertIn("my remi app", widget.repr())
        assertValidHTML(widget.repr())


class TestBODY(unittest.TestCase):
    def test_init(self):
        widget = gui.BODY()
        assertValidHTML(widget.repr())


class TestGridBox(unittest.TestCase):
    def test_init(self):
        w = gui.GridBox()
        l = gui.Label("box_label")
        w.append(l)
        self.assertIn("box_label", w.repr())
        assertValidHTML(w.repr())


class TestHBox(unittest.TestCase):
    def test_init(self):
        w = gui.HBox()
        l = gui.Label("hbox_label")
        w.append(l)
        self.assertIn("hbox_label", w.repr())
        assertValidHTML(w.repr())


class TestVBox(unittest.TestCase):
    def test_init(self):
        w = gui.VBox()
        l = gui.Label("vbox_label")
        w.append(l)
        self.assertIn("vbox_label", w.repr())
        assertValidHTML(w.repr())


class TestTabBox(unittest.TestCase):
    def test_init(self):
        w = gui.TabBox()
        l = gui.Label("testTabBox_label")
        w.add_tab(l, key="testtabbox", callback=None)
        self.assertIn("testTabBox_label", w.repr())
        assertValidHTML(w.repr())


class TestButton(unittest.TestCase):
    """
    Unit testing for Button class. Testing for instantiation and
    exceptions.
    """

    def test_init(self):
        widget = gui.Button("test button")
        self.assertIn("test button", widget.repr())
        assertValidHTML(widget.repr())

        invalid_types = [{}, [], 123, (4, 5)]
        for each_type in invalid_types:
            with self.assertRaises(Exception):
                gui.Button(each_type)


class TestTextInput(unittest.TestCase):
    def test_init(self):
        widget = gui.TextInput(single_line=True, hint="test text input")
        self.assertIn("test text input", widget.repr())
        assertValidHTML(widget.repr())

        widget = gui.TextInput(single_line=False, hint="test text input")
        self.assertIn("test text input", widget.repr())
        assertValidHTML(widget.repr())


class TestLabel(unittest.TestCase):
    """
    Unit testing for Label class. This tests the instantiation of
    the class. It also test to see if there are any exceptions too.
    """

    def test_init(self):
        widget = gui.Label("testing title")
        self.assertIn("testing title", widget.repr())
        assertValidHTML(widget.repr())

        invalid_types = [{}, [], 123, (4, 5)]
        for each_type in invalid_types:
            with self.assertRaises(Exception):
                gui.Label(each_type)


class TestProgress(unittest.TestCase):
    def test_init(self):
        widget = gui.Progress(_max=12, value=1)

        h = SimpleParser()
        h.feed(widget.repr())
        (tag, attrs) = h.elements[0]
        self.assertEquals(int(attrs["max"]), 12)
        self.assertEquals(int(attrs["value"]), 1)


class TestGenericDialog(unittest.TestCase):
    """
    Unit testing for TestGenericDialog class. Tests the functions widgetithin
    the GenericDialog class.
    """

    def test_init(self):
        widget = gui.GenericDialog(title="testing title", message="testing message")

        self.assertIn("testing title", widget.repr())
        self.assertIn("testing message", widget.repr())
        assertValidHTML(widget.repr())


class TestInputDialog(unittest.TestCase):
    def test_init(self):
        widget = gui.InputDialog(title="testing title", message="testing message")

        self.assertIn("testing title", widget.repr())
        self.assertIn("testing message", widget.repr())
        assertValidHTML(widget.repr())


class TestListView(unittest.TestCase):
    def test_init(self):
        widget = gui.ListView()
        assertValidHTML(widget.repr())


class TestListItem(unittest.TestCase):
    def test_init(self):
        widget = gui.ListItem("test list item")
        self.assertIn("test list item", widget.repr())
        assertValidHTML(widget.repr())


class TestDropDown(unittest.TestCase):
    def test_init(self):
        widget = gui.DropDown()
        widget.append("test drop down")
        self.assertIn("test drop down", widget.repr())
        assertValidHTML(widget.repr())


class TestDropDownItem(unittest.TestCase):
    def test_init(self):
        widget = gui.DropDownItem("test drop down item")
        self.assertIn("test drop down item", widget.repr())
        assertValidHTML(widget.repr())


class TestImage(unittest.TestCase):
    def test_init(self):
        widget = gui.Image("http://placekitten.com/200/200")
        assertValidHTML(widget.repr())


class TestTable(unittest.TestCase):
    def test_init(self):
        widget = gui.Table()
        assertValidHTML(widget.repr())


class TestTableWidget(unittest.TestCase):
    def test_init(self):
        widget = gui.TableWidget(2, 3, use_title=True, editable=False)
        assertValidHTML(widget.repr())


class TestTableRow(unittest.TestCase):
    def test_init(self):
        widget = gui.TableRow()
        assertValidHTML(widget.repr())


class TestTableEditableItem(unittest.TestCase):
    def test_init(self):
        widget = gui.TableEditableItem()
        assertValidHTML(widget.repr())


class TestTableItem(unittest.TestCase):
    def test_init(self):
        widget = gui.TableItem()
        assertValidHTML(widget.repr())


class TestTableTitle(unittest.TestCase):
    def test_init(self):
        widget = gui.TableTitle()
        assertValidHTML(widget.repr())


class TestInput(unittest.TestCase):
    def test_init(self):
        widget = gui.Input()
        assertValidHTML(widget.repr())


class TestCheckBoxLabel(unittest.TestCase):
    def test_init(self):
        widget = gui.CheckBoxLabel()
        assertValidHTML(widget.repr())


class TestCheckBox(unittest.TestCase):
    def test_init(self):
        widget = gui.CheckBox()
        assertValidHTML(widget.repr())


class TestSpinBox(unittest.TestCase):
    def test_init(self):
        widget = gui.SpinBox()
        assertValidHTML(widget.repr())


class TestSlider(unittest.TestCase):
    def test_init(self):
        widget = gui.Slider()
        assertValidHTML(widget.repr())


class TestColorPicker(unittest.TestCase):
    def test_init(self):
        widget = gui.ColorPicker()
        assertValidHTML(widget.repr())


class TestDate(unittest.TestCase):
    def test_init(self):
        widget = gui.Date()
        assertValidHTML(widget.repr())


class TestGenericObject(unittest.TestCase):
    def test_init(self):
        widget = gui.GenericObject(filename="shockwave.swf")
        assertValidHTML(widget.repr())

        h = SimpleParser()
        h.feed(widget.repr())
        (tag, attrs) = h.elements[0]
        self.assertEquals(attrs["data"], "shockwave.swf")


class TestFileFolderNavigator(unittest.TestCase):
    def test_init(self):
        widget = gui.FileFolderNavigator(
            multiple_selection=True,
            selection_folder="/",
            allow_file_selection=True,
            allow_folder_selection=True,
        )
        assertValidHTML(widget.repr())


class TestFileFolderItem(unittest.TestCase):
    def test_init(self):
        widget = gui.FileFolderItem("full path", "test file folder item")
        assertValidHTML(widget.repr())


class TestFileSelectionDialog(unittest.TestCase):
    def test_init(self):
        widget = gui.FileSelectionDialog()
        assertValidHTML(widget.repr())


class TestMenuBar(unittest.TestCase):
    def test_init(self):
        widget = gui.MenuBar()
        assertValidHTML(widget.repr())


class TestMenu(unittest.TestCase):
    def test_init(self):
        widget = gui.Menu()
        assertValidHTML(widget.repr())


class TestMenuItem(unittest.TestCase):
    def test_init(self):
        widget = gui.MenuItem("test menu item")
        widget.append(gui.MenuItem("2nd menu item"))
        self.assertIn("test menu item", widget.repr())
        self.assertIn("2nd menu item", widget.repr())
        assertValidHTML(widget.repr())


class TestTreeView(unittest.TestCase):
    def test_init(self):
        widget = gui.TreeView()
        assertValidHTML(widget.repr())


class TestTreeItem(unittest.TestCase):
    def test_init(self):
        widget = gui.TreeItem("test tree item")
        widget.append(gui.TreeItem("2nd tree item"))
        self.assertIn("test tree item", widget.repr())
        self.assertIn("2nd tree item", widget.repr())
        assertValidHTML(widget.repr())


class TestFileUploader(unittest.TestCase):
    def test_init(self):
        widget = gui.FileUploader()
        assertValidHTML(widget.repr())


class TestFileDownloader(unittest.TestCase):
    def test_init(self):
        widget = gui.FileDownloader(text="click here", filename="food.txt")
        assertValidHTML(widget.repr())


class TestLink(unittest.TestCase):
    def test_init(self):
        widget = gui.Link(url="http://google.com", text="google")
        assertValidHTML(widget.repr())
        self.assertIn("google", widget.repr())


class TestVideoPlayer(unittest.TestCase):
    def test_init(self):
        widget = gui.VideoPlayer("http://example.com/video.mp4")
        assertValidHTML(widget.repr())


class TestSvg(unittest.TestCase):
    def test_init(self):
        widget = gui.Svg(width=10, height=10)
        assertValidHTML(widget.repr())


class TestSvgSubcontainer(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgSubcontainer(0, 0, 100, 100)
        assertValidHTML(widget.repr())


class TestSvgGroup(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgGroup()
        assertValidHTML(widget.repr())


class TestSvgRectangle(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgRectangle(10, 10, 10, 10)
        assertValidHTML(widget.repr())


class TestSvgImage(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgImage(filename="food.png", x=10, y=10, w=10, h=10)
        assertValidHTML(widget.repr())


class TestSvgCircle(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgCircle(10, 10, 10)
        assertValidHTML(widget.repr())


class TestSvgLine(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgLine(10, 10, 20, 20)
        assertValidHTML(widget.repr())


class TestSvgPolyline(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgPolyline()
        assertValidHTML(widget.repr())


class TestSvgPolygon(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgPolygon()
        assertValidHTML(widget.repr())


class TestSvgText(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgText(x=10, y=10, text="hello world")
        assertValidHTML(widget.repr())


class TestSvgPath(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgPath(path_value="M 10 10 L 20 20 Z")
        assertValidHTML(widget.repr())


if __name__ == "__main__":
    unittest.main()
