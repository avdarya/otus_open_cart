import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.storefront.account_page import AccountPage
from pages.storefront.register_customer_page import RegisterCustomerPage
from pages.storefront.success_page import SuccessPage
from tests.conftest import CustomerData


@pytest.mark.parametrize('expected_success_header', ['Your Account Has Been Created!'])
def test_register_new_customer(
        browser: WebDriver,
        base_url: str,
        generate_customer_data: CustomerData,
        expected_success_header: str
):
    RegisterCustomerPage(browser, base_url) \
        .go_to_register_customer_page() \
        .fill_first_name(generate_customer_data.first_name) \
        .fill_last_name(generate_customer_data.last_name) \
        .fill_email(generate_customer_data.email) \
        .fill_password(generate_customer_data.password) \
        .toggle_agree() \
        .click_continue_button()

    success_page = SuccessPage(browser)

    assert success_page.get_success_header() == expected_success_header

    success_page.click_continue_button()

    account_page = AccountPage(browser)

    assert account_page.is_visible_header_my_account()
    assert account_page.is_visible_header_my_orders()
    assert account_page.is_visible_header_affiliate()
    assert account_page.is_visible_header_newsletter()

