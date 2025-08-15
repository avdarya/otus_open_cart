import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_TITLE = By.CSS_SELECTOR, '#content h1'
    PRICE_NEW = By.CSS_SELECTOR, 'span.price-new'
    DESCRIPTION = By.CSS_SELECTOR, '#tab-description p.intro'
    ADD_BUTTON = By.CSS_SELECTOR, '#button-cart'
    REVIEW_STARS = By.CSS_SELECTOR, 'span.fa-stack'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Получить название продукта на странице Продукта')
    def get_product_title(self) -> str:
        self.logger.info('Get product title')
        return self.get_element(self.PRODUCT_TITLE).text

    @allure.step('Получить новую цену на странице Продукта')
    def get_price_new(self) -> str:
        self.logger.info('Get price new')
        return self.get_element(self.PRICE_NEW).text

    @allure.step('Получить описание на странице Продукта')
    def get_description(self) -> str:
        self.logger.info('Get description')
        description = self.get_element(self.DESCRIPTION).text
        return ' '.join(description.split())

    @allure.step('Проверить видимость кнопки Добавить на странице Продукта')
    def is_visible_add_button(self) -> bool:
        self.logger.info('Check visibility Add button')
        return self.get_element(self.ADD_BUTTON).is_displayed()

    @allure.step('Получить количество отображаемых звезд на странице Продукта')
    def get_stars_count(self) -> int:
        self.logger.info('Get stars count')
        stars = self.get_elements(self.REVIEW_STARS)
        self.logger.debug(f'Getting stars count: {len(stars)}')
        return len(stars)

