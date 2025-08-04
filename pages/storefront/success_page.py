from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SuccessPage(BasePage):
    SUCCESS_HEADER = By.CSS_SELECTOR, '#common-success h1'
    CONTINUE_BUTTON = By.CSS_SELECTOR, 'div.text-end a.btn.btn-primary'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def get_success_header(self) -> str:
        return self.get_element(self.SUCCESS_HEADER).text

    def click_continue_button(self) -> None:
        self.get_element(self.CONTINUE_BUTTON).click()