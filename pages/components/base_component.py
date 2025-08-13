from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import scroll_shim, wait_until_in_viewport


class BaseComponent:

    def __init__(self, browser: WebDriver, root: WebElement):
        self.browser = browser
        self.root = root

    def get_element(self, locator: tuple[str, str], timeout: float = 5) -> WebElement:
        return WebDriverWait(self.browser, timeout).until(
            lambda d: self.root.find_element(*locator)
        )

    def get_elements(self, locator: tuple[str, str], timeout: float = 5) -> list[WebElement]:
        WebDriverWait(self.browser, timeout).until(
            lambda d: len(self.root.find_elements(*locator)) > 0
        )
        return self.root.find_elements(*locator)

    def scroll_and_click(self, target: tuple[str, str] | WebElement) -> None:
        if isinstance(target, tuple):
            element = self.get_element(target)
        else:
            element = target
        scroll_shim(self.browser, element)
        wait_until_in_viewport(self.browser, element, timeout=5, fully=False, unobstructed=True)
        element.click()

    def refresh_root(self, locator: tuple[str, str]) -> None:
        self.root = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(locator)
        )

