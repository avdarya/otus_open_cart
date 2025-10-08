import logging

import allure
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pages.components.base_component import BaseComponent


class HeaderCart(BaseComponent):
    CART = By.CSS_SELECTOR, '#header-cart button'
    VIEW_CART = By.CSS_SELECTOR, 'div.dropdown a[href*=cart]'

    def __init__(self, browser: WebDriver, root: WebElement, logger: logging.Logger | None = None):
        super().__init__(browser, root, logger)

    @allure.step('Получить счетчик и стоимость корзины')
    def get_counter_cost(self) -> tuple[int, float]:
        self.logger.info('Get counter cost')
        self.refresh_root(self.CART)
        cart_text = self.root.text.strip()
        self.logger.debug(f'Cart text raw: "{cart_text}"')
        counter = int(cart_text.split()[0])
        cost = float(cart_text.split('$')[1])
        self.logger.debug(f'Counter={counter}, cost={cost}')
        return counter, cost

    @allure.step('Ожидать обновления счётчика корзины')
    def wait_for_cart_update(self, previous_counter: int, timeout: int = 5) -> None:
        WebDriverWait(self.browser, timeout).until(
            lambda d: int(d.find_element(*self.CART).text.split()[0]) != previous_counter
        )

    @allure.step('Нажать на кнопку Корзина в Header')
    def click_cart_btn(self) -> 'HeaderCart':
        self.logger.info('Click Cart button')
        self.scroll_and_click(self.CART)
        return self

