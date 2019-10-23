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


# This is the only code you need to edit in this script.
# Enter in your Sauce Labs Credentials in order to run this test
# This variable contains the service address for the Sauce Labs VM hub

@unittest.skipIf(webdriver is None, "Skipping Selenium test.")
class TestAppendAndRemoveWidgetApp(unittest.TestCase):

    def setUp(self):
        self.server = remi.Server(MyApp, start=False, address='0.0.0.0',start_browser=False)
        self.server.start()
        # the desired_capabilities parameter tells us which browsers and OS to spin up.
        # This creates a webdriver object to send to Sauce Labs including the desired capabilities
        # self.driver = webdriver.Remote(command_executor=remote_url, desired_capabilities=desired_cap)
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.driver = webdriver.Chrome(chrome_options=self.options)
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

if __name__ == '__main__':
    unittest.main(buffer=True)