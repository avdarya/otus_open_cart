import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.storefront.base_product_page import BaseProductPage


class MainPage(BaseProductPage):

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Добавить продукт "{product}" в корзину')
    def add_product_to_cart(self, product: str) -> 'MainPage':
        self.logger.info(f'Add product "{product}" to cart')
        self.get_product_card(product).add_to_cart()
        return self

