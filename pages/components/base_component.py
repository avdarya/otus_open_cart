import logging

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import scroll_shim, wait_until_in_viewport, describe_logged_target


class BaseComponent:

    def __init__(self, browser: WebDriver, root: WebElement, logger: logging.Logger | None = None):
        self.browser = browser
        self.root = root
        self.logger = logger or logging.getLogger(type(self).__name__)

    def get_element(
            self,
            locator: tuple[str, str],
            root: WebElement | None = None,
            timeout: float = 5
    ) -> WebElement:
        self.logger.debug(f'Get element: {describe_logged_target(locator)}')
        try:
            search_context = root or self.root
            return WebDriverWait(search_context, timeout).until(
                lambda d: search_context.find_element(*locator)
            )
        except TimeoutException:
            self.logger.error(f"Element {describe_logged_target(locator)} not found on {self.browser.current_url}")
            raise

    def get_elements(
            self,
            locator: tuple[str, str],
            root: WebElement | None = None,
            allow_empty: bool = False,
            timeout: float = 5
    ) -> list[WebElement]:
        self.logger.debug(f'Get elements: {describe_logged_target(locator)}')
        search_context = root or self.root
        if allow_empty:
            try:
                return search_context.find_elements(*locator)
            except TimeoutException:
                return []

        try:
            WebDriverWait(search_context, timeout).until(
                lambda d: len(search_context.find_elements(*locator)) > 0
            )
            return search_context.find_elements(*locator)
        except TimeoutException:
            self.logger.error(f'Elements {describe_logged_target(locator)} not found on {self.browser.current_url}')
            raise

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

    def refresh_root(self, locator: tuple[str, str]) -> None:
        self.logger.debug(f'Refresh root element: {describe_logged_target(locator)}')
        self.root = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(locator)
        )

