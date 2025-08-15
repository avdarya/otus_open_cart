import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.allert_success import AlertSuccess
from pages.admin_panel.products.product_form_page import ProductFormPage
from pages.admin_panel.products.product_list_page import ProductListPage
from pages.admin_panel.dashboard_page import DashboardPage
from tests.conftest import ProductData


@allure.epic('Admin panel')
@allure.feature('Product management')
@allure.story('Success add product')
@allure.title('Add new product')
def test_add_product(admin_browser: WebDriver, generate_product_data: ProductData):
    DashboardPage(admin_browser) \
        .get_navigation_menu() \
        .click_catalog() \
        .click_products()
    ProductListPage(admin_browser).click_add_new()
    product_form_page = ProductFormPage(admin_browser)
    product_form_page \
        .fill_product_name(generate_product_data.name) \
        .fill_description(generate_product_data.description) \
        .fill_meta_tag_title(generate_product_data.meta_tag) \
        .click_tab_data() \
        .fill_model(generate_product_data.model) \
        .fill_price(generate_product_data.price) \
        .fill_quantity(generate_product_data.quantity) \
        .click_tab_seo() \
        .fill_keyword(generate_product_data.keyword) \
        .click_save()
    alert_text = AlertSuccess(admin_browser, product_form_page.logger).get_alert_text()

    assert alert_text == 'Success: You have modified products!'

    product_form_page.click_back()

    assert ProductListPage(admin_browser).is_product_in_list(
        generate_product_data.name,
        generate_product_data.model,
        generate_product_data.price,
        generate_product_data.quantity
    )