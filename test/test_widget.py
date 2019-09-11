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
        raise NotImplemented
        
class TestWidget(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestHTML(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestHEAD(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestBODY(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestGridBox(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
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
        raise NotImplemented
        
class Test_MixinTextualWidget(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
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
        raise NotImplemented
        
class TestListView(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestListItem(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestDropDown(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestDropDownItem(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestImage(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTable(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTableWidget(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTableRow(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTableEditableItem(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTableItem(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTableTitle(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestInput(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestCheckBoxLabel(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestCheckBox(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSpinBox(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSlider(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestColorPicker(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestDate(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestGenericObject(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestFileFolderNavigator(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestFileFolderItem(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestFileSelectionDialog(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestMenuBar(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestMenu(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestMenuItem(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTreeView(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestTreeItem(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestFileUploader(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestFileDownloader(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestLink(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestVideoPlayer(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvg(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgShape(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgGroup(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgRectangle(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgImage(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgCircle(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgLine(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgPolyline(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgPolygon(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgText(unittest.TestCase):
    def test_init(self):
        raise NotImplemented
        
class TestSvgPath(unittest.TestCase):
    def test_init(self):
        raise NotImplemented


if __name__ == '__main__':
    unittest.main()
