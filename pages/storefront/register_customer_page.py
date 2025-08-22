import allure
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

    @allure.step('Открыть страницу Регистрация клиента')
    def go_to_register_customer_page(self) -> 'RegisterCustomerPage':
        self.logger.info('Open Register Customer Page')
        self.logger.debug(f'url: {self.url}')
        self.browser.get(self.url)
        return self

    @allure.step('Заполнить поле Имя {first_name}')
    def fill_first_name(self, first_name: str) -> 'RegisterCustomerPage':
        self.logger.info(f'Fill first name: {first_name}')
        self.input_value(self.FIRST_NAME_INPUT, first_name)
        return self

    @allure.step('Заполнить поле Фамилия {last_name}')
    def fill_last_name(self, last_name: str) -> 'RegisterCustomerPage':
        self.logger.info(f'Fill last name: {last_name}')
        self.input_value(self.LAST_NAME_INPUT, last_name)
        return self

    @allure.step('Заполнить поле Email {email}')
    def fill_email(self, email: str) -> 'RegisterCustomerPage':
        self.logger.info(f'Fill email: {email}')
        self.input_value(self.EMAIL_INPUT, email)
        return self

    @allure.step('Заполнить поле Пароль ******')
    def fill_password(self, password: str) -> 'RegisterCustomerPage':
        self.logger.info(f'Fill password: {password}')
        self.input_value(self.PASSWORD_INPUT, password)
        return self

    @allure.step('Переключить чекбокс согласия с политикой конфиденциальности')
    def toggle_agree(self) -> 'RegisterCustomerPage':
        self.logger.info('Toggle Agree button')
        self.scroll_and_click(self.CHECKBOX_AGREE)
        return self

    @allure.step('Нажать на кнопку Продолжить')
    def click_continue_button(self) -> None:
        self.logger.info('Click Continue button')
        self.scroll_and_click(self.CONTINUE_BUTTON)

    @allure.step('Проверить видимость поля Имя')
    def is_visible_first_name_input(self) -> bool:
        self.logger.info('Check visibility First Name input')
        return self.get_element(self.FIRST_NAME_INPUT).is_displayed()

    @allure.step('Проверить видимость поля Фамилия')
    def is_visible_last_name_input(self) -> bool:
        self.logger.info('Check visibility Last Name input')
        return self.get_element(self.LAST_NAME_INPUT).is_displayed()

    @allure.step('Проверить видимость поля Email')
    def is_visible_email_input(self) -> bool:
        self.logger.info('Check visibility Email input')
        return self.get_element(self.EMAIL_INPUT).is_displayed()

    @allure.step('Проверить видимость поля Пароль')
    def is_visible_password_input(self) -> bool:
        self.logger.info('Check visibility Password input')
        return self.get_element(self.PASSWORD_INPUT).is_displayed()

    @allure.step('Проверить видимость кнопки Продолжить')
    def is_visible_continue_button(self) -> bool:
        self.logger.info('Check visibility Continue button')
        return self.get_element(self.CONTINUE_BUTTON).is_displayed()

