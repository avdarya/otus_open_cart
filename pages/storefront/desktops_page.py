from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.storefront.base_product_page import BaseProductPage


class DesktopsPage(BaseProductPage):
    CATALOG_TITLE = By.CSS_SELECTOR, '#content h2'
    COMPARE_BUTTON = By.CSS_SELECTOR, '#compare-total'
    SORT_INPUT = By.CSS_SELECTOR, '#input-sort'
    COUNT_INPUT = By.CSS_SELECTOR, '#input-limit'

    def __init__(self, browser: WebDriver, base_url: str):
        super().__init__(browser)
        self.url = f'{base_url}/en-gb/catalog/desktops'

    def go_to_desktops_page(self) -> 'DesktopsPage':
        self.browser.get(self.url)
        return self

    def get_catalog_title(self) -> str:
        return self.get_element(self.CATALOG_TITLE).text

    def is_visible_compare_button(self) -> bool:
        return self.get_element(self.COMPARE_BUTTON).is_displayed()

    def is_visible_sort_input(self) -> bool:
        return self.get_element(self.SORT_INPUT).is_displayed()

    def is_visible_count_input(self) -> bool:
        return self.get_element(self.COUNT_INPUT).is_displayed()

