import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountPage(BasePage):
    HEADER_MY_ACCOUNT = By.XPATH, '//h2[normalize-space()="My Account"]'
    HEADER_MY_ORDERS = By.XPATH, '//h2[normalize-space()="My Orders"]'
    HEADER_AFFILIATE = By.XPATH, '//h2[normalize-space()="My Affiliate Account"]'
    HEADER_NEWSLETTER = By.XPATH, '//h2[normalize-space()="Newsletter"]'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Проверить видимость заголовка Мой аккаунт')
    def is_visible_header_my_account(self) -> bool:
        self.logger.info('Check visibility header My Account')
        return self.get_element(self.HEADER_MY_ACCOUNT).is_displayed()

    @allure.step('Проверить видимость заголовка Мои заказы')
    def is_visible_header_my_orders(self) -> bool:
        self.logger.info('Check visibility header My Orders')
        return self.get_element(self.HEADER_MY_ORDERS).is_displayed()

    @allure.step('Проверить видимость заголовка Мой аккаунт партнера')
    def is_visible_header_affiliate(self) -> bool:
        self.logger.info('Check visibility header My Affiliate')
        return self.get_element(self.HEADER_AFFILIATE).is_displayed()

    @allure.step('Проверить видимость заголовка Рассылка')
    def is_visible_header_newsletter(self) -> bool:
        self.logger.info('Check visibility header Newsletter')
        return self.get_element(self.HEADER_NEWSLETTER).is_displayed()