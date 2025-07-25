from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    # === LOCATORS ===
    from_input = (By.ID, "from")
    to_input = (By.ID, "to")
    call_taxi_btn = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    supportive_plan = (
        By.XPATH, "//div[contains(@class, 'tcard') and .//div[text()='Supportive']]"
    )
    active_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and contains(@class, 'active')]")

    phone_field = (By.ID, "phone")
    code_field = (By.ID, "code")
    payment_button = (By.XPATH, "//button[contains(@class, 'payment__button')]")
    add_card_btn = (By.XPATH, "//button[contains(@class, 'add-card')]")
    card_number = (By.ID, "number")
    card_code = (By.XPATH, "//input[contains(@placeholder, 'CVV')]")
    link_btn = (By.XPATH, "//button[contains(@class, 'card-add__button')]")

    comment_box = (By.XPATH, "//textarea[contains(@class, 'order-comment')]")
    blanket_slider = (By.ID, "blanket")
    ice_cream_btn = (By.XPATH, "//button[contains(@class, 'ice-cream')]")
    ice_cream_counter = (By.CLASS_NAME, "counter__count")
    order_btn = (By.XPATH, "//button[contains(@class, 'order-confirm')]")
    modal_popup = (By.CLASS_NAME, "search-popup")

    # === METHODS ===
    def set_address(self, from_addr, to_addr):
        self.driver.find_element(*self.from_input).send_keys(from_addr)
        self.driver.find_element(*self.to_input).send_keys(to_addr)

    def click_call_taxi(self):
        self.driver.find_element(*self.call_taxi_btn).click()

    def select_supportive_plan(self):
        elem = self.driver.find_element(*self.supportive_plan)
        if "active" not in elem.get_attribute("class"):
            elem.click()

    def enter_phone(self, phone):
        self.driver.find_element(*self.phone_field).send_keys(phone)

    def enter_code(self, code):
        self.driver.find_element(*self.code_field).send_keys(code)

    def add_card(self, number, cvv):
        self.driver.find_element(*self.payment_button).click()
        self.driver.find_element(*self.add_card_btn).click()
        self.driver.find_element(*self.card_number).send_keys(number)
        cvv_input = self.driver.find_element(*self.card_code)
        cvv_input.send_keys(cvv)
        cvv_input.send_keys(Keys.TAB)
        self.driver.find_element(*self.link_btn).click()

    def write_comment(self, message):
        box = self.driver.find_element(*self.comment_box)
        box.clear()
        box.send_keys(message)

    def toggle_blanket(self):
        self.driver.find_element(*self.blanket_slider).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.blanket_slider).get_property("checked")

    def order_ice_cream(self, times=2):
        for _ in range(times):
            self.driver.find_element(*self.ice_cream_btn).click()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter).text

    def place_order(self):
        self.driver.find_element(*self.order_btn).click()

    def is_car_search_modal_visible(self):
        return self.driver.find_element(*self.modal_popup).is_displayed()

    # === ASSERTION HELPERS (OPTIONAL) ===
    def is_phone_authenticated(self):
        return "authenticated" in self.driver.page_source

    def is_card_added(self):
        return "Card added" in self.driver.page_source or "linked" in self.driver.page_source

    def is_comment_saved(self):
        return self.driver.find_element(*self.comment_box).get_attribute("value") != ""

    def is_route_set(self):
        pass
