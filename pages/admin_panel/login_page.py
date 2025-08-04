from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_FIELD = By.CSS_SELECTOR, '#input-username'
    USER_ICON = By.CSS_SELECTOR, 'i.fa-user'
    PASSWORD_FIELD = By.CSS_SELECTOR, '#input-password'
    PASSWORD_ICON = By.CSS_SELECTOR, 'form[id="form-login"] i.fa-lock'
    SUBMIT_BUTTON = By.CSS_SELECTOR, 'button[type="submit"]'

    def __init__(self, browser: WebDriver, base_url: str):
        super().__init__(browser)
        self.url = f'{base_url}/administration'

    def open_login_page(self) -> 'LoginPage':
        self.browser.get(self.url)
        return self

    def fill_username(self, username: str) -> 'LoginPage':
        self.input_value(self.USERNAME_FIELD, username)
        return self

    def fill_password(self, password: str) -> 'LoginPage':
        self.input_value(self.PASSWORD_FIELD, password)
        return self

    def click_submit_button(self) -> None:
        self.scroll_and_click(self.SUBMIT_BUTTON)

    def is_visible_username_input(self) -> bool:
        username_input = self.get_element(self.USERNAME_FIELD)
        return username_input.is_displayed()

    def is_visible_user_icon(self) -> bool:
        icon = self.get_element(self.USER_ICON)
        return icon.is_displayed()

    def is_visible_password_input(self) -> bool:
        password_input = self.get_element(self.PASSWORD_FIELD)
        return password_input.is_displayed()

    def is_visible_password_icon(self) -> bool:
        icon = self.get_element(self.PASSWORD_ICON)
        return icon.is_displayed()

    def is_visible_submit_button(self) -> bool:
        submit_button = self.get_element(self.SUBMIT_BUTTON)
        return submit_button.is_displayed()
