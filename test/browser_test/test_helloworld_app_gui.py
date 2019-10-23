import unittest
import time
import sys
import os
import remi
examples_dir = os.path.realpath(os.path.join(os.path.abspath(\
                                os.path.dirname(__file__)), '../../examples'))
sys.path.append(examples_dir)
from helloworld_app import MyApp

try:
    from selenium import webdriver
except ImportError:
    webdriver = None

class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        try:
            self.options = self.OptionsClass()
            self.options.headless = True
            self.driver = self.DriverClass(options=self.options)
            self.driver.implicitly_wait(30)
        except:
            self.skipTest("Selenium webdriver is not installed")
        self.server = remi.Server(MyApp, start=False, address='0.0.0.0', start_browser=False, multiple_instance=True)
        self.server.start()

    def test_should_open_browser(self):
        self.driver.get(self.server.address)
        button = self.driver.find_element_by_tag_name('button')
        self.assertTrue('Press me!' in button.text)

    def test_button_press(self):
        self.driver.get(self.server.address)
        body = self.driver.find_element_by_tag_name('body')
        # self.assertFalse('Hello World!' in body.text)
        self.assertNotIn('Hello World!', body.text)
        # print(body.text, "hereee")

        time.sleep(1.0)
        button = self.driver.find_element_by_tag_name('button')
        # button.send_keys('\n')
        button.click()
        time.sleep(1.0)
        body = self.driver.find_elements_by_tag_name('body')[-1]
        # print(body.text, "hereee")
        # self.assertTrue('Hello World!' in body.text)
        self.assertIn('Hello World!', body.text)
        time.sleep(1.0)

    def tearDown(self):
        self.driver.quit()
        self.server.stop()

class TestHelloWorldChrome(TestHelloWorld):
    DriverClass = getattr(webdriver, "Chrome", None)
    OptionsClass = getattr(webdriver, "ChromeOptions", None)

class TestHelloWorldFirefox(TestHelloWorld):
    DriverClass = getattr(webdriver, "Firefox", None)
    OptionsClass = getattr(webdriver, "FirefoxOptions", None)

# remove the abstract base class from test discovery
del TestHelloWorld


if __name__ == '__main__':
    unittest.main(buffer=True, verbosity=2)
