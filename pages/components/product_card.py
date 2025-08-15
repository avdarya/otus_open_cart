import logging

import allure
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

    def __init__(self, browser: WebDriver, root: WebElement, logger: logging.Logger | None = None):
        super().__init__(browser, root, logger)

    @allure.step('Нажать на кнопку Добавить в корзину в карточке товара')
    def add_to_cart(self) -> 'ProductCard':
        self.logger.info('Add product to cart')
        self.scroll_and_click(self.ADD_TO_CART)
        return self

    @allure.step('Получить описание в карточке товара')
    def get_description(self) -> str:
        self.logger.info('Get product description')
        desc = self.get_element(self.DESCRIPTION).text
        self.logger.debug(f'Getting product description: {desc}')
        return ' '.join(desc.split())

    @allure.step('Получить новую цену в карточке товара')
    def get_price_new(self) -> str:
        self.logger.info('Get product price new')
        price =self.get_element(self.PRICE_NEW).text.strip()
        self.logger.debug(f'Getting price new: {price}')
        return price

    @allure.step('Получить старую цену в карточке товара')
    def get_price_old(self) -> str | None:
        self.logger.info('Get product price old')
        elements = self.get_elements(
            self.PRICE_OLD,
            root=self.root,
            allow_empty=True
        )
        price = elements[0].text.strip() if elements else None
        self.logger.debug(f'Getting price old: {price}')
        return price

    @allure.step('Получить цену без налога в карточке товара')
    def get_price_tax(self) -> str:
        self.logger.info('Get product price tax')
        tax = self.get_element(self.PRICE_TAX).text.strip().split('Ex Tax: ')[1]
        self.logger.debug(f'Getting price tax: {tax}')
        return tax

    @allure.step('Проверить видимость кнопки Добавить в корзину в карточке товара')
    def is_visible_add_to_cart(self) -> bool:
        self.logger.info('Check visibility add to cart button')
        return self.get_element(self.ADD_TO_CART).is_displayed()

    @allure.step('Нажать на заголовок в карточке товара')
    def click_product_title(self) -> None:
        self.logger.info('Click product title')
        self.scroll_and_click(self.TITLE)


