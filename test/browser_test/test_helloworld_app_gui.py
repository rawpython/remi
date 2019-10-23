import unittest
import time
import sys
import os
import remi
examples_dir = os.path.realpath(os.path.join(os.path.abspath(\
                                os.path.dirname(__file__)), '../../examples'))
sys.path.append(examples_dir)
from helloworld_app import MyApp

def load_webdriver(browser_name):
    try:
        from selenium import webdriver
    except ImportError:
        webdriver = None

    try:
        DriverClass = webdriver.get(browser_name)
        OptionsClass = webdriver.get(str(browser_name)+"Options")
        DriverClass()
        return (webdriver, DriverClass, OptionsClass)
    except:
        return (webdriver, None, None)

def define_test_suite(browser_name=None):
    (webdriver, DriverClass, OptionsClass) = load_webdriver(browser_name)
    @unittest.skipIf(webdriver is None, "Selenium is not installed.")
    @unittest.skipIf(DriverClass is None, "{} webdriver is not installed.".format(browser_name))
    class TestHelloWorld(unittest.TestCase):

        def setUp(self):
            self.server = remi.Server(MyApp, start=False, address='0.0.0.0', start_browser=False, multiple_instance=True)
            self.server.start()
            self.options = OptionsClass()
            self.options.headless = True
            self.driver = DriverClass(options=self.options)
            self.driver.implicitly_wait(30)
            
        def test_should_open_chrome(self):
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
            button.send_keys('\n')
            time.sleep(1.0)
            body = self.driver.find_elements_by_tag_name('body')[-1]
            # print(body.text, "hereee")
            # self.assertTrue('Hello World!' in body.text)
            self.assertIn('Hello World!', body.text)
            time.sleep(1.0)


        # Here we send the results to Sauce Labs and tear down our driver session
        def tearDown(self):
            # It's important so that you aren't billed after your test finishes.
            self.driver.quit()
            self.server.stop()

    return TestHelloWorld

TestHelloWorldChrome = define_test_suite(browser_name="Chrome")
TestHelloWorldFirefox = define_test_suite(browser_name="Firefox")

if __name__ == '__main__':
    unittest.main(buffer=True, verbosity=2)
