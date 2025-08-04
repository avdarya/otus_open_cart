from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_TITLE = By.CSS_SELECTOR, '#content h1'
    PRICE_NEW = By.CSS_SELECTOR, 'span.price-new'
    DESCRIPTION = By.CSS_SELECTOR, '#tab-description p.intro'
    ADD_BUTTON = By.CSS_SELECTOR, '#button-cart'
    REVIEW_STARS = By.CSS_SELECTOR, 'span.fa-stack'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def get_product_title(self) -> str:
        return self.get_element(self.PRODUCT_TITLE).text

    def get_price_new(self) -> str:
        return self.get_element(self.PRICE_NEW).text

    def get_description(self) -> str:
        description = self.get_element(self.DESCRIPTION).text
        return ' '.join(description.split())

    def is_visible_add_button(self) -> bool:
        return self.get_element(self.ADD_BUTTON).is_displayed()

    def get_stars_count(self) -> int:
        stars = self.get_elements(self.REVIEW_STARS)
        return len(stars)

