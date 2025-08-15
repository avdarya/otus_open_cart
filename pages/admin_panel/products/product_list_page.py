import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.admin_panel.base_admin_page import BaseAdminPage


class ProductListPage(BaseAdminPage):
    ADD_NEW = By.CSS_SELECTOR, 'div.float-end a.btn.btn-primary'
    PRODUCT_ROWS = By.CSS_SELECTOR, 'table tbody tr'
    NAME_CELL = By.CSS_SELECTOR, 'td[class="text-start"]'
    MODEL_CELL = By.CSS_SELECTOR,'td[class="text-start d-none d-lg-table-cell"]'
    PRICE_CELL = By.CSS_SELECTOR, 'td.text-end'
    QUANTITY_CELL = By.CSS_SELECTOR, 'td.text-end span'
    CHECKBOX_CELL = By.CSS_SELECTOR, 'input[type="checkbox"]'
    DELETE_BUTTON = By.CSS_SELECTOR, 'button.btn.btn-danger'
    NEXT_BUTTON = By.XPATH, '//ul[@class="pagination"]//a[normalize-space()=">"]'
    PAGINATION_BLOCK = By.CSS_SELECTOR, 'ul.pagination'

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    @allure.step('Обновить страницу')
    def refresh_page(self) -> 'ProductListPage':
        self.logger.info('Refresh Product list page')
        self.logger.debug(f'{self.browser.current_url}')
        self.browser.refresh()
        return self

    @allure.step('Нажать на кнопку Добавить новое')
    def click_add_new(self) -> None:
        self.logger.info('Click Add New button')
        self.scroll_and_click(self.ADD_NEW)

    @allure.step('Нажать на кнопку Удалить')
    def click_delete(self) -> 'ProductListPage':
        self.logger.info('Click Delete button')
        self.scroll_and_click(self.DELETE_BUTTON)
        return self

    @allure.step('Подтвердить удаление')
    def confirm_delete(self) -> 'ProductListPage':
        self.logger.info('Confirm delete in popup')
        alert = WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert.accept()
        return self

    @allure.step('Выбрать продукт "{name}"')
    def select_product(self, name: str) -> 'ProductListPage':
        self.logger.info(f'Select product "{name}"')
        while True:
            rows = self.get_elements(self.PRODUCT_ROWS)

            for row in rows:
                name_cell = self.get_element(self.NAME_CELL, row).text.split('\n')[0].strip()

                if name == name_cell:
                    checkbox = self.get_element(self.CHECKBOX_CELL, row)
                    self.scroll_and_click(checkbox)
                    self.logger.info(f'Product "{name}" found and selected')
                    return self
            next_buttons = self.browser.find_elements(*self.NEXT_BUTTON)
            if not next_buttons:
                break
            self.logger.debug('Product not found on current page, click Next')
            self.scroll_and_click(next_buttons[0])
            WebDriverWait(self.browser, 5).until(EC.staleness_of(rows[0]))

        self.logger.error(f'Product "{name}" not found on any pages')
        raise AssertionError(f'Продукт с названием "{name}" не найден на всех страницах')

    @allure.step('Проверить наличие строки продукта в списке: название={name} модель={model} цена={price} кол-во={quantity}')
    def is_product_in_list(self, name: str, model: str, price: float, quantity: int) -> bool:
        self.logger.info(f'Checking row: name={name}, model={model}, price={price}, quantity={quantity}')
        while True:
            rows = self.get_elements(self.PRODUCT_ROWS)

            for row in rows:
                name_cell = self.get_element(self.NAME_CELL, row).text.split('\n')[0].strip()
                model_cell = self.get_element(self.MODEL_CELL, row).text
                price_cell = self.get_element(self.PRICE_CELL, row).text.strip()
                quantity_cell = self.get_element(self.QUANTITY_CELL, row).text


                if (name == name_cell and
                    model == model_cell and
                    str(price) in price_cell and
                    quantity == int(quantity_cell)
                ):
                    self.logger.info(f'Product "{name}" found')
                    return True

            next_buttons = self.browser.find_elements(*self.NEXT_BUTTON)
            if not next_buttons:
                break
            self.logger.debug('Product not found on current page, click Next')
            self.scroll_and_click(next_buttons[0])
            WebDriverWait(self.browser, 5).until(EC.staleness_of(rows[0]))

        return False