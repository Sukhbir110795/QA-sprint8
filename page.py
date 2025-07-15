
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_address(self, from_address, to_address):
        from_input = self.wait.until(EC.presence_of_element_located((By.ID, "from")))
        from_input.clear()
        from_input.send_keys(from_address)

        to_input = self.driver.find_element(By.ID, "to")
        to_input.clear()
        to_input.send_keys(to_address)

    def click_call_taxi(self):
        call_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "order")))
        call_button.click()

    def select_supportive_plan(self):
        plans = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tcard")))
        for plan in plans:
            if "Supportive" in plan.text and "active" not in plan.get_attribute("class"):
                plan.click()
                break

    def enter_phone_number(self, phone):
        phone_field = self.wait.until(EC.presence_of_element_located((By.ID, "phone")))
        phone_field.clear()
        phone_field.send_keys(phone)

    def enter_sms_code(self, code):
        code_field = self.wait.until(EC.presence_of_element_located((By.ID, "code")))
        code_field.clear()
        code_field.send_keys(code)

    def add_credit_card(self, card_number, cvv):
        self.driver.find_element(By.CLASS_NAME, "payment-method").click()
        self.driver.find_element(By.CLASS_NAME, "add-card").click()

        card_input = self.wait.until(EC.presence_of_element_located((By.ID, "number")))
        card_input.send_keys(card_number)

        code_input = self.driver.find_element(By.ID, "code")
        code_input.send_keys(cvv)
        code_input.send_keys(Keys.TAB)

        link_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "link")))
        link_button.click()

        method = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "payment-method")))
        assert "Card" in method.text

    def leave_driver_comment(self, comment):
        comment_input = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "comment-input")))
        comment_input.clear()
        comment_input.send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        toggle = self.driver.find_element(By.ID, "blanket" if self.driver.find_element(By.ID, "blanket").is_displayed() else "default")
        if not toggle.get_property("checked"):
            toggle.click()
            assert toggle.get_property("checked") == True

    def order_ice_cream(self, count):
        ice_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ice-cream-add")))
        for _ in range(count):
            ice_button.click()
        ice_count = self.driver.find_element(By.CLASS_NAME, "ice-cream-count").text
        assert int(ice_count) == count

    def submit_order(self):
        order_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit")))
        order_btn.click()

    def is_car_search_modal_displayed(self):
        modal = self.wait.until(EC.visibility_of_element_located((By.ID, "car-search")))
        return modal.is_displayed()
