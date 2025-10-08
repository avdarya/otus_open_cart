import logging

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AlertSuccess:
    SUCCESS_ALERT = By.CSS_SELECTOR, '.alert-success'
    CLOSE_BUTTON = By.CSS_SELECTOR, '.btn-close'
    SHOPPING_CART_LINK = By.CSS_SELECTOR, '.alert-success a[href*="checkout/cart"]'

    def __init__(self, browser: WebDriver, logger: logging.Logger | None = None):
        self.browser = browser
        self.alert = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located(self.SUCCESS_ALERT))
        self.logger = logger or logging.getLogger(type(self).__name__)

    @allure.step('Закрыть уведомление')
    def close_alert(self) -> None:
        self.logger.info('Close alert')
        self.alert.find_element(*self.CLOSE_BUTTON).click()

    @allure.step('Получить текст уведомления')
    def get_alert_text(self) -> str:
        self.logger.info('Get alert text')
        text = self.alert.text
        self.logger.debug(f'Getting alert text: {text}')
        return text

    @allure.step('Перейти в корзину из уведомления')
    def click_shopping_cart(self) -> None:
        self.logger.info('Click "shopping cart" link in success alert')
        self.alert.find_element(*self.SHOPPING_CART_LINK).click()