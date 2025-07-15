import data

def test_full_order_flow(self):
    page = self.page
    page.set_address(data.FROM_ADDRESS, data.TO_ADDRESS)
    page.click_call_taxi()
    page.select_supportive_plan()
    page.enter_phone_number(data.PHONE_NUMBER)
    code = retrieve_phone_code()
    page.enter_sms_code(code)
    page.add_credit_card(data.CARD_NUMBER, data.CVV_CODE)
    page.leave_driver_comment(data.DRIVER_COMMENT)
    page.order_blanket_and_handkerchiefs()
    page.order_ice_cream(count=data.ICE_CREAM_COUNT)
    page.submit_order()
    assert page.is_car_search_modal_displayed()
