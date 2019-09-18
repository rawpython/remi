#!/usr/bin/env python

import unittest
import remi.gui as gui
import sys
import os.path
import time

try:
    from mock_server_and_request import MockServer, MockRequest
except ValueError:
    from .mock_server_and_request import MockServer, MockRequest

examples_dir = os.path.realpath(os.path.join(os.path.abspath(\
                                os.path.dirname(__file__)), '../../examples'))
sys.path.append(examples_dir)

import helloworld_app
import template_app
import append_and_remove_widgets_app
import closeable_app
import gauge_app
import grid_layout_app
import layout_app #huh? should it be MyApp??
import matplotlib_app
import minefield_app
import notification_app
import onclose_window_app
import page_internals_app
import pil_app
import resizable_panes
import resources_app
import root_widget_change_app
import session_app
import standalone_app
import svgplot_app
import tabbox
import table_widget_app
import template_advanced_app
import threaded_app
import webAPI_app
import widgets_overview_app


class TestHelloWorldApp(unittest.TestCase):
    def setUp(self):
        # silence request logging for testing
        helloworld_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del helloworld_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = helloworld_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestTemplateApp(unittest.TestCase):
    def setUp(self):
        template_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del template_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = template_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestAppendAndRemoveWidgetsApp(unittest.TestCase):
    def setUp(self):
        append_and_remove_widgets_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del append_and_remove_widgets_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = append_and_remove_widgets_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestCloseableApp(unittest.TestCase):
    def setUp(self):
        closeable_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del closeable_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = closeable_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestGaugeApp(unittest.TestCase):
    def setUp(self):
        gauge_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del gauge_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = gauge_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestGridLayoutApp(unittest.TestCase):
    def setUp(self):
        grid_layout_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del grid_layout_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = grid_layout_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestLayoutApp(unittest.TestCase):
    def setUp(self):
        layout_app.untitled.log_request = (lambda x,y:None)

    def tearDown(self):
        del layout_app.untitled.log_request
        self.app.on_close()

    def test_main(self):
        self.app = layout_app.untitled(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestMatplotlibApp(unittest.TestCase):
    def setUp(self):
        matplotlib_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del matplotlib_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = matplotlib_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

@unittest.skip('This was not terminating cleanly')
class TestMinefieldApp(unittest.TestCase):
    def setUp(self):
        minefield_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del minefield_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = minefield_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestNotificationApp(unittest.TestCase):
    def setUp(self):
        notification_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del notification_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = notification_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestOncloseWindowApp(unittest.TestCase):
    def setUp(self):
        onclose_window_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del onclose_window_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = onclose_window_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestPageInternalsApp(unittest.TestCase):
    def setUp(self):
        page_internals_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del page_internals_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = page_internals_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestPilApp(unittest.TestCase):
    def setUp(self):
        pil_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del pil_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = pil_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()


class TestResizablePanes(unittest.TestCase):
    def setUp(self):
        resizable_panes.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del resizable_panes.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = resizable_panes.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestResourcesApp(unittest.TestCase):
    def setUp(self):
        resources_app.MyApp.log_request = (lambda x,y:None)
        self.previouse_dir = os.getcwd()
        os.chdir(examples_dir)

    def tearDown(self):
        del resources_app.MyApp.log_request
        self.app.on_close()
        os.chdir(self.previouse_dir)

    def test_main(self):
        self.app = resources_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestRootWidgetChangeApp(unittest.TestCase):
    def setUp(self):
        root_widget_change_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del root_widget_change_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = root_widget_change_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

@unittest.skip('This was not terminating cleanly')
class TestSessionApp(unittest.TestCase):
    def setUp(self):
        session_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del session_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = session_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestStandaloneApp(unittest.TestCase):
    def setUp(self):
        standalone_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del standalone_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = standalone_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

@unittest.skip('This was not terminating cleanly')
class TestSvgplotApp(unittest.TestCase):
    def setUp(self):
        svgplot_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del svgplot_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = svgplot_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestTabboxApp(unittest.TestCase):
    def setUp(self):
        tabbox.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del tabbox.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = tabbox.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestTableWidgetApp(unittest.TestCase):
    def setUp(self):
        table_widget_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del table_widget_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = table_widget_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestTemplateAdvancedApp(unittest.TestCase):
    def setUp(self):
        template_advanced_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del template_advanced_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = template_advanced_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

class TestThreadedApp(unittest.TestCase):
    def setUp(self):
        threaded_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del threaded_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = threaded_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        time.sleep(1)
        self.app.on_button_pressed(None)

class TestWebAPIApp(unittest.TestCase):
    def setUp(self):
        webAPI_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del webAPI_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = webAPI_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()

@unittest.skip('This was not terminating cleanly')
class TestWidgetOverviewApp(unittest.TestCase):
    def setUp(self):
        widgets_overview_app.MyApp.log_request = (lambda x,y:None)

    def tearDown(self):
        del widgets_overview_app.MyApp.log_request
        self.app.on_close()

    def test_main(self):
        self.app = widgets_overview_app.MyApp(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()



if __name__ == '__main__':
    unittest.main()