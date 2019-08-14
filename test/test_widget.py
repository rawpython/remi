#!/usr/bin/env python

    

import unittest
import remi.gui as gui


class TestLabel(unittest.TestCase):
    '''
    Unit testing for Label class. This tests the instantiation of 
    the class. It also test to see if there are any exceptions too.
    '''
    def test_init(self):
        self.assertEqual(gui.Label('Testing').innerHTML({}), 'Testing')

        invalid_types = [{}, [], 123, (4, 5)]
        for each_type in invalid_types:
            with self.assertRaises(Exception) as error:
                gui.Label(each_type)



if __name__ == '__main__':
    unittest.main()