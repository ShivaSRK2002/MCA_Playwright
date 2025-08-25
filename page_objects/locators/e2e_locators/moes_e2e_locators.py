class MoesE2ELocators:
    # Navigation and Account
    MENU_NAV_LINK = '#Menu_Menu'
    SIGN_IN_BUTTON = '[data-testid="signin-button"]'
    CREATE_ACCOUNT_BTN = '[data-testid="btn_create_account"]'
    CONTINUE_AS_GUEST_BUTTON = '[data-testid="txt_guest_account"]'
    ACCEPT_ALL_COOKIES_BTN = "//button[@id='acceptAllCookieButton']"

    
    SIGN_IN_BUTTON_USER = '#sign-in-button'


    # Signup / Login Fields
    EMAIL_INPUT = '[data-testid="email"]'
    CONTINUE_BTN = '[data-testid="continue-button"]'
    FIRST_NAME_INPUT = '[data-testid="firstname"]'
    LAST_NAME_INPUT = '[data-testid="lastname"]'
    PHONE_NUMBER_INPUT = '[data-testid="phone"]'
    PASSWORD_INPUT = '[data-testid="password"]'
    CONFIRM_PASSWORD_INPUT = '[data-testid="confirmpassword"]'
    BIRTH_MONTH_DROPDOWN = '[data-testid="sign_up_birth_month"]'
    BIRTH_DAY_DROPDOWN = '[data-testid="sign_up_birth_day"]'
    COMPLETE_SIGN_UP_BTN = '[data-testid="btn_complete_sign_up"]'
    CONFIRM_BIRTHDAY_BTN = '[data-testid="conformSubmitPopup"]'
    SKIP_BTN = '[data-testid="skip-button"]'
    FINAL_CONTINUE_BTN = '#continuebutton'

    January_DROPDOWN = 'li[role="option"][aria-label="January"]'
    Date_DROPDOWN = 'li[role="option"][aria-label="1"]'

    # Ordering
    START_ORDER = '#btn_startorder'
    SEARCH_TEXT = '[data-testid="input_store_search_input"]'
    SELECT_ADDRESS_BTN = 'button[data-testid="btn_placeId"] >> text=Guam'
    ORDER_NOW_BUTTON = '[data-testid="zipcode_95635"] >> [data-testid="btn_order_now"]'
    # Locator for the "Select Location" button inside the store card with ID 95635
   

    LOCATION_TEXT = '[data-testid="btn_restaurant_name"]'
    SELECT_LOCATION = "div.storeCardContainer[id='id_95635'] button[data-testid='btn_select location']"

    BEVERAGES_CATEGORY = '[data-testid="menu_category_id_cat-004"]'
    BOTTLED_20OZ_TILE = '[data-testid="img_pro-032"]'
    REGULAR_FOUNTAIN_DRINK_TILE = "#drinks-id [alt='Regular Fountain Drink']"
    BOTTLED_WATER_TILE = "[data-testid='img_pro-031']"

    ADD_CART = '[data-testid="btn_add_to_cart"]'
    CART_ICON = '#link_cart'
    CHECKOUT_BUTTON = '#cart_checkout_button'

    # Payment
    CREDIT_CARD_RADIO = '[data-testid="btn_creditcard"]'
    CARD_NUMBER_INPUT = '#CardNumber'
    EXPIRATION_DATE_INPUT = '#ExpirationDate'
    CVV_INPUT = '#SecurityCode'
    POSTAL_CODE_INPUT = '#PostalCode'
    SAVE_BUTTON = 'button.fp-hpc-pay-button'
    PLACE_ORDER_BUTTON = '[data-testid="btn_place_order"]'

    # Survey Close
    SURVEY_CLOSE_BUTTON = '[data-aut="button-close"]'

    CHECKOUT_FIRSTNAME_INPUT = '[data-testid="txt_checkout_firstname"]'
    CHECKOUT_LASTNAME_INPUT = '[data-testid="txt_checkout_lastname"]'
    CHECKOUT_EMAIL_INPUT = '[data-testid="txt_checkout_email"]'
    CHECKOUT_PHONE_INPUT = '[data-testid="txt_checkout_phonenumber"]'
    ACCEPT_BTN = "#acceptAllCookieButton"

    ORDER_DETAIL_SECTION = '[data-testid="orderDetail"]'
    ORDER_ID_TEXT = '[data-testid="orderID"]'
    ORDER_TIME_TEXT = '.orderDetailTime'
    See_menu_button = "//a[@href='https://www.moes.com/menu']"

