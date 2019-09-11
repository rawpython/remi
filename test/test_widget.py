#!/usr/bin/env python

'''TODO: make the instantiation test and exception for the rest
of the widgets

NOTE: the dots above the dash line are missing for the full test
command.


'''

import unittest
import remi.gui as gui
try:
    from html.parser import HTMLPARSER
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


class Test_VBox(unittest.TestCase):
    def test_init(self):
        w = gui.VBox()
        l = gui.Label('vbox_label')
        w.append(l)
        self.assertIn('vbox_label',w.repr())


class TestGenericDialog(unittest.TestCase):
    '''
    Unit testing for TestGenericDialog class. Tests the functions within 
    the GenericDialog class.
    '''
    def test_init(self):
        self.assertIn('title test', gui.GenericDialog(\
                      title='title test').innerHTML({}))


class Test_Progress(unittest.TestCase):
    def test_init(self):
        progress = gui.Progress()

        h = SimpleParser()
        w = gui.Progress(_max=12,value=1)
        h.feed(w.repr())
        (tag, attrs) = h.elements[0]
        self.assertEquals(int(attrs['max']),12)
        self.assertEquals(int(attrs['value']),1)


if __name__ == '__main__':
    unittest.main()
