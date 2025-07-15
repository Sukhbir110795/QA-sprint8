import sys
import os
sys.path.append(os.path.dirname(__file__))

import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code, is_url_reachable

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        server_url = "https://cnt-59c08492-c002-4ce8-91fe-2d43434e2332.containerhub.tripleten-services.com"
        if not is_url_reachable(server_url):
            raise Exception("Server is not reachable")

        cls.driver.get(server_url)
        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_full_order_flow(self):
        page = self.page
        page.set_address("123 Main St", "456 Elm St")
        page.click_call_taxi()
        page.select_supportive_plan()
        page.enter_phone_number("+1234567890")
        code = retrieve_phone_code()
        page.enter_sms_code(code)
        page.add_credit_card("4242 4242 4242 4242", "123")
        page.leave_driver_comment("Please be quick and friendly.")
        page.order_blanket_and_handkerchiefs()
        page.order_ice_cream(count=2)
        page.submit_order()
        assert page.is_car_search_modal_displayed()
