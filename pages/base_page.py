from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.components.header_cart import HeaderCart
from pages.components.header_currency import HeaderCurrency
from utils.helpers import scroll_shim, wait_until_in_viewport


class BasePage:
    CART = By.CSS_SELECTOR, '#header-cart button'
    CURRENCY_FORM = By.CSS_SELECTOR, '#form-currency'

    def __init__(self, browser: WebDriver):
        self.browser = browser

    def get_element(self, locator: tuple[str, str], timeout: float = 5) -> WebElement:
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def get_elements(self, locator: tuple[str, str], timeout: float = 5) -> list[WebElement]:
        return WebDriverWait(self.browser, timeout).until(EC.visibility_of_all_elements_located(locator))

    def get_header_cart(self) -> HeaderCart:
        cart = self.get_element(self.CART)
        return HeaderCart(self.browser, cart)

    def get_header_currency(self) -> HeaderCurrency:
        currency_form = self.get_element(self.CURRENCY_FORM)
        return HeaderCurrency(self.browser, currency_form)

    def scroll_and_click(self, target: tuple[str, str] | WebElement) -> None:
        if isinstance(target, tuple):
            element = self.get_element(target)
        else:
            element = target
        scroll_shim(self.browser, element)
        wait_until_in_viewport(self.browser, element, timeout=5, fully=False, unobstructed=True)
        element.click()

    def input_value(self, locator: tuple[str, str], text: str):
        element = self.get_element(locator)
        self.scroll_and_click(element)
        element.clear()
        for letter in text:
            element.send_keys(letter)

