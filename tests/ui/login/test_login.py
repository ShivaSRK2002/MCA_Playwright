from page_objects.pages.login_pages.login_page import LoginPage
from page_objects.pages.e2e_pages.e2e_page import E2EPage
from utils.config_reader import read_json_config



def test_order_placement_logged(page):
    e2e_page = E2EPage(page)
    e2e_page.order_placement()

def test_order_placement_guest(page):
    e2e_page = E2EPage(page)
    e2e_page.order_placement_guest()