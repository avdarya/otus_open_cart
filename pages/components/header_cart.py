import logging

import allure
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.components.base_component import BaseComponent
from utils.helpers import describe_logged_target


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

    @allure.step('Нажать на кнопку Корзина в Header')
    def click_cart_btn(self) -> 'HeaderCart':
        self.logger.info('Click Cart button')
        self.scroll_and_click(self.CART)
        return self

    @allure.step('Нажать на кнопку Посмотреть корзину')
    def go_to_cart_page(self) -> None:
        self.logger.info("Go to cart page from header cart's link")
        self.refresh_root(self.CART)
        self.scroll_and_click(self.root)
        self.logger.debug(f'Waiting for view cart link: {describe_logged_target(self.VIEW_CART)}')
        view_cart = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable(self.VIEW_CART)
        )
        view_cart.click()

