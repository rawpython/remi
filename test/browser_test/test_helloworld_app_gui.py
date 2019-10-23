# Selenium 3.14+ doesn't enable certificate checking
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



# This is the only code you need to edit in this script.
# Enter in your Sauce Labs Credentials in order to run this test
# This variable contains the service address for the Sauce Labs VM hub

@unittest.skipIf(webdriver is None, "Skipping Selenium test.")
class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.server = remi.Server(MyApp, start=False, address='0.0.0.0',start_browser=False, multiple_instance=True)
        print("MyApp2 is:")
        self.server.start()
        # self.options = webdriver.ChromeOptions()
        # self.options.headless = True
        # self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)

    def test_should_open_chrome(self):
        self.driver.get(self.server.address)
        print("MyApp2 address: " + str(self.server.address))
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


if __name__ == '__main__':
    unittest.main(buffer=True)