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
    @unittest.skipIf(webdriver is None, "Skipping Selenium test.")
    class TestAppendAndRemoveWidgetApp(unittest.TestCase):

        def setUp(self):
            self.server = remi.Server(MyApp, start=False, address='0.0.0.0', start_browser=False, multiple_instance=True)
            self.server.start()
            self.options = OptionsClass()
            self.options.headless = True
            self.driver = DriverClass(options=self.options)
            self.driver.implicitly_wait(30)

        def test_should_open_chrome(self):
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

        # Here we send the results to Sauce Labs and tear down our driver session
        def tearDown(self):
            # This is where you tell Sauce Labs to stop running tests on your behalf.
            # It's important so that you aren't billed after your test finishes.
            self.driver.quit()
            self.server.stop()

    return TestAppendAndRemoveWidgetApp

TestHelloWorldChrome = define_test_suite(browser_name="Chrome")
TestHelloWorldFirefox = define_test_suite(browser_name="Firefox")

if __name__ == '__main__':
    unittest.main(buffer=False, verbosity=2)
