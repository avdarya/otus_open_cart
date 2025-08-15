from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from pages.components.product_card import ProductCard
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import get_parsed_currency, describe_logged_target


class BaseProductPage(BasePage):
    PRODUCT_CARD = By.XPATH, '//div[contains(@class, "product-thumb")][.//h4/a[contains(normalize-space(.), "{}")]]'
    PRODUCT_CARDS = By.CSS_SELECTOR, '.product-thumb'
    PRICE_NEW = By.CSS_SELECTOR, 'span.price-new'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def get_product_card(self, product: str) -> ProductCard:
        self.logger.debug(f'''Getting product card for "{product}": locator: {
            describe_logged_target((
                self.PRODUCT_CARD[0],
                self.PRODUCT_CARD[1].format(product)
            ))
        }''')
        card = self.get_element((
            self.PRODUCT_CARD[0],
            self.PRODUCT_CARD[1].format(product)
        ))
        return ProductCard(self.browser, card, self.logger)

    def get_product_cards(self) -> list[ProductCard]:
        self.logger.debug(f'Getting product cards: locator: {describe_logged_target(self.PRODUCT_CARDS)}')
        cards = self.get_elements(self.PRODUCT_CARDS)
        self.logger.debug(f'Found {len(cards)} product cards: {cards}')
        return [ProductCard(self.browser, card) for card in cards]

    def get_all_prices_new(self) -> list[str]:
        prices = [card.get_price_new() for card in self.get_product_cards()]
        self.logger.debug(f'Collected {len(prices)} new prices new: {prices}')
        return prices

    def get_all_currencies_new(self) -> set[str]:
        currencies = {get_parsed_currency(card.get_price_new()) for card in self.get_product_cards()}
        self.logger.debug(f'Collected {len(currencies)} new currencies new: {currencies}')
        return currencies

    def get_all_prices_old(self) -> list[str]:
        prices = []
        for card in self.get_product_cards():
            old_price = card.get_price_old()
            if old_price:
                prices.append(old_price)
        self.logger.debug(f'Collected {len(prices)} old prices old: {prices}')
        return prices

    def get_all_currencies_old(self) -> set[str]:
        currencies = set()
        for card in self.get_product_cards():
            old_price = card.get_price_old()
            if old_price:
                currencies.add(get_parsed_currency(old_price))
        self.logger.debug(f'Collected {len(currencies)} old currencies old: {currencies}')
        return currencies

    def get_all_prices_tax(self) -> list[str]:
        taxes = [card.get_price_tax() for card in self.get_product_cards()]
        self.logger.debug(f'Collected {len(taxes)} new prices tax: {taxes}')
        return taxes

    def get_all_currencies_tax(self) -> set[str]:
        currencies = {get_parsed_currency(card.get_price_tax()) for card in self.get_product_cards()}
        self.logger.debug(f'Collected {len(currencies)} new currencies tax: {currencies}')
        return currencies

    def wait_currency_symbol(self, currency: str) -> None:
        self.logger.debug(f'Waiting currency symbol: {currency}: locator: {describe_logged_target(self.PRICE_NEW)}')
        WebDriverWait(self.browser, 5).until(
            EC.text_to_be_present_in_element(self.PRICE_NEW, currency)
        )

    def switch_currency(self, target_currency: str) -> None:
        self.logger.debug(f'Switching currency to {target_currency}')
        header_currency = self.get_header_currency()
        header_currency.click_currency_form().select_currency(target_currency)
        self.wait_currency_symbol(target_currency)
