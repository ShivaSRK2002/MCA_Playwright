import pytest
from page_objects.pages.e2e_pages.moes_e2e_page import MoesE2EPage

@pytest.mark.parametrize("browser", ["chromium"])  # parametrize browser
def test_order_placement_logged(page, browser):  # <-- accept browser parameter
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement()
    # Add assertions here based on expected behavior

@pytest.mark.parametrize("browser", ["chromium"])
def test_order_placement_guest(page, browser):
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement_guest()
    # Add assertions here
@pytest.mark.parametrize("browser", ["chromium,"])  # parametrize browser
def test_order_placement_logged_1(page, browser):  # <-- accept browser parameter
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement()
    # Add assertions here based on expected behavior

@pytest.mark.parametrize("browser", ["chromium"])
def test_order_placement_guest_2(page, browser):
    e2e_page = MoesE2EPage(page)
    e2e_page.order_placement_guest()
    # Add assertions here
