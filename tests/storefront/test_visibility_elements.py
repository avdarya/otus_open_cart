import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.storefront.desktops_page import DesktopsPage
from pages.admin_panel.login_page import LoginPage
from pages.storefront.main_page import MainPage
from pages.storefront.product_page import ProductPage
from pages.storefront.register_customer_page import RegisterCustomerPage

@allure.epic('Storefront')
@allure.feature('UI layout')
@allure.story('Elements visibility - Main page')
@allure.title('Verify Main page UI elements visibility')
@pytest.mark.parametrize('product, expected_desc, expected_price', [(
        'MacBook',
        'Intel Core 2 Duo processor Powered by an Intel Core 2 Duo processor at speeds up to 2.16GHz, t..',
        '$602.00'
)])
def test_main_page(
        browser: WebDriver,
        product: str,
        expected_desc: str,
        expected_price: str
):
    product_card = MainPage(browser).get_product_card(product)

    assert product_card is not None
    assert product_card.get_description() == expected_desc
    assert product_card.get_price_new() == expected_price
    assert product_card.is_visible_add_to_cart()

@allure.epic('Storefront')
@allure.feature('UI layout')
@allure.story('Elements visibility - Desktops page')
@allure.title('Verify Desktops page UI elements visibility')
def test_desktops_page(browser: WebDriver, base_url: str):
    desktop_page = DesktopsPage(browser, base_url).go_to_desktops_page()
    product_cards = desktop_page.get_product_cards()

    assert desktop_page.get_catalog_title() =='Desktops'
    assert desktop_page.is_visible_compare_button()
    assert desktop_page.is_visible_sort_input()
    assert desktop_page.is_visible_count_input()
    assert len(product_cards) == 10

@allure.epic('Storefront')
@allure.feature('UI layout')
@allure.story('Elements visibility - Product page')
@allure.title('Verify Product page UI elements visibility')
@pytest.mark.parametrize('product, expected_desc, expected_price_new,  expected_stars_count',
    [(
        'iPhone',
        'iPhone is a revolutionary new mobile phone that allows you to make a call by simply tapping a name or number in your address book, a favorites list, or a call log. It also automatically syncs all your contacts from a PC, Mac, or Internet service. And it lets you select and listen to voicemail messages in whatever order you want just like email.',
        '$123.20',
        5
    )]
)
def test_product_page(
        browser: WebDriver,
        product: str,
        expected_desc: str,
        expected_price_new: str,
        expected_stars_count: int
):
    MainPage(browser) \
        .get_product_card(product) \
        .click_product_title()
    page = ProductPage(browser)

    assert page.get_product_title() == product
    assert page.get_price_new() == expected_price_new
    assert page.get_description() == expected_desc
    assert page.is_visible_add_button()
    assert page.get_stars_count() == expected_stars_count

@allure.epic('Storefront')
@allure.feature('UI layout')
@allure.story('Elements visibility - Login page')
@allure.title('Verify Desktops page UI elements visibility')
def test_login_page(browser: WebDriver, base_url: str):
    page = LoginPage(browser, base_url).open_login_page()

    assert page.is_visible_username_input()
    assert page.is_visible_user_icon()
    assert page.is_visible_password_input()
    assert page.is_visible_password_icon()
    assert page.is_visible_submit_button()

@allure.epic('Storefront')
@allure.feature('UI layout')
@allure.story('Elements visibility - Register customer page')
@allure.title('Verify Register customer page UI elements visibility')
def test_register_customer_page(browser: WebDriver, base_url: str):
    page = RegisterCustomerPage(browser, base_url).go_to_register_customer_page()

    assert page.is_visible_first_name_input()
    assert page.is_visible_last_name_input()
    assert page.is_visible_email_input()
    assert page.is_visible_password_input()
    assert page.is_visible_continue_button()

