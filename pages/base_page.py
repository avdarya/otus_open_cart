import logging
import hashlib
import os

from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.components.header_cart import HeaderCart
from pages.components.header_currency import HeaderCurrency
from utils.helpers import scroll_shim, wait_until_in_viewport, describe_logged_target


class BasePage:
    CART = By.CSS_SELECTOR, '#header-cart button'
    CURRENCY_FORM = By.CSS_SELECTOR, '#form-currency'

    def __init__(self, browser: WebDriver, logger: logging.Logger | None = None):
        self.browser = browser
        self._config_logger(logger)

    def _config_logger(self, logger: logging.Logger | None):
        self.logger = logger or logging.getLogger(type(self).__name__)
        # self.logger.propagate = False # if False do not attach log to allure

        level = getattr(self.browser, 'log_level', logging.INFO)
        self.logger.setLevel(level)

        log_to_file = getattr(self.browser, 'log_to_file', False)
        if log_to_file:
            os.makedirs('logs', exist_ok=True)
            test_name = getattr(self.browser, 'test_name', 'test').replace('/', '_').replace('\\', '_')
            safe_name = test_name
            if len(safe_name) > 50:
                hash_suffix = hashlib.md5(test_name.encode()).hexdigest()[:8]
                safe_name = f'{test_name[:50]}_{hash_suffix}'
            log_path = f'logs/{safe_name}.log'

            already = any(
                isinstance(h, logging.FileHandler) and getattr(h, 'baseFilename', None) == os.path.abspath(log_path)
                for h in self.logger.handlers
            )
            if not already:
                fh = logging.FileHandler(log_path, mode='w')
                fmt = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
                fh.setFormatter(fmt)
                self.logger.addHandler(fh)

    def get_element(
            self,
            locator: tuple[str, str],
            root: WebElement | None = None,
            timeout: float = 5
    ) -> WebElement:
        self.logger.debug(f'Get element: {describe_logged_target(locator)}')
        try:
            search_context = root or self.browser
            return WebDriverWait(search_context, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element {describe_logged_target(locator)} not found on {self.browser.current_url}")
            raise

    def get_elements(
            self,
            locator: tuple[str, str],
            root: WebElement | None = None,
            timeout: float = 5
    ) -> list[WebElement]:
        self.logger.debug(f'Get elements: {describe_logged_target(locator)}')
        try:
            search_context = root or self.browser
            return WebDriverWait(search_context, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.logger.error(f'Elements {describe_logged_target(locator)} not found on {self.browser.current_url}')
            raise

    def get_header_cart(self) -> HeaderCart:
        self.logger.debug('Get header cart.')
        cart = self.get_element(self.CART)
        return HeaderCart(self.browser, cart, self.logger)

    def get_header_currency(self) -> HeaderCurrency:
        self.logger.debug('Get header currency.')
        currency_form = self.get_element(self.CURRENCY_FORM)
        return HeaderCurrency(self.browser, currency_form, self.logger)

    def scroll_and_click(self, target: tuple[str, str] | WebElement) -> None:
        self.logger.debug(f"Scroll to and click element: {describe_logged_target(target)}")
        if isinstance(target, tuple):
            element = self.get_element(target)
        else:
            element = target
        self.logger.debug(f'Element located: {describe_logged_target(element)}')
        scroll_shim(self.browser, element)
        wait_until_in_viewport(self.browser, element, timeout=5, fully=False, unobstructed=True)
        element.click()

    def input_value(self, locator: tuple[str, str], text: str):
        self.logger.debug(f'Input "{text}" into {describe_logged_target(locator)}')
        element = self.get_element(locator)
        self.scroll_and_click(element)
        element.clear()
        for letter in text:
            element.send_keys(letter)
