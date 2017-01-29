import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pytest
# Currently just used for the temporary hack to quit the phantomjs process
# see below in quit_driver.
import signal

import threading

import remi
import examples.widgets_overview_app as example_app

class ServerThread(threading.Thread):
    def run(self):
        self.server = remi.Server(example_app.MyApp, start=False, start_browser=False)
        self.server.start()

    def stop(self):
        self.server.stop()

class BrowserClient(object):
    """Interacts with a running instance of the application via animating a
    browser."""
    def __init__(self, browser="phantom"):
        """Note, dbfile is ignored here, this is really only for with AppClient"""
        driver_class = {
            'phantom': webdriver.PhantomJS,
            'chrome': webdriver.Chrome,
            'firefox': webdriver.Firefox
            }.get(browser)
        self.driver = driver_class()
        self.driver.set_window_size(1200, 760)


    def finalise(self):
        self.driver.close()
        # A bit of hack this but currently there is some bug I believe in
        # the phantomjs code rather than selenium, but in any case it means that
        # the phantomjs process is not being killed so we do so explicitly here
        # for the time being. Obviously we can remove this when that bug is
        # fixed. See: https://github.com/SeleniumHQ/selenium/issues/767
        self.driver.service.process.send_signal(signal.SIGTERM)
        self.driver.quit()


    def log_current_page(self, message=None, output_basename=None):
        content = self.driver.page_source
        if message:
            logging.info(message)
        # This is frequently what we really care about so I also output it
        # here as well to make it convenient to inspect (with highlighting).
        basename = output_basename or 'log-current-page'
        file_name = 'generated/{}.html'.format(basename)
        with open(file_name, 'w') as outfile:
            if message:
                outfile.write("<!-- {} --> ".format(message))
            outfile.write(content)
        filename = 'generated/{}.png'.format(basename)
        self.driver.save_screenshot(filename)

import time

def test_server():
    server_thread = ServerThread()
    # First start the server
    server_thread.start()

    client = BrowserClient()
    driver = client.driver

    try:
        driver.get("http://localhost:8081/")

        client.log_current_page(output_basename="before-button-click")

        label_element = driver.find_element_by_css_selector('#main-output-label')
        assert label_element.text == 'This is a LABEL!'

        element = driver.find_element_by_css_selector('button')
        element.click()
        label_element = driver.find_element_by_css_selector('#main-output-label')
        assert label_element.text == 'Button pressed!'

        file_menu = driver.find_element_by_css_selector('#file-menu-item')
        file_save_menu = driver.find_element_by_css_selector('#file-save-menu-item')
        file_save_save_menu = driver.find_element_by_css_selector('#file-save-save-menu-item')

        ActionChains(driver).move_to_element(file_menu)\
                            .move_to_element(file_save_menu)\
                            .click(file_save_save_menu)\
                            .perform()

        client.log_current_page(output_basename="after-button-click")
        label_element = driver.find_element_by_css_selector('#main-output-label')
        assert label_element.text == 'Menu clicked: Save'


    finally:
        client.finalise()
        server_thread.stop()
