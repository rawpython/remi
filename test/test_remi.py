""" Unit testing for widget_overview_app.py"""

""" 
	Questions:
	1. Do all the functions in this class need to be unit tested? OR do we only
	unit test the important functions? 
	no for making a unit test for the methods/functions only the basic and what
	needs to be tested for sure, use regression testing. 
	you make a test for 1 function and when you change a bit of the function in the
	future, you the regression test will still be able to check it.


	notes:
	https://github.com/dddomodossola/remi/blob/master/remi/server.py
	https://github.com/dddomodossola/remi/blob/master/remi/gui.py

	these 2 are the most important things as they are the functions that makes remi
	possible

	steps:
	1. read the code in the links above
	2. try to create something with the library in remi
	3. then from your new understanding -> judge which methods are the most important
	(ideally all the functions will have unit testing)
	4. make the unit test.

"""

import unittest
import remi.gui as gui

class TestLabel(unittest.TestCase):
	def test_init(self):
		self.assertEqual(gui.Label('Testing').innerHTML({}), 'Testing')
		with self.assertRaises(Exception) as error:
			label = gui.Label(234).innerHTML({})
			self.assertTrue(label in error.exception)


if __name__ == '__main__':
	unittest.main()

