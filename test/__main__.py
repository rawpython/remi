#!/usr/bin/env python

import unittest
import os.path
import sys

if __name__ == '__main__':
    ''' Finds and runs the unit tests.

    '''
    suite = unittest.defaultTestLoader.discover(os.path.dirname(__file__))

    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
