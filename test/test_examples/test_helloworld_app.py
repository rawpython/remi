#!/usr/bin/env python


import unittest
import remi.gui as gui
import sys
import os.path
examples_dir = os.path.realpath(os.path.relpath('../../examples', os.path.dirname(__file__)))
sys.path.append(examples_dir)
from helloworld_app import MyApp

from mock_server_and_request import MockServer, MockRequest


class TestHelloWorld_App(unittest.TestCase):
    def test_main(self):
        myapp = MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = myapp.main()
        html = root_widget.repr()

if __name__ == '__main__':
    unittest.main()
