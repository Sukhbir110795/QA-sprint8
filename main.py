import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import helpers
import data
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        # Open the app URL
        cls.driver.get("https://cnt-159fc465-580d-4de5-9a1a-146a4fa61bf1.containerhub.tripleten-services.com/")

        # Optional check
        if not helpers.is_url_reachable():
            raise Exception("Urban Routes app is not reachable.")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_order_supportive_plan(self):
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.FROM_ADDRESS, data.TO_ADDRESS)
        page.click_call_taxi()
        page.select_supportive_plan()
        assert "active" in self.driver.find_element(*page.active_tariff).get_attribute("class")

    def test_phone_authentication(self):
        page = UrbanRoutesPage(self.driver)
        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_code(code)

    def test_add_card(self):
        page = UrbanRoutesPage(self.driver)
        page.add_card(data.CARD_NUMBER, data.CVV)

    def test_write_comment(self):
        page = UrbanRoutesPage(self.driver)
        page.write_comment(data.DRIVER_COMMENT)

    def test_blanket_selection(self):
        page = UrbanRoutesPage(self.driver)
        page.toggle_blanket()
        assert page.is_blanket_selected() is True

    def test_order_ice_cream(self):
        page = UrbanRoutesPage(self.driver)
        page.order_ice_cream()
        assert page.get_ice_cream_count() == "2"

    def test_final_order(self):
        page = UrbanRoutesPage(self.driver)
        page.write_comment(data.DRIVER_COMMENT)
        page.place_order()
        assert page.is_car_search_modal_visible()