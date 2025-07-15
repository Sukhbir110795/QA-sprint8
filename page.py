# pages.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # For simulating TAB key
import time # For small waits if necessary
import helpers # To access retrieve_phone_code
import data # To access test data

class UrbanRoutesPage:
    # URL of the application
    URL = data.BASE_URL

    # --- Locators ---
    # From address field
    FROM_ADDRESS_FIELD = (By.ID, "address-from")
    # To address field
    TO_ADDRESS_FIELD = (By.ID, "address-to")
    # Call a Taxi button
    CALL_TAXI_BUTTON = (By.CLASS_NAME, "button.button--ui-recommended-extra") # Adjust if needed
    # Supportive plan option
    SUPPORTIVE_PLAN_BUTTON = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[text()='Supportive']]")
    # Active supportive plan check (to verify selection)
    SUPPORTIVE_PLAN_ACTIVE = (By.XPATH, "//div[contains(@class, 'tcard_active') and .//div[text()='Supportive']]")

    # Phone number field (on the modal)
    PHONE_NUMBER_FIELD = (By.CLASS_NAME, "number") # This is the input field
    # Phone number entry button (to open phone modal)
    PHONE_NUMBER_BUTTON = (By.CLASS_NAME, "np-text") # Button that opens the phone input modal
    # Next button on phone modal
    NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")
    # SMS code input field
    SMS_CODE_INPUT = (By.ID, "code")
    # Confirm button for SMS code
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirm']")
    # Confirmed phone number display (to assert login)
    CONFIRMED_PHONE_NUMBER_DISPLAY = (By.CLASS_NAME, "number") # This might be the same as input, or a display element

    # Payment method button (e.g., "Cash")
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-text")
    # Add Card button on payment method modal
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-plus")
    # Card number input field
    CARD_NUMBER_INPUT = (By.ID, "number")
    # Card CVV input field
    CARD_CVV_INPUT = (By.ID, "code") # Note: This ID is reused, so context is important
    # Link button on add card modal
    LINK_BUTTON = (By.XPATH, "//button[text()='Link']")
    # Payment method display after adding card (should change to "Card")
    PAYMENT_METHOD_DISPLAY = (By.CLASS_NAME, "pp-text") # Should show "Card" after linking

    # Driver comment input field
    DRIVER_COMMENT_FIELD = (By.ID, "comment")

    # Blanket and Handkerchiefs slider/toggle
    BLANKET_HANDKERCHIEFS_TOGGLE = (By.CSS_SELECTOR, ".switch-input[type='checkbox']") # The actual checkbox input
    # Element to verify if blanket/handkerchiefs are selected (e.g., a visual indicator)
    # This might be a label, an icon, or a parent div with a specific class when active.
    # Adjust this locator based on your UI. Assuming a specific class on the parent div when active.
    BLANKET_HANDKERCHIEFS_ACTIVE_INDICATOR = (By.XPATH, "//div[contains(@class, 'r-header') and .//div[text()='Blanket and handkerchiefs']]/following-sibling::div//div[contains(@class, 'switch-input') and @checked]")


    # Ice cream counter increment button
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//div[contains(@class, 'counter-plus')]")
    # Ice cream counter display
    ICE_CREAM_COUNT_DISPLAY = (By.CLASS_NAME, "counter-value")

    # Order button (final confirmation)
    ORDER_BUTTON = (By.CLASS_NAME, "button.button--ui-cta") # Adjust if needed, e.g., "order-button"
    # Car search modal window (to assert its appearance)
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-button-text") # Assuming this class becomes visible on the modal

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # Initialize WebDriverWait

    def open(self):
        """Opens the Urban Routes application URL."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.FROM_ADDRESS_FIELD)) # Wait for page to load

    def set_address_from(self, address):
        """Sets the pickup address."""
        from_field = self.wait.until(EC.element_to_be_clickable(self.FROM_ADDRESS_FIELD))
        from_field.send_keys(address)
        # Wait for suggestions to appear and select the first one (or press ENTER)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "address-item"))) # Wait for suggestion
        from_field.send_keys(Keys.ENTER) # Select first suggestion

    def set_address_to(self, address):
        """Sets the destination address."""
        to_field = self.wait.until(EC.element_to_be_clickable(self.TO_ADDRESS_FIELD))
        to_field.send_keys(address)
        # Wait for suggestions to appear and select the first one (or press ENTER)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "address-item"))) # Wait for suggestion
        to_field.send_keys(Keys.ENTER) # Select first suggestion

    def get_address_from_value(self):
        """Retrieves the value from the 'from' address field."""
        return self.wait.until(EC.visibility_of_element_located(self.FROM_ADDRESS_FIELD)).get_attribute("value")

    def get_address_to_value(self):
        """Retrieves the value from the 'to' address field."""
        return self.wait.until(EC.visibility_of_element_located(self.TO_ADDRESS_FIELD)).get_attribute("value")

    def click_call_taxi_button(self):
        """Clicks the 'Call a Taxi' button."""
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        """Selects the 'Supportive' tariff plan."""
        # Check if supportive plan is already active to avoid unnecessary clicks
        try:
            self.wait.until(EC.presence_of_element_located(self.SUPPORTIVE_PLAN_ACTIVE))
            print("Supportive plan is already active.")
        except:
            # If not active, click the button
            self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_BUTTON)).click()
            self.wait.until(EC.presence_of_element_located(self.SUPPORTIVE_PLAN_ACTIVE)) # Wait for it to become active

    def get_selected_plan_text(self):
        """Retrieves the text of the currently selected plan."""
        # This assumes the active plan has a specific class or structure that contains its text
        return self.wait.until(EC.visibility_of_element_located(self.SUPPORTIVE_PLAN_ACTIVE)).text

    def enter_phone_number_and_confirm(self, phone_number):
        """Enters phone number, retrieves SMS code, and confirms."""
        # Click the button to open the phone number input modal
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NUMBER_BUTTON)).click()

        # Enter phone number
        phone_field = self.wait.until(EC.visibility_of_element_located(self.PHONE_NUMBER_FIELD))
        phone_field.send_keys(phone_number)

        # Click Next
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

        # Retrieve SMS code using helper function
        sms_code = helpers.retrieve_phone_code(self.driver)
        if sms_code:
            # Enter SMS code
            sms_input = self.wait.until(EC.visibility_of_element_located(self.SMS_CODE_INPUT))
            sms_input.send_keys(sms_code)
            # Click Confirm
            self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()
            self.wait.until(EC.invisibility_of_element_located(self.SMS_CODE_INPUT)) # Wait for modal to close
        else:
            raise Exception("Could not retrieve SMS confirmation code.")

    def get_phone_number_display(self):
        """Retrieves the displayed phone number after confirmation."""
        # This might be the same element as the input field, or a read-only display
        return self.wait.until(EC.visibility_of_element_located(self.CONFIRMED_PHONE_NUMBER_DISPLAY)).text

    def add_credit_card(self, card_number, cvv):
        """Adds a credit card as a payment method."""
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()

        # Switch to the iframe if the card input is in an iframe
        # This is a common pattern for payment forms. Adjust if your app doesn't use an iframe.
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-input__iframe")))
            self.driver.switch_to.frame(iframe)
        except:
            print("No iframe found for card input, proceeding without switching.")
            pass # No iframe, continue

        card_num_field = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        card_num_field.send_keys(card_number)

        cvv_field = self.wait.until(EC.visibility_of_element_located(self.CARD_CVV_INPUT))
        cvv_field.send_keys(cvv)

        # Simulate TAB or click outside to change focus from CVV
        cvv_field.send_keys(Keys.TAB) # Simulate pressing TAB
        # Or alternatively, click on a neutral background element
        # self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5) # Small wait to ensure focus change registers

        # Switch back to default content if you switched to an iframe
        try:
            self.driver.switch_to.default_content()
        except:
            pass # Was not in an iframe, no need to switch back

        # Click the Link button (it should now be clickable)
        link_button = self.wait.until(EC.element_to_be_clickable(self.LINK_BUTTON))
        link_button.click()
        self.wait.until(EC.invisibility_of_element_located(self.LINK_BUTTON)) # Wait for modal to close

    def get_payment_method_text(self):
        """Retrieves the text of the selected payment method."""
        return self.wait.until(EC.visibility_of_element_located(self.PAYMENT_METHOD_DISPLAY)).text

    def enter_driver_comment(self, comment):
        """Enters a comment for the driver."""
        comment_field = self.wait.until(EC.element_to_be_clickable(self.DRIVER_COMMENT_FIELD))
        comment_field.send_keys(comment)

    def get_driver_comment_value(self):
        """Retrieves the value from the driver comment field."""
        return self.wait.until(EC.visibility_of_element_located(self.DRIVER_COMMENT_FIELD)).get_attribute("value")

    def toggle_blanket_handkerchiefs(self):
        """Toggles the 'Blanket and Handkerchiefs' option."""
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_HANDKERCHIEFS_TOGGLE)).click()

    def is_blanket_handkerchiefs_checked(self):
        """Checks if the 'Blanket and Handkerchiefs' option is checked."""
        # Check the 'checked' property of the input element
        checkbox = self.wait.until(EC.presence_of_element_located(self.BLANKET_HANDKERCHIEFS_TOGGLE))
        return checkbox.get_property('checked')

    def add_ice_cream(self, count):
        """Adds a specified number of ice creams."""
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)).click()
            time.sleep(0.2) # Small wait to ensure counter updates

    def get_ice_cream_count(self):
        """Retrieves the displayed count of ice creams."""
        count_element = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_COUNT_DISPLAY))
        return int(count_element.text)

    def click_order_button(self):
        """Clicks the final 'Order' button."""
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def is_car_search_modal_displayed(self):
        """Checks if the car search modal window is displayed."""
        try:
            return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL)).is_displayed()
        except:
            return False # Modal not found or not visible