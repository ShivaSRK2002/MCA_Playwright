import pytest
from page_objects.pages.e2e_pages.moes_e2e_page import MoesE2EPage


def test_order_placement_logged(page, browser_name):
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement()

def test_order_placement_guest(page, browser_name):
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement_guest()

def test_order_placement_signed_in(page, browser_name):
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement_signed_in()