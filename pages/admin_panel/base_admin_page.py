import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.components.navigation_menu import NavigationMenu
from pages.base_page import BasePage


class BaseAdminPage(BasePage):
    NAVIGATION_MENU = By.CSS_SELECTOR, '#menu'
    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Получить навигационное меню')
    def get_navigation_menu(self) -> NavigationMenu:
        self.logger.debug('Get navigation menu')
        menu = self.get_element(self.NAVIGATION_MENU)
        return NavigationMenu(self.browser, menu, self.logger)