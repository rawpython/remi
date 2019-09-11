#!/usr/bin/env python

'''TODO: make the instantiation test and exception for the rest
of the widgets

NOTE: the dots above the dash line are missing for the full test
command.


'''

import unittest
import remi.gui as gui
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

class SimpleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

def assertValidHTML(text):
    h = SimpleParser()
    h.feed(text) 
    # throws expections if invalid.
    return True


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
        self.assertIn('my remi app', widget.repr())
        assertValidHTML(widget.repr())
        
class TestBODY(unittest.TestCase):
    def test_init(self):
        widget = gui.BODY()
        assertValidHTML(widget.repr())
        
class TestGridBox(unittest.TestCase):
    def test_init(self):
        w = gui.GridBox()
        l = gui.Label('box_label')
        w.append(l)
        self.assertIn('box_label',w.repr())
        assertValidHTML(w.repr())
        
class TestHBox(unittest.TestCase):
    def test_init(self):
        w = gui.HBox()
        l = gui.Label('hbox_label')
        w.append(l)
        self.assertIn('hbox_label',w.repr())
        assertValidHTML(w.repr())

class TestVBox(unittest.TestCase):
    def test_init(self):
        w = gui.VBox()
        l = gui.Label('vbox_label')
        w.append(l)
        self.assertIn('vbox_label',w.repr())
        assertValidHTML(w.repr())
      
class TestTabBox(unittest.TestCase):
    def test_init(self):
        w = gui.TabBox()
        l = gui.Label('testTabBox_label')
        w.add_tab(l, name='testtabbox', tab_cb=None) 
        self.assertIn('testTabBox_label',w.repr())
        assertValidHTML(w.repr())
        
        
class TestButton(unittest.TestCase):
    '''
    Unit testing for Button class. Testing for instantiation and
    exceptions.
    '''
    def test_init(self):
        self.assertEqual(gui.Button(\
                        'Testing button').innerHTML({}),\
                        'Testing button')

        invalid_types = [{}, [], 123, (4, 5)]
        for each_type in invalid_types:
            with self.assertRaises(Exception) as error:
                gui.Button(each_type)

        assertValidHTML(gui.Button('Testing').innerHTML({}))

        
class TestTextInput(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
    
class TestLabel(unittest.TestCase):
    '''
    Unit testing for Label class. This tests the instantiation of 
    the class. It also test to see if there are any exceptions too.
    '''
    def test_init(self):
        self.assertEqual(gui.Label(\
                        'Testing').innerHTML({}),\
                        'Testing')

        invalid_types = [{}, [], 123, (4, 5)]
        for each_type in invalid_types:
            with self.assertRaises(Exception) as error:
                gui.Label(each_type)
        
        assertValidHTML(gui.Label('Testing').innerHTML({}))


class TestProgress(unittest.TestCase):
    def test_init(self):
        progress = gui.Progress()

        h = SimpleParser()
        w = gui.Progress(_max=12,value=1)
        h.feed(w.repr())
        (tag, attrs) = h.elements[0]
        self.assertEquals(int(attrs['max']),12)
        self.assertEquals(int(attrs['value']),1)

class TestGenericDialog(unittest.TestCase):
    '''
    Unit testing for TestGenericDialog class. Tests the functions within 
    the GenericDialog class.
    '''
    def test_init(self):
        self.assertIn('title test', gui.GenericDialog(\
                      title='title test').innerHTML({}))
        
class TestInputDialog(unittest.TestCase):
    def test_init(self):
        widget = gui.InputDialog()
        assertValidHTML(widget.repr())
        
class TestListView(unittest.TestCase):
    def test_init(self):
        widget = gui.ListView()
        assertValidHTML(widget.repr())
        
class TestListItem(unittest.TestCase):
    def test_init(self):
        widget = gui.ListItem()
        assertValidHTML(widget.repr())
        
class TestDropDown(unittest.TestCase):
    def test_init(self):
        widget = gui.DropDown()
        assertValidHTML(widget.repr())
        
class TestDropDownItem(unittest.TestCase):
    def test_init(self):
        widget = gui.DropDownItem()
        assertValidHTML(widget.repr())
        
class TestImage(unittest.TestCase):
    def test_init(self):
        widget = gui.Image()
        assertValidHTML(widget.repr())
        
class TestTable(unittest.TestCase):
    def test_init(self):
        widget = gui.Table()
        assertValidHTML(widget.repr())
        
class TestTableWidget(unittest.TestCase):
    def test_init(self):
        widget = gui.TableWidget()
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
        widget = gui.GenericObject()
        assertValidHTML(widget.repr())
        
class TestFileFolderNavigator(unittest.TestCase):
    def test_init(self):
        widget = gui.FileFolderNavigator()
        assertValidHTML(widget.repr())
        
class TestFileFolderItem(unittest.TestCase):
    def test_init(self):
        widget = gui.FileFolderItem()
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
        widget = gui.MenuItem()
        assertValidHTML(widget.repr())
        
class TestTreeView(unittest.TestCase):
    def test_init(self):
        widget = gui.TreeView()
        assertValidHTML(widget.repr())
        
class TestTreeItem(unittest.TestCase):
    def test_init(self):
        widget = gui.TreeItem()
        assertValidHTML(widget.repr())
        
class TestFileUploader(unittest.TestCase):
    def test_init(self):
        widget = gui.FileUploader()
        assertValidHTML(widget.repr())
        
class TestFileDownloader(unittest.TestCase):
    def test_init(self):
        widget = gui.FileDownloader()
        assertValidHTML(widget.repr())
        
class TestLink(unittest.TestCase):
    def test_init(self):
        widget = gui.Link()
        assertValidHTML(widget.repr())
        
class TestVideoPlayer(unittest.TestCase):
    def test_init(self):
        widget = gui.VideoPlayer()
        assertValidHTML(widget.repr())
        
class TestSvg(unittest.TestCase):
    def test_init(self):
        widget = gui.Svg()
        assertValidHTML(widget.repr())
        
class TestSvgShape(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgShape()
        assertValidHTML(widget.repr())
        
class TestSvgGroup(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgGroup()
        assertValidHTML(widget.repr())
        
class TestSvgRectangle(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgRectangle()
        assertValidHTML(widget.repr())
        
class TestSvgImage(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgImage()
        assertValidHTML(widget.repr())
        
class TestSvgCircle(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgCircle()
        assertValidHTML(widget.repr())
        
class TestSvgLine(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgLine()
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
        widget = gui.SvgText()
        assertValidHTML(widget.repr())
        
class TestSvgPath(unittest.TestCase):
    def test_init(self):
        widget = gui.SvgPath()
        assertValidHTML(widget.repr())


if __name__ == '__main__':
    unittest.main()
