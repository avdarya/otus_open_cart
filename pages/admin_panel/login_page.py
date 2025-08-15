import allure
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

    @allure.step('Открыть страницу Авторизации')
    def open_login_page(self) -> 'LoginPage':
        self.logger.info('Open Login page')
        self.logger.debug(f'{self.url}')
        self.browser.get(self.url)
        return self

    @allure.step('Заполнить поле Логин "{username}"')
    def fill_username(self, username: str) -> 'LoginPage':
        self.logger.info(f'Fill username: {username}')
        self.input_value(self.USERNAME_FIELD, username)
        return self

    @allure.step('Заполнить поле Пароль "******"')
    def fill_password(self, password: str) -> 'LoginPage':
        self.logger.info('Fill password')
        self.input_value(self.PASSWORD_FIELD, password)
        return self

    @allure.step('Нажать на кнопку Подтвердить')
    def click_submit_button(self) -> None:
        self.logger.info('Click submit button')
        self.scroll_and_click(self.SUBMIT_BUTTON)

    @allure.step('Проверить видимость поля Логин')
    def is_visible_username_input(self) -> bool:
        self.logger.info('Check visibility username input')
        username_input = self.get_element(self.USERNAME_FIELD)
        return username_input.is_displayed()

    @allure.step('Проверить видимость иконки Пользователь')
    def is_visible_user_icon(self) -> bool:
        self.logger.info('Check visibility username_icon')
        icon = self.get_element(self.USER_ICON)
        return icon.is_displayed()

    @allure.step('Проверить видимость поля Пароль')
    def is_visible_password_input(self) -> bool:
        self.logger.info('Check visibility password_input')
        password_input = self.get_element(self.PASSWORD_FIELD)
        return password_input.is_displayed()

    @allure.step('Проверить видимость иконки Пароль')
    def is_visible_password_icon(self) -> bool:
        self.logger.info('Check visibility password_icon')
        icon = self.get_element(self.PASSWORD_ICON)
        return icon.is_displayed()

    @allure.step('Проверить видимость кнопки Подтвердить')
    def is_visible_submit_button(self) -> bool:
        self.logger.info('Check visibility submit_button')
        submit_button = self.get_element(self.SUBMIT_BUTTON)
        return submit_button.is_displayed()
