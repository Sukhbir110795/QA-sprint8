import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import helper
import data
from page import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls, https=None):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        # Optional check
        if not helper.is_url_reachable(data.URBAN_ROUTES_URL):
            print('url is not reachable')
        else:
            print('url is reachable')

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.is_route_set()
    def test_order_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi()
        page.select_supportive_plan()
        assert "active" in self.driver.find_element(*page.active_tariff).get_attribute("class")

    def test_phone_authentication(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        # Assuming address is set and call taxi is clicked from previous tests if this were part of a full flow.
        # For standalone execution of this test, you might need to add these steps:
        # page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        # page.click_call_taxi()
        page.enter_phone(data.PHONE_NUMBER)
        code = helper.retrieve_phone_code(self.driver)
        page.enter_code(code)
        assert page.is_phone_authenticated()  # Assumes you have a method like this

    def test_add_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert page.is_card_added()  # Assumes you have a method like this

    def test_write_comment(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.write_comment(data.MESSAGE_FOR_DRIVER)
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
        page.write_comment(data.MESSAGE_FOR_DRIVER)
        page.place_order()
        assert page.is_car_search_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
