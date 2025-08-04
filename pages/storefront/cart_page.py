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

    def get_product_row(self, product_name: str) -> WebElement:
        product_row = self.get_element((
            self.PRODUCT_ROW[0],
            self.PRODUCT_ROW[1].format(product_name
        )))
        return product_row

    def get_product_count(self, product_row: WebElement) -> int:
        count_input = product_row.find_element(*self.PRODUCT_COUNT)
        return int(count_input.get_attribute('value'))

    def get_unit_product_price(self, product_row: WebElement) -> str:
        return product_row.find_element(*self.PRODUCT_PRICE).text
