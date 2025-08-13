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

    def is_visible_header_my_account(self) -> bool:
        return self.get_element(self.HEADER_MY_ACCOUNT).is_displayed()

    def is_visible_header_my_orders(self) -> bool:
        return self.get_element(self.HEADER_MY_ORDERS).is_displayed()

    def is_visible_header_affiliate(self) -> bool:
        return self.get_element(self.HEADER_AFFILIATE).is_displayed()

    def is_visible_header_newsletter(self) -> bool:
        return self.get_element(self.HEADER_NEWSLETTER).is_displayed()