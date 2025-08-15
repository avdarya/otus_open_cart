import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class CartPage(BasePage):
    PRODUCT_ROW = By.XPATH, '//tr[.//td[@class="text-start text-wrap"]/a[normalize-space()="{}"]]'
    PRODUCT_COUNT = By.CSS_SELECTOR, 'input[name="quantity"]'
    PRODUCT_PRICE = By.XPATH, './td[@class="text-end"][1]'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Получить строку продукта "{product_name}"')
    def get_product_row(self, product_name: str) -> WebElement:
        self.logger.info(f'Get product row "{product_name}"')
        product_row = self.get_element((
            self.PRODUCT_ROW[0],
            self.PRODUCT_ROW[1].format(product_name
        )))
        return product_row

    @allure.step('Получить количество в строке продукта')
    def get_product_count(self, product_row: WebElement) -> int:
        self.logger.info('Get product count')
        count_input = self.get_element(self.PRODUCT_COUNT, product_row)
        count = int(count_input.get_attribute('value'))
        self.logger.debug(f'Getting product count: {count}')
        return count

    @allure.step('Получить стоимость за одну единицу в строке продукта')
    def get_unit_product_price(self, product_row: WebElement) -> str:
        self.logger.info('Get unit product price')
        unit_price = self.get_element(self.PRODUCT_PRICE, product_row).text
        self.logger.debug(f'Getting unit product price: {unit_price}')
        return unit_price
