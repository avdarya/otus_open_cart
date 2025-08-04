from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.components.base_component import BaseComponent


class HeaderCart(BaseComponent):
    CART = By.CSS_SELECTOR, '#header-cart button'
    VIEW_CART = By.CSS_SELECTOR, 'div.dropdown a[href*=cart]'

    def __init__(self, browser: WebDriver, root: WebElement):
        super().__init__(browser, root)

    def get_counter_cost(self) -> tuple[int, float]:
        self.refresh_root(self.CART)
        cart_text = self.root.text.strip()
        counter = int(cart_text.split()[0])
        cost = float(cart_text.split('$')[1])
        return counter, cost

    def click_cart_btn(self) -> 'HeaderCart':
        self.scroll_and_click(self.CART)
        return self

    def go_to_cart_page(self) -> None:
        self.refresh_root(self.CART)
        self.scroll_and_click(self.root)
        view_cart = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable(self.VIEW_CART)
        )
        view_cart.click()

