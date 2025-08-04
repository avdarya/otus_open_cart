from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class RegisterCustomerPage(BasePage):
    FIRST_NAME_INPUT = By.CSS_SELECTOR, '#input-firstname'
    LAST_NAME_INPUT = By.CSS_SELECTOR, '#input-lastname'
    EMAIL_INPUT = By.CSS_SELECTOR, '#input-email'
    PASSWORD_INPUT = By.CSS_SELECTOR, '#input-password'
    CONTINUE_BUTTON = By.CSS_SELECTOR, 'button[type="submit"]'
    CHECKBOX_AGREE = By.CSS_SELECTOR, 'input[name="agree"]'

    def __init__(self, browser: WebDriver, base_url: str):
        super().__init__(browser)
        self.url = f'{base_url}/en-gb?route=account/register'

    def go_to_register_customer_page(self) -> 'RegisterCustomerPage':
        self.browser.get(self.url)
        return self

    def fill_first_name(self, first_name: str) -> 'RegisterCustomerPage':
        self.input_value(self.FIRST_NAME_INPUT, first_name)
        return self

    def fill_last_name(self, last_name: str) -> 'RegisterCustomerPage':
        self.input_value(self.LAST_NAME_INPUT, last_name)
        return self

    def fill_email(self, email: str) -> 'RegisterCustomerPage':
        self.input_value(self.EMAIL_INPUT, email)
        return self

    def fill_password(self, password: str) -> 'RegisterCustomerPage':
        self.input_value(self.PASSWORD_INPUT, password)
        return self

    def toggle_agree(self) -> 'RegisterCustomerPage':
        self.scroll_and_click(self.CHECKBOX_AGREE)
        return self

    def click_continue_button(self) -> None:
        self.scroll_and_click(self.CONTINUE_BUTTON)

    def is_visible_first_name_input(self) -> bool:
        return self.get_element(self.FIRST_NAME_INPUT).is_displayed()

    def is_visible_last_name_input(self) -> bool:
        return self.get_element(self.LAST_NAME_INPUT).is_displayed()

    def is_visible_email_input(self) -> bool:
        return self.get_element(self.EMAIL_INPUT).is_displayed()

    def is_visible_password_input(self) -> bool:
        return self.get_element(self.PASSWORD_INPUT).is_displayed()

    def is_visible_continue_button(self) -> bool:
        return self.get_element(self.CONTINUE_BUTTON).is_displayed()

