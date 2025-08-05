import time

from page_objects.locators.e2e_locators.e2e_locators import E2ELocators
import utils.data_utils
from utils.logger_utils import get_logger

logger = get_logger()

class E2EPage:
    def __init__(self, page):
        self.page = page
        logger.debug("E2E Page initialized")

    def order_placement(self):
        try:
            logger.info("Starting registered user order placement")
            email_id = utils.data_utils.random_email()
            password = utils.data_utils.random_password()
            card = utils.data_utils.load_card_details()

            self.page.click(E2ELocators.CLOSE_POPUP)
            self.page.click(E2ELocators.SIGNIN_BUTTON)
            self.page.click(E2ELocators.CREATE_ACCOUNT_BTN)

            self.page.fill(E2ELocators.SIGNUP_EMAIL, email_id)
            self.page.click(E2ELocators.CONTINUE_BTN)
            self.page.fill(E2ELocators.FIRST_NAME_INPUT, utils.data_utils.random_first_name())
            self.page.fill(E2ELocators.LAST_NAME_INPUT, utils.data_utils.random_last_name())
            self.page.fill(E2ELocators.PHONE_NUMBER_INPUT, utils.data_utils.generate_us_mobile_number())
            self.page.fill(E2ELocators.PASSWORD_INPUT, password)
            self.page.fill(E2ELocators.CONFIRM_PASSWORD_INPUT, password)
            self.page.click(E2ELocators.FINAL_CONTINUE_BTN)

            self.page.locator(E2ELocators.BIRTH_MONTH_DROPDOWN).click()
            self.page.locator(E2ELocators.January_DROPDOWN).click()
            self.page.locator(E2ELocators.BIRTH_DAY_DROPDOWN).click()
            self.page.locator(E2ELocators.Date_DROPDOWN).click()

            self.page.click(E2ELocators.COMPLETE_SIGN_UP_BTN)
            self.page.locator(E2ELocators.Confirm_Birthday_btn).click()
            self.page.click(E2ELocators.SKIP_BTN)

            self.page.click(E2ELocators.START_ORDER)
            self.page.fill(E2ELocators.SEARCH_TEXT, "roswell")
            self.page.click(E2ELocators.LOCATION_TEXT)
            self.page.click(E2ELocators.SELECT_LOCATION)

            if self.page.locator(E2ELocators.ORDER_FOR_LATER_BTN).is_visible(timeout=3000):
                logger.info("Store is closed — proceeding with 'Order for Later'")
                self.page.click(E2ELocators.ORDER_FOR_LATER_BTN)
                self.page.click(E2ELocators.ORDER_INFO_CONFIRM_BTN)
                self.page.click(E2ELocators.MENU_NAV_LINK)
            else:
                logger.info("Store is open — redirected to homepage")

            self.page.click(E2ELocators.BEVERAGES_CATEGORY)
            self.page.click(E2ELocators.PEACH_MANGO_TEA_GALLON_TILE)
            self.page.wait_for_selector(E2ELocators.ADD_CART, timeout=5000)
            self.page.click(E2ELocators.ADD_CART)
            time.sleep(10)

            self.page.wait_for_selector(E2ELocators.CART_ICON, timeout=5000)
            self.page.click(E2ELocators.CART_ICON)

            self.page.wait_for_selector(E2ELocators.CHECKOUT_BUTTON, timeout=10000)
            self.page.click(E2ELocators.CHECKOUT_BUTTON)
            time.sleep(15)

            self.page.wait_for_selector(E2ELocators.CREDIT_CARD_RADIO, timeout=5000)
            self.page.click(E2ELocators.CREDIT_CARD_RADIO)
            time.sleep(10)
            self.page.wait_for_selector(E2ELocators.CARD_NUMBER_INPUT, timeout=10000)
            self.page.fill(E2ELocators.CARD_NUMBER_INPUT, card["number"])
            self.page.fill(E2ELocators.EXPIRATION_DATE_INPUT, card["expiration_year_month"])
            self.page.fill(E2ELocators.CVV_INPUT, card["cvv"])
            self.page.fill(E2ELocators.POSTAL_CODE_INPUT, card["postal_code"])

            logger.info("Order placed successfully")

        except Exception as e:
            logger.exception(f"Order not placed: {str(e)}")
            raise

    def order_placement_guest(self):
        try:
            logger.info("Starting guest user order placement")
            card = utils.data_utils.load_card_details()

            self.page.click(E2ELocators.CLOSE_POPUP)
            self.page.click(E2ELocators.SIGNIN_BUTTON)
            self.page.click(E2ELocators.CONTINUE_AS_GUEST_BUTTON)

            self.page.click(E2ELocators.START_ORDER)
            self.page.fill(E2ELocators.SEARCH_TEXT, "roswell")
            self.page.click(E2ELocators.LOCATION_TEXT)
            self.page.click(E2ELocators.SELECT_LOCATION)

            if self.page.locator(E2ELocators.ORDER_FOR_LATER_BTN).is_visible(timeout=3000):
                logger.info("Store is closed — proceeding with 'Order for Later'")
                self.page.click(E2ELocators.ORDER_FOR_LATER_BTN)
                self.page.click(E2ELocators.ORDER_INFO_CONFIRM_BTN)
            else:
                logger.info("Store is open — redirected to homepage")

            self.page.click(E2ELocators.BEVERAGES_CATEGORY)
            self.page.click(E2ELocators.PEACH_MANGO_TEA_GALLON_TILE)
            self.page.wait_for_selector(E2ELocators.ADD_CART, timeout=5000)
            self.page.click(E2ELocators.ADD_CART)

            self.page.wait_for_selector(E2ELocators.CART_ICON, timeout=5000)
            self.page.click(E2ELocators.CART_ICON)
            self.page.wait_for_selector(E2ELocators.CHECKOUT_BUTTON, timeout=5000)
            self.page.click(E2ELocators.CHECKOUT_BUTTON)

            logger.info("Guest checkout completed up to payment screen")

        except Exception as e:
            logger.exception(f"Order not placed: {str(e)}")
            raise
