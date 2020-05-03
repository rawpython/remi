# Selenium 3.14+ doesn't enable certificate checking
import unittest
import time
import sys
import os
import remi
examples_dir = os.path.realpath(os.path.join(os.path.abspath(\
                                os.path.dirname(__file__)), '../../examples'))
sys.path.append(examples_dir)
from append_and_remove_widgets_app import MyApp

try:
    from selenium import webdriver
except ImportError:
    webdriver = None

class TestAppendAndRemoveWidgetApp(unittest.TestCase):

    def setUp(self):
        try:
            self.options = self.OptionsClass()
            self.options.headless = True
            self.driver = self.DriverClass(options=self.options)
            self.driver.implicitly_wait(30)
        except Exception:
            self.skipTest("Selenium webdriver is not installed")
        self.server = remi.Server(MyApp, start=False, address='0.0.0.0', start_browser=False, multiple_instance=True)
        self.server.start()

    def test_should_open_browser(self):
        self.driver.get(self.server.address)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('buttons', body.text)

    def test_button_press(self):
        self.driver.get(self.server.address)
        add_button = self.driver.find_elements_by_tag_name('button')[0]
        remove_button = self.driver.find_elements_by_tag_name('button')[1]
        empty_button = self.driver.find_elements_by_tag_name('button')[2]

        time.sleep(1.0)
        for count in range(0,2):
            add_button.send_keys('\n')

        time.sleep(1.0)
        remove_button.send_keys('\n')
        # now we need to know that the right number of boxes have been
        # generated

    def tearDown(self):
        self.driver.quit()
        self.server.stop()

class TestAppendAndRemoveWidgetAppChrome(TestAppendAndRemoveWidgetApp):
    DriverClass = getattr(webdriver, "Chrome", None)
    OptionsClass = getattr(webdriver, "ChromeOptions", None)

class TestAppendAndRemoveWidgetAppFirefox(TestAppendAndRemoveWidgetApp):
    DriverClass = getattr(webdriver, "Firefox", None)
    OptionsClass = getattr(webdriver, "FirefoxOptions", None)

# remove the abstract base class from test discovery
del TestAppendAndRemoveWidgetApp

if __name__ == '__main__':
    unittest.main(buffer=False, verbosity=2)
