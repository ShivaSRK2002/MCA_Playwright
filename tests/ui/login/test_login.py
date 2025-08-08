from page_objects.pages.e2e_pages.moes_e2e_page import MoesE2EPage
from utils.config_reader import read_json_config


def test_order_placement_logged(page):
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement()


def test_order_placement_guest(page):
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement_guest()
