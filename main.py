import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import helpers
import data
from page import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls, https=None):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        # Open the app URL
        cls.driver.get('https://cnt-70092a2f-fa12-4701-87d1-b9abaa82b1aa.containerhub.tripleten-services.com/')

        # Optional check
        if not helpers.is_url_reachable():
            raise Exception("Urban Routes app is not reachable.")

    def test_order_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.FROM_ADDRESS, data.TO_ADDRESS)
        page.click_call_taxi()
        page.select_supportive_plan()
        assert "active" in self.driver.find_element(*page.active_tariff).get_attribute("class")

    def test_phone_authentication(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_phone(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.enter_code(code)
        assert page.is_phone_authenticated()  # Assumes you have a method like this

    def test_add_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.add_card(data.CARD_NUMBER, data.CVV)
        assert page.is_card_added()  # Assumes you have a method like this

    def test_write_comment(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.write_comment(data.DRIVER_COMMENT)
        assert page.is_comment_saved()  # Assumes you have a method like this

    def test_blanket_selection(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.toggle_blanket()
        assert page.is_blanket_selected() is True

    def test_order_ice_cream(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.order_ice_cream()
        assert page.get_ice_cream_count() == "2"

    def test_final_order(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.write_comment(data.DRIVER_COMMENT)
        page.place_order()
        assert page.is_car_search_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
