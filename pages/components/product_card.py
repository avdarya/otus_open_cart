from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pages.components.base_component import BaseComponent


class ProductCard(BaseComponent):
    ADD_TO_CART = By.XPATH, './/button[contains(@formaction, "/cart.add")]'
    TITLE = By.CSS_SELECTOR, 'h4 a'
    DESCRIPTION = By.CSS_SELECTOR, 'div.description p'
    PRICE_NEW = By.CSS_SELECTOR, 'span.price-new'
    PRICE_OLD = By.CSS_SELECTOR, 'span.price-old'
    PRICE_TAX = By.CSS_SELECTOR, 'span.price-tax'

    def __init__(self, browser: WebDriver, root: WebElement):
        super().__init__(browser, root)

    def add_to_cart(self) -> 'ProductCard':
        self.scroll_and_click(self.ADD_TO_CART)
        return self

    def get_description(self) -> str:
        desc = self.get_element(self.DESCRIPTION).text
        return ' '.join(desc.split())

    def get_price_new(self) -> str:
        return self.get_element(self.PRICE_NEW).text.strip()

    def get_price_old(self) -> str | None:
        elements = self.root.find_elements(*self.PRICE_OLD)
        return elements[0].text.strip() if elements else None

    def get_price_tax(self) -> str:
        return self.get_element(self.PRICE_TAX).text.strip().split('Ex Tax: ')[1]

    def is_visible_add_to_cart(self) -> bool:
        return self.get_element(self.ADD_TO_CART).is_displayed()

    def click_product_title(self) -> None:
        self.scroll_and_click(self.TITLE)


