import logging

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class HeaderCurrency(BaseComponent):
    CURRENCY_VALUE = By.XPATH, '//a[contains(text(), "{}")]'
    CURRENCY_FORM = By.CSS_SELECTOR, '#form-currency'
    SELECTED_CURRENCY = By.CSS_SELECTOR, '#form-currency strong'

    def __init__(self, browser: WebDriver, root: WebElement, logger: logging.Logger | None = None):
        super().__init__(browser, root, logger)

    @allure.step('Нажать на поле Валюта в Header')
    def click_currency_form(self) -> 'HeaderCurrency':
        self.logger.info('Click currency form')
        self.refresh_root(self.CURRENCY_FORM)
        self.scroll_and_click(self.root)
        return self

    @allure.step('Выбрать валюту "{currency}"')
    def select_currency(self, currency: str) -> 'HeaderCurrency':
        self.logger.info(f'Select currency "{currency}"')
        currency_el = self.get_element((
            self.CURRENCY_VALUE[0],
            self.CURRENCY_VALUE[1].format(currency),
        ))
        self.scroll_and_click(currency_el)
        return self

    @allure.step('Получить символ выбранной валюты')
    def get_selected_currency(self) -> str:
        self.logger.info('Get selected currency')
        self.refresh_root(self.CURRENCY_FORM)
        sel_currency = self.get_element(self.SELECTED_CURRENCY).text.strip()
        self.logger.debug(f'Selected currency is "{sel_currency}"')
        return sel_currency
