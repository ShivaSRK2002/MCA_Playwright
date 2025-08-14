import time
from page_objects.locators.e2e_locators.moes_e2e_locators import MoesE2ELocators
import utils.data_utils
from utils.logger_utils import get_logger
logger = get_logger()

class MoesE2EPage:
    def __init__(self, page):
        self.page = page
        logger.debug("Moes E2E Page initialized")

    def order_placement(self):
        try:
            logger.info("Starting registered user order placement")

            # --- Generate test data ---
            email = utils.data_utils.random_email()
            password = utils.data_utils.random_password()
            card = utils.data_utils.load_card_details()
            logger.debug(f"Generated Email: {email}")
            logger.debug(f"Card ends with: {card['number'][-4:]}")

            # --- Sign up flow ---
            email = utils.data_utils.random_email()
            first_name = utils.data_utils.random_first_name()
            last_name = utils.data_utils.random_last_name()
            phone_number = utils.data_utils.generate_us_mobile_number()
            logger.info("Starting guest user order placement")
            card = utils.data_utils.load_card_details()
            
            self.page.click(MoesE2ELocators.SIGN_IN_BUTTON)
            self.page.click(MoesE2ELocators.CREATE_ACCOUNT_BTN)

            logger.info("Filling account creation form")
            self.page.fill(MoesE2ELocators.EMAIL_INPUT, email)
            self.page.click(MoesE2ELocators.CONTINUE_BTN)
            self.page.fill(MoesE2ELocators.FIRST_NAME_INPUT, utils.data_utils.random_first_name())
            self.page.fill(MoesE2ELocators.LAST_NAME_INPUT, utils.data_utils.random_last_name())
            self.page.fill(MoesE2ELocators.PHONE_NUMBER_INPUT, utils.data_utils.generate_us_mobile_number())
            self.page.fill(MoesE2ELocators.PASSWORD_INPUT, password)
            self.page.fill(MoesE2ELocators.CONFIRM_PASSWORD_INPUT, password)
            self.page.click(MoesE2ELocators.FINAL_CONTINUE_BTN)

            logger.info("Selecting DOB")
            self.page.locator(MoesE2ELocators.BIRTH_MONTH_DROPDOWN).click()
            self.page.locator(MoesE2ELocators.January_DROPDOWN).click()
            self.page.locator(MoesE2ELocators.BIRTH_DAY_DROPDOWN).click()
            self.page.locator(MoesE2ELocators.Date_DROPDOWN).click()
            self.page.click(MoesE2ELocators.COMPLETE_SIGN_UP_BTN)
            self.page.locator(MoesE2ELocators.CONFIRM_BIRTHDAY_BTN).click()
            self.page.click(MoesE2ELocators.SKIP_BTN)
            try:
                self.page.wait_for_selector('#truyo-consent-module', state='visible', timeout=10000)
                self.page.wait_for_selector('#acceptAllCookieButton', state='visible', timeout=5000)
                self.page.click('#acceptAllCookieButton')
            except:
                self.page.click('#acceptAllCookieButton', force=True)

            logger.info("Waiting for and clicking Start Order")
            self.page.locator(MoesE2ELocators.START_ORDER).wait_for(state="visible", timeout=10000)
            self.page.locator(MoesE2ELocators.START_ORDER).click()

            logger.info("Waiting for store search input and filling address: 'Guam'")
            self.page.locator(MoesE2ELocators.SEARCH_TEXT).wait_for(state="visible", timeout=10000)
            self.page.fill(MoesE2ELocators.SEARCH_TEXT, "Guam")

            logger.info("Waiting for and clicking address from suggestions")
            self.page.locator(MoesE2ELocators.SELECT_ADDRESS_BTN).first.wait_for(state="visible", timeout=10000)
            self.page.locator(MoesE2ELocators.SELECT_ADDRESS_BTN).first.click()

            logger.info("Waiting for and selecting location")
            self.page.locator(MoesE2ELocators.SELECT_LOCATION).first.wait_for(state="visible", timeout=10000)
            self.page.locator(MoesE2ELocators.SELECT_LOCATION).first.click()

            logger.info("Waiting for and clicking Beverages category")
            self.page.wait_for_selector(MoesE2ELocators.BEVERAGES_CATEGORY, timeout=10000)
            self.page.click(MoesE2ELocators.BEVERAGES_CATEGORY)

            logger.info("Waiting for and clicking Regular Fountain Drink tile")
            self.page.wait_for_selector(MoesE2ELocators.REGULAR_FOUNTAIN_DRINK_TILE, timeout=10000)
            time.sleep(2)
            self.page.click(MoesE2ELocators.REGULAR_FOUNTAIN_DRINK_TILE)
            
            logger.info("Waiting for Add to Cart button to appear after drink click")
            self.page.wait_for_selector(MoesE2ELocators.ADD_CART, timeout=15000)
            time.sleep(2)  # Let UI settle after click

            logger.info("Clicking Add to Cart")
            self.page.click(MoesE2ELocators.ADD_CART)
            time.sleep(5)  # Let UI settle after adding to cart
            self.page.locator(".globalPageLoader").wait_for(state="detached", timeout=10000)

            # Also wait for any open drawer to close
            self.page.locator(".drawerWrapper.drawerOpen").wait_for(state="hidden", timeout=10000)
            logger.info("Waiting for and clicking Cart icon")
            self.page.wait_for_selector(MoesE2ELocators.CART_ICON, timeout=10000)            
            self.page.click(MoesE2ELocators.CART_ICON)
            time.sleep(10)  # Wait for cart to open


            logger.info("Scrolling to bottom of the page before clicking Checkout button")
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            logger.info("Waiting for and clicking Checkout button")
            checkout_button = self.page.locator(MoesE2ELocators.CHECKOUT_BUTTON)
            checkout_button.wait_for(timeout=10000)
            checkout_button.click()
            time.sleep(5)  # Let UI settle after click

            
            # Step 1: Click credit card radio
            self.page.wait_for_selector(MoesE2ELocators.CREDIT_CARD_RADIO, timeout=5000)
            time.sleep(5)
            self.page.click(MoesE2ELocators.CREDIT_CARD_RADIO)
            time.sleep(10)

            # Step 2: Switch to FreedomPay iframe
            payment_frame = self.page.frame_locator('iframe#hpc--card-frame')

            # Step 3: Interact with input fields inside iframe
            card_number_input = payment_frame.locator("#CardNumber")
            expiration_input = payment_frame.locator("#ExpirationDate")
            cvv_input = payment_frame.locator("#SecurityCode")
            postal_code_input = payment_frame.locator("#PostalCode")

            # Step 4: Wait and fill each field
            card_number_input.wait_for(timeout=8000)
            card_number_input.scroll_into_view_if_needed()
            card_number_input.fill(card["number"])
            time.sleep(1)

            expiration_input.scroll_into_view_if_needed()
            expiration_input.fill(card["expiration_year_month"])
            time.sleep(1)

            cvv_input.scroll_into_view_if_needed()
            cvv_input.fill(card["cvv"])
            time.sleep(1)

            postal_code_input.scroll_into_view_if_needed()
            postal_code_input.fill(card["postal_code"])
            time.sleep(10)

            payment_frame.locator(MoesE2ELocators.SAVE_BUTTON).click()

            self.page.wait_for_timeout(5000)  # Wait for payment processing
            self.page.click(MoesE2ELocators.PLACE_ORDER_BUTTON)
            time.sleep(10)
            
        except Exception as e:
            logger.exception(f"Order placement failed: {e}")
            raise

    def order_placement_guest(self):
        try:
            email = utils.data_utils.random_email()
            first_name = utils.data_utils.random_first_name()
            last_name = utils.data_utils.random_last_name()
            phone_number = utils.data_utils.generate_us_mobile_number()
            logger.info("Starting guest user order placement")
            card = utils.data_utils.load_card_details()

            logger.info("Waiting for and clicking Sign In button")
            self.page.wait_for_selector(MoesE2ELocators.SIGN_IN_BUTTON, timeout=10000)
            self.page.click(MoesE2ELocators.SIGN_IN_BUTTON)
            

            logger.info("Waiting for and clicking Continue as Guest")
            self.page.wait_for_selector(MoesE2ELocators.CONTINUE_AS_GUEST_BUTTON, timeout=10000)
            self.page.click(MoesE2ELocators.CONTINUE_AS_GUEST_BUTTON)   
            try:
                self.page.wait_for_selector('#truyo-consent-module', state='visible', timeout=10000)
                self.page.wait_for_selector('#acceptAllCookieButton', state='visible', timeout=5000)
                self.page.click('#acceptAllCookieButton')
            except:
                self.page.click('#acceptAllCookieButton', force=True)        

            logger.info("Waiting for and clicking Start Order")
            self.page.locator(MoesE2ELocators.START_ORDER).wait_for(state="visible", timeout=10000)
            self.page.locator(MoesE2ELocators.START_ORDER).click()

            logger.info("Waiting for store search input and filling address: 'Guam'")

            self.page.locator(MoesE2ELocators.SEARCH_TEXT).wait_for(state="visible", timeout=10000)
            self.page.fill(MoesE2ELocators.SEARCH_TEXT, "Guam")

            logger.info("Waiting for and clicking address from suggestions")
            self.page.locator(MoesE2ELocators.SELECT_ADDRESS_BTN).first.wait_for(state="visible", timeout=10000)
            self.page.locator(MoesE2ELocators.SELECT_ADDRESS_BTN).first.click()

            logger.info("Waiting for and selecting location")
            self.page.locator(MoesE2ELocators.SELECT_LOCATION).first.wait_for(state="visible", timeout=10000)
            self.page.locator(MoesE2ELocators.SELECT_LOCATION).first.click()

            logger.info("Waiting for and clicking Beverages category")
            self.page.wait_for_selector(MoesE2ELocators.BEVERAGES_CATEGORY, timeout=10000)
            self.page.click(MoesE2ELocators.BEVERAGES_CATEGORY)

            logger.info("Waiting for and clicking Regular Fountain Drink tile")
            self.page.wait_for_selector(MoesE2ELocators.REGULAR_FOUNTAIN_DRINK_TILE, timeout=10000)
            time.sleep(2)
            self.page.click(MoesE2ELocators.REGULAR_FOUNTAIN_DRINK_TILE)
            
            logger.info("Waiting for Add to Cart button to appear after drink click")
            self.page.wait_for_selector(MoesE2ELocators.ADD_CART, timeout=15000)
            time.sleep(2)  # Let UI settle after click

            logger.info("Clicking Add to Cart")
            self.page.click(MoesE2ELocators.ADD_CART)
            time.sleep(5)  # Let UI settle after adding to cart
            self.page.locator(".globalPageLoader").wait_for(state="detached", timeout=10000)

            # Also wait for any open drawer to close
            self.page.locator(".drawerWrapper.drawerOpen").wait_for(state="hidden", timeout=10000)
            logger.info("Waiting for and clicking Cart icon")
            self.page.wait_for_selector(MoesE2ELocators.CART_ICON, timeout=10000)            
            self.page.click(MoesE2ELocators.CART_ICON)
            
            logger.info("Scrolling to bottom of the page before clicking Checkout button")
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            logger.info("Waiting for and clicking Checkout button")
            checkout_button = self.page.locator(MoesE2ELocators.CHECKOUT_BUTTON)
            checkout_button.wait_for(timeout=10000)
            checkout_button.click()

            # Optionally wait for the checkout page to load or settle
            self.page.wait_for_timeout(5000)

            self.page.fill(MoesE2ELocators.CHECKOUT_FIRSTNAME_INPUT, first_name)
            self.page.fill(MoesE2ELocators.CHECKOUT_LASTNAME_INPUT, last_name)
            self.page.fill(MoesE2ELocators.CHECKOUT_EMAIL_INPUT, email)
            self.page.fill(MoesE2ELocators.CHECKOUT_PHONE_INPUT, phone_number)
            # Step 1: Click credit card radio
            self.page.wait_for_selector(MoesE2ELocators.CREDIT_CARD_RADIO, timeout=5000)
            time.sleep(5)
            self.page.click(MoesE2ELocators.CREDIT_CARD_RADIO)
            time.sleep(10)

            # Step 2: Switch to FreedomPay iframe
            payment_frame = self.page.frame_locator('iframe#hpc--card-frame')

            # Step 3: Interact with input fields inside iframe
            card_number_input = payment_frame.locator("#CardNumber")
            expiration_input = payment_frame.locator("#ExpirationDate")
            cvv_input = payment_frame.locator("#SecurityCode")
            postal_code_input = payment_frame.locator("#PostalCode")

            # Step 4: Wait and fill each field
            card_number_input.wait_for(timeout=8000)
            card_number_input.scroll_into_view_if_needed()
            card_number_input.fill(card["number"])
            time.sleep(1)

            expiration_input.scroll_into_view_if_needed()
            expiration_input.fill(card["expiration_year_month"])
            time.sleep(1)

            cvv_input.scroll_into_view_if_needed()
            cvv_input.fill(card["cvv"])
            time.sleep(1)

            postal_code_input.scroll_into_view_if_needed()
            postal_code_input.fill(card["postal_code"])
            time.sleep(10)

            payment_frame.locator(MoesE2ELocators.SAVE_BUTTON).click()

            self.page.wait_for_timeout(5000)  # Wait for payment processing
            self.page.click(MoesE2ELocators.PLACE_ORDER_BUTTON)
            time.sleep(10)

        except Exception as e:
            logger.exception(f"Order not placed: {str(e)}")
            raise

    def order_placement_signed_in(self):
        try:
            email = utils.data_utils.random_email()
            first_name = utils.data_utils.random_first_name()
            last_name = utils.data_utils.random_last_name()
            phone_number = utils.data_utils.generate_us_mobile_number()
            logger.info("Starting guest user order placement")
            card = utils.data_utils.load_card_details()

            logger.info("Waiting for and clicking Sign In button")
            logger.info("Waiting for and clicking Sign In button")
            self.page.click(MoesE2ELocators.SIGN_IN_BUTTON)
            time.sleep(2)
            self.page.click(MoesE2ELocators.SIGN_IN_BUTTON)
            self.page.fill(MoesE2ELocators.EMAIL_INPUT, 'q1@gmail.com')
            self.page.fill(MoesE2ELocators.PASSWORD_INPUT, 'Test@123')
            self.page.click(MoesE2ELocators.SIGN_IN_BUTTON_USER)
           
            try:
                self.page.wait_for_selector('#truyo-consent-module', state='visible', timeout=10000)
                self.page.wait_for_selector('#acceptAllCookieButton', state='visible', timeout=5000)
                self.page.click('#acceptAllCookieButton')
            except:
                self.page.click('#acceptAllCookieButton', force=True)     
            
            self.page.click(MoesE2ELocators.MENU_NAV_LINK)
            time.sleep(2)      

            logger.info("Waiting for and clicking Beverages category")
            self.page.wait_for_selector(MoesE2ELocators.BEVERAGES_CATEGORY, timeout=10000)
            self.page.click(MoesE2ELocators.BEVERAGES_CATEGORY)

            logger.info("Waiting for and clicking Regular Fountain Drink tile")
            self.page.wait_for_selector(MoesE2ELocators.REGULAR_FOUNTAIN_DRINK_TILE, timeout=10000)
            time.sleep(2)
            self.page.click(MoesE2ELocators.REGULAR_FOUNTAIN_DRINK_TILE)
            
            logger.info("Waiting for Add to Cart button to appear after drink click")
            self.page.wait_for_selector(MoesE2ELocators.ADD_CART, timeout=15000)
            time.sleep(2)  # Let UI settle after click

            logger.info("Clicking Add to Cart")
            self.page.click(MoesE2ELocators.ADD_CART)
            time.sleep(5)  # Let UI settle after adding to cart
            self.page.locator(".globalPageLoader").wait_for(state="detached", timeout=10000)

        # Wait for any open drawer to close before clicking cart icon
            drawer_locator = self.page.locator(".drawerWrapper.drawerOpen")
            if drawer_locator.is_visible():
                # Close the drawer
                close_button = drawer_locator.locator(".drawerCloseBtn")
                close_button.click()
                drawer_locator.wait_for(state="detached", timeout=5000)

            # Now click the cart icon safely
            self.page.locator(MoesE2ELocators.CART_ICON).click()




            
            time.sleep(10)

            logger.info("Scrolling to bottom of the page before clicking Checkout button")
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            logger.info("Waiting for and clicking Checkout button")
            checkout_button = self.page.locator(MoesE2ELocators.CHECKOUT_BUTTON)
            checkout_button.wait_for(timeout=10000)
            checkout_button.click()

            # Optionally wait for the checkout page to load or settle
            self.page.wait_for_timeout(5000)

            # Step 1: Click credit card radio
            self.page.wait_for_selector(MoesE2ELocators.CREDIT_CARD_RADIO, timeout=5000)
            time.sleep(5)
            self.page.click(MoesE2ELocators.CREDIT_CARD_RADIO)
            time.sleep(10)

            # Step 2: Switch to FreedomPay iframe
            payment_frame = self.page.frame_locator('iframe#hpc--card-frame')

            # Step 3: Interact with input fields inside iframe
            card_number_input = payment_frame.locator("#CardNumber")
            expiration_input = payment_frame.locator("#ExpirationDate")
            cvv_input = payment_frame.locator("#SecurityCode")
            postal_code_input = payment_frame.locator("#PostalCode")

            # Step 4: Wait and fill each field
            card_number_input.wait_for(timeout=8000)
            card_number_input.scroll_into_view_if_needed()
            card_number_input.fill(card["number"])
            time.sleep(1)

            expiration_input.scroll_into_view_if_needed()
            expiration_input.fill(card["expiration_year_month"])
            time.sleep(1)

            cvv_input.scroll_into_view_if_needed()
            cvv_input.fill(card["cvv"])
            time.sleep(1)

            postal_code_input.scroll_into_view_if_needed()
            postal_code_input.fill(card["postal_code"])
            time.sleep(10)

            payment_frame.locator(MoesE2ELocators.SAVE_BUTTON).click()

            self.page.wait_for_timeout(5000)  # Wait for payment processing
            self.page.click(MoesE2ELocators.PLACE_ORDER_BUTTON)
            time.sleep(10)

        except Exception as e:
            logger.exception(f"Order not placed: {str(e)}")
            raise