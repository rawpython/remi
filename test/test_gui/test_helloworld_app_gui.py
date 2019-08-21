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
sauce_username = os.environ.get("SAUCE_USERNAME")
sauce_access_key = os.environ.get("SAUCE_ACCESS_KEY")
tunnel_identifier = os.environ.get("TRAVIS_JOB_NUMBER8")
# This variable contains the service address for the Sauce Labs VM hub
remote_url = "https://ondemand.saucelabs.com:443/wd/hub"

@unittest.skipIf(webdriver is None, "Skipping Selenium test.")
class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.server = remi.Server(MyApp, start=False, address='0.0.0.0',start_browser=False)
        self.server.start()
        # the desired_capabilities parameter tells us which browsers and OS to spin up.
        desired_cap = {
            'platform': 'Mac OS X 10.13',
            'browserName': 'safari',
            'version': "11.1",
            'build': 'remi - Python + UnitTest',
            'name': '1-first-test',
            'username': sauce_username,
            'accessKey': sauce_access_key,
            'tunnel-identifier': tunnel_identifier
        }

        # This creates a webdriver object to send to Sauce Labs including the desired capabilities
        self.driver = webdriver.Remote(command_executor=remote_url, desired_capabilities=desired_cap)
        # self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(5)

    # Here is our actual test code. In this test we open the saucedemo app in chrome
    # and assert that the title is correct.
    # @unittest.skip("You need to input Sauce Credentials")
    def test_should_open_chrome(self):
        self.driver.get(self.server.address)
        button = self.driver.find_element_by_tag_name('button')
        self.assertTrue('Press me!' in button.text)

    def test_button_press(self):
        self.driver.get(self.server.address)
        body = self.driver.find_element_by_tag_name('body')
        self.assertFalse('Hello World!' in body.text)
        print(body.text, "hereee")

        time.sleep(1.0)
        button = self.driver.find_element_by_tag_name('button')
        button.click()
        time.sleep(1.0)
        body = self.driver.find_elements_by_tag_name('body')[-1]
        print(body.text, "hereee")
        self.assertTrue('Hello World!' in body.text)
        time.sleep(1.0)


    # Here we send the results to Sauce Labs and tear down our driver session
    def tearDown(self):
        if sauce_username:
            if self.driver.title == 'MyApp':
                # we use the JavaScript Executor to send results to Sauce Labs Service Hub
                self.driver.execute_script('sauce:job-result=passed')
            else:
                self.driver.execute_script('sauce:job-result=failed')
        # This is where you tell Sauce Labs to stop running tests on your behalf.
        # It's important so that you aren't billed after your test finishes.
        self.driver.quit()
        self.server.stop()


if __name__ == '__main__':
    unittest.main(buffer=True)