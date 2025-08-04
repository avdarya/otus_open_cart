from selenium.webdriver.remote.webdriver import WebDriver
from pages.components.allert_success import AlertSuccess
from pages.admin_panel.products.product_list_page import ProductListPage
from pages.admin_panel.dashboard_page import DashboardPage
from tests.conftest import ProductData


def test_delete_product(admin_browser: WebDriver, added_product: ProductData):
    DashboardPage(admin_browser) \
        .get_navigation_menu() \
        .click_catalog() \
        .click_products()
    product_page = ProductListPage(admin_browser)
    product_page \
        .select_product(added_product.name) \
        .click_delete() \
        .confirm_delete()

    alert_text = AlertSuccess(admin_browser).get_alert_text()

    assert alert_text == 'Success: You have modified products!'

    product_page.refresh_page()

    assert ProductListPage(admin_browser).is_product_in_list(
        added_product.name,
        added_product.model,
        added_product.price,
        added_product.quantity
    ) is False

