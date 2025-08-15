import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.admin_panel.base_admin_page import BaseAdminPage


class DashboardPage(BaseAdminPage):
    PROFILE_NAME = By.CSS_SELECTOR, '#nav-profile'
    LOGOUT_BUTTON = By.CSS_SELECTOR, '#nav-logout'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Получить имя текущего пользователя')
    def get_profile_name(self) -> str:
        self.logger.info('Get profile name')
        profile_name = self.get_element(self.PROFILE_NAME)
        return profile_name.text

    @allure.step('Нажать на кнопку Выйти')
    def click_logout_button(self) -> None:
        self.logger.info('Click Logout button')
        self.scroll_and_click(self.LOGOUT_BUTTON)
