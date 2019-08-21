#!/usr/bin/env python

'''TODO: make the instantiation test and exception for the rest
of the widgets

NOTE: the dots above the dash line are missing for the full test
command.
'''

import unittest
import remi.gui as gui


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
    '''Unit testing for Button class. Testing for instantiation and
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


class test_VBox(unittest.TestCase):
    def test_init(self):
        pass


if __name__ == '__main__':
    unittest.main()