import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.admin_panel.base_admin_page import BaseAdminPage


class ProductFormPage(BaseAdminPage):
    TAB_DATA = By.CSS_SELECTOR, 'a[href="#tab-data"]'
    TAB_SEO = By.CSS_SELECTOR, 'a[href="#tab-seo"]'
    PRODUCT_NAME_INPUT = By.CSS_SELECTOR, '#input-name-1'
    FRAME_DESCRIPTION = By.CSS_SELECTOR, 'iframe[title*="input-description-1"]'
    DESCRIPTION_INPUT = By.CSS_SELECTOR, 'body'
    META_TAG_INPUT = By.CSS_SELECTOR, '#input-meta-title-1'
    MODEL_INPUT = By.CSS_SELECTOR, '#input-model'
    PRICE_INPUT = By.CSS_SELECTOR, '#input-price'
    QUANTITY_INPUT = By.CSS_SELECTOR, '#input-quantity'
    KEYWORD_INPUT = By.CSS_SELECTOR, '#input-keyword-0-1'
    SAVE_BUTTON = By.CSS_SELECTOR, 'button[type="submit"]'
    BACK_BUTTON = By.CSS_SELECTOR, 'div.float-end a.btn.btn-light'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Нажать на Таб Данные')
    def click_tab_data(self) -> 'ProductFormPage':
        self.logger.info('Click Tab Data')
        self.scroll_and_click(self.TAB_DATA)
        return self

    @allure.step('Нажать на Таб SEO')
    def click_tab_seo(self) -> 'ProductFormPage':
        self.logger.info('Click Tab SEO')
        self.scroll_and_click(self.TAB_SEO)
        return self

    @allure.step('Заполнить поле Название продукта "{product_name}"')
    def fill_product_name(self, product_name: str) -> 'ProductFormPage':
        self.logger.info(f'Fill product name: {product_name}')
        self.input_value(self.PRODUCT_NAME_INPUT, product_name)
        return self

    @allure.step('Заполнить поле Описание продукта')
    def fill_description(self, description: str) -> 'ProductFormPage':
        self.logger.info(f'Fill description: {description}')
        self.logger.info('Switch to description frame')
        frame = self.get_element(self.FRAME_DESCRIPTION)
        self.browser.switch_to.frame(frame)
        try:
            self.input_value(self.DESCRIPTION_INPUT, description)
        finally:
            self.browser.switch_to.default_content()
        return self

    @allure.step('Заполнить поле Мета тэг "{meta_tag}"')
    def fill_meta_tag_title(self, meta_tag: str) -> 'ProductFormPage':
        self.logger.info(f'Fill meta tag title: {meta_tag}')
        self.input_value(self.META_TAG_INPUT, meta_tag)
        return self

    @allure.step('Заполнить поле Модель "{model}"')
    def fill_model(self, model: str) -> 'ProductFormPage':
        self.logger.info(f'Fill model: {model}')
        self.input_value(self.MODEL_INPUT, model)
        return self

    @allure.step('Заполнить поле Цену "{price}"')
    def fill_price(self, price: float) -> 'ProductFormPage':
        self.logger.info(f'Fill price: {price}')
        self.input_value(self.PRICE_INPUT, str(price))
        return self

    @allure.step('Заполнить поле Количество "{quantity}"')
    def fill_quantity(self, quantity: int) -> 'ProductFormPage':
        self.logger.info(f'Fill quantity: {quantity}')
        self.input_value(self.QUANTITY_INPUT, str(quantity))
        return self

    @allure.step('Заполнить поле Ключевые слова "{keyword}"')
    def fill_keyword(self, keyword: str) -> 'ProductFormPage':
        self.logger.info(f'Fill keyword: {keyword}')
        self.input_value(self.KEYWORD_INPUT, keyword)
        return self

    @allure.step('Нажать на кнопку Сохранить')
    def click_save(self) -> 'ProductFormPage':
        self.logger.info('Click Save button')
        self.scroll_and_click(self.SAVE_BUTTON)
        return self

    @allure.step('Нажать на кнопку Назад')
    def click_back(self) -> None:
        self.logger.info('Click Back button')
        self.scroll_and_click(self.BACK_BUTTON)
