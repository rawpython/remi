#!/usr/bin/env python

import unittest
import os.path
import sys

if __name__ == '__main__':
    '''
    Find and run the unit tests.
    This is equivalent to running:
    python -m unittest discover -t remi/ -s remi/test/ -v
    '''

    suite = unittest.defaultTestLoader.discover(os.path.dirname(__file__))
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
