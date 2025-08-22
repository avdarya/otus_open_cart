import allure
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.components.allert_success import AlertSuccess
from pages.storefront.cart_page import CartPage
from pages.storefront.main_page import MainPage


@allure.epic('Storefront')
@allure.feature('Cart management')
@allure.story('Add product to cart')
@allure.title('Add product to cart from Main page')
@pytest.mark.parametrize('product, price', [('MacBook', '602.00')])
def test_add_to_cart_from_main(browser: WebDriver, product: str, price: str, logger):
    main_page = MainPage(browser)
    header_cart = main_page.get_header_cart()

    counter_before, cost_before = header_cart.get_counter_cost()

    main_page.add_product_to_cart(product)

    AlertSuccess(browser, main_page.logger).close_alert()

    counter_after, cost_after = header_cart.get_counter_cost()
    assert counter_before + 1 == counter_after
    assert cost_before + float(price) == cost_after

    header_cart.go_to_cart_page()
    cart_page = CartPage(browser)
    product_row = cart_page.get_product_row(product)

    assert product_row is not None
    assert cart_page.get_product_count(product_row) == 1
    assert str(price) in cart_page.get_unit_product_price(product_row)
