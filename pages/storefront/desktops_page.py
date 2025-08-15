import allure
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

    @allure.step('Открыть страницу Desktops')
    def go_to_desktops_page(self) -> 'DesktopsPage':
        self.logger.info('Open Desktops page')
        self.logger.debug(f'url: {self.url}')
        self.browser.get(self.url)
        return self

    @allure.step('Получить заголовок каталога')
    def get_catalog_title(self) -> str:
        self.logger.info('Get catalog title')
        return self.get_element(self.CATALOG_TITLE).text

    @allure.step('Проверить видимость кнопки Сравнить')
    def is_visible_compare_button(self) -> bool:
        self.logger.info('Check visibility Compare button')
        return self.get_element(self.COMPARE_BUTTON).is_displayed()

    @allure.step('Проверить видимость поля Сортировка')
    def is_visible_sort_input(self) -> bool:
        self.logger.info('Check visibility Sort input')
        return self.get_element(self.SORT_INPUT).is_displayed()

    @allure.step('Проверить видимость поля Количество отображаемых продуктов')
    def is_visible_count_input(self) -> bool:
        self.logger.info('Check visibility Count input')
        return self.get_element(self.COUNT_INPUT).is_displayed()

