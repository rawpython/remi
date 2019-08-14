#!/usr/bin/env python


import unittest
import remi.gui as gui
import sys
import os.path
from mock_server_and_request import MockServer, MockRequest

examples_dir = os.path.realpath(os.path.join(os.path.abspath(\
                                os.path.dirname(__file__)), '../../examples'))
sys.path.append(examples_dir)
from helloworld_app import MyApp


class TestHelloWorld_App(unittest.TestCase):
    def setUp(self):
        # silence request logging for testing
        MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del MyApp.log_request


    def test_main(self):
        myapp = MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = myapp.main()
        html = root_widget.repr()


if __name__ == '__main__':
    unittest.main()
