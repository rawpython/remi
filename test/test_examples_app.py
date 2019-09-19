#!/usr/bin/env python

import unittest
import remi.gui as gui
import sys
import os.path
import time


try:
    from mock_server_and_request import MockServer, MockRequest
    from html_validator import assertValidHTML
except ValueError:
    from .mock_server_and_request import MockServer, MockRequest
    from .html_validator import assertValidHTML

examples_dir = os.path.realpath(os.path.join(os.path.abspath(\
                                os.path.dirname(__file__)), '../examples'))
sys.path.append(examples_dir)


class TestHelloWorldApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import helloworld_app
        cls.AppClass = helloworld_app.MyApp

    def setUp(self):
        # silence request logging for testing
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestTemplateApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import template_app
        cls.AppClass = template_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestAppendAndRemoveWidgetsApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import append_and_remove_widgets_app
        cls.AppClass = append_and_remove_widgets_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestCloseableApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import closeable_app
        cls.AppClass = closeable_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestGaugeApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import gauge_app
        cls.AppClass = gauge_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestGridLayoutApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import grid_layout_app
        cls.AppClass = grid_layout_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestLayoutApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import layout_app
        cls.AppClass = layout_app.untitled

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestMatplotlibApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import matplotlib_app
        cls.AppClass = matplotlib_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

@unittest.skip('This was not terminating cleanly')
class TestMinefieldApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import minefield_app
        cls.AppClass = minefield_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestNotificationApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import notification_app
        cls.AppClass = notification_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestOncloseWindowApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import onclose_window_app
        cls.AppClass = onclose_window_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestPageInternalsApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import page_internals_app
        cls.AppClass = page_internals_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestPilApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import pil_app
        cls.AppClass = pil_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestResizablePanes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import resizable_panes
        cls.AppClass = resizable_panes.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestResourcesApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import resources_app
        cls.AppClass = resources_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)
        self.previouse_dir = os.getcwd()
        os.chdir(examples_dir)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()
        os.chdir(self.previouse_dir)

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestRootWidgetChangeApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import root_widget_change_app
        cls.AppClass = root_widget_change_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

@unittest.skip('This was not terminating cleanly')
class TestSessionApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import session_app
        cls.AppClass = session_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestStandaloneApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import standalone_app
        cls.AppClass = standalone_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

@unittest.skip('This was not terminating cleanly')
class TestSvgplotApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import svgplot_app
        cls.AppClass = svgplot_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestTabboxApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tabbox
        cls.AppClass = tabbox.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestTableWidgetApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import table_widget_app
        cls.AppClass = table_widget_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestTemplateAdvancedApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import template_advanced_app
        cls.AppClass = template_advanced_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

class TestThreadedApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import threaded_app
        cls.AppClass = threaded_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)
        time.sleep(1)
        self.app.on_button_pressed(None)

class TestWebAPIApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import webAPI_app
        cls.AppClass = webAPI_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)

@unittest.skip('This was not terminating cleanly')
class TestWidgetOverviewApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import widgets_overview_app
        cls.AppClass = widgets_overview_app.MyApp

    def setUp(self):
        self.AppClass.log_request = (lambda x,y:None)

    def tearDown(self):
        del self.AppClass.log_request
        self.app.on_close()

    def test_main(self):
        self.app = self.AppClass(MockRequest(), ('0.0.0.0', 8888), MockServer())
        root_widget = self.app.main()
        html = root_widget.repr()
        assertValidHTML(html)



if __name__ == '__main__':
    unittest.main()
