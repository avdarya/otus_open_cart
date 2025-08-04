from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class NavigationMenu(BaseComponent):
    CATALOG = By.CSS_SELECTOR, '#menu-catalog > a'
    PRODUCTS = By.LINK_TEXT, 'Products'

    def __init__(self, browser: WebDriver, root: WebElement):
        super().__init__(browser, root)

    def click_catalog(self) -> 'NavigationMenu':
        self.scroll_and_click(self.CATALOG)
        return self

    def click_products(self) -> 'NavigationMenu':
        self.scroll_and_click(self.PRODUCTS)
        return self