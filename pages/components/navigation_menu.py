import logging

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class NavigationMenu(BaseComponent):
    CATALOG = By.CSS_SELECTOR, '#menu-catalog > a'
    PRODUCTS = By.LINK_TEXT, 'Products'

    def __init__(self, browser: WebDriver, root: WebElement, logger: logging.Logger | None = None):
        super().__init__(browser, root, logger)

    @allure.step('Нажать на Каталог')
    def click_catalog(self) -> 'NavigationMenu':
        self.logger.info('Click Catalog tab')
        self.scroll_and_click(self.CATALOG)
        return self


    @allure.step('Нажать на Продукты')
    def click_products(self) -> 'NavigationMenu':
        self.logger.info('Click Products tab')
        self.scroll_and_click(self.PRODUCTS)
        return self