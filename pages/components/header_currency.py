from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class HeaderCurrency(BaseComponent):
    CURRENCY_VALUE = By.XPATH, '//a[contains(text(), "{}")]'
    CURRENCY_FORM = By.CSS_SELECTOR, '#form-currency'
    SELECTED_CURRENCY = By.CSS_SELECTOR, '#form-currency strong'

    def __init__(self, browser: WebDriver, root: WebElement):
        super().__init__(browser, root)

    def click_currency_form(self) -> 'HeaderCurrency':
        self.refresh_root(self.CURRENCY_FORM)
        self.root.click()
        return self

    def select_currency(self, currency: str) -> 'HeaderCurrency':
        currency_el = self.get_element((
            self.CURRENCY_VALUE[0],
            self.CURRENCY_VALUE[1].format(currency),
        ))
        currency_el.click()
        return self

    def get_selected_currency(self) -> str:
        self.refresh_root(self.CURRENCY_FORM)
        return self.get_element(self.SELECTED_CURRENCY).text.strip()
