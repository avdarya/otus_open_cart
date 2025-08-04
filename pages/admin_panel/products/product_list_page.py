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

    def __init__(self, browser: WebDriver):
        super().__init__(browser)

    def refresh_page(self) -> 'ProductListPage':
        self.browser.refresh()
        return self

    def click_add_new(self) -> None:
        self.scroll_and_click(self.ADD_NEW)

    def click_delete(self) -> 'ProductListPage':
        self.scroll_and_click(self.DELETE_BUTTON)
        return self

    def confirm_delete(self) -> 'ProductListPage':
        alert = WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert.accept()
        return self

    def select_product(self, name: str) -> 'ProductListPage':
        while True:
            rows = self.get_elements(self.PRODUCT_ROWS)

            for row in rows:
                name_cell = row.find_element(*self.NAME_CELL).text.split('\n')[0].strip()

                if name == name_cell:
                    checkbox = row.find_element(*self.CHECKBOX_CELL)
                    self.scroll_and_click(checkbox)
                    return self
            next_buttons = self.browser.find_elements(*self.NEXT_BUTTON)
            if not next_buttons:
                break
            self.scroll_and_click(next_buttons[0])
            WebDriverWait(self.browser, 5).until(EC.staleness_of(rows[0]))

        raise AssertionError(f"Продукт с названием '{name}' не найден на всех страницах")

    def is_product_in_list(self, name: str, model: str, price: float, quantity: int) -> bool:
        while True:
            rows = self.get_elements(self.PRODUCT_ROWS)

            for row in rows:
                name_cell = row.find_element(*self.NAME_CELL).text.split('\n')[0].strip()
                model_cell = row.find_element(*self.MODEL_CELL).text
                price_cell = row.find_element(*self.PRICE_CELL).text.strip()
                quantity_cell = row.find_element(*self.QUANTITY_CELL).text

                if (name == name_cell and
                    model == model_cell and
                    str(price) in price_cell and
                    quantity == int(quantity_cell)
                ):
                    return True

            next_buttons = self.browser.find_elements(*self.NEXT_BUTTON)
            if not next_buttons:
                break
            self.scroll_and_click(next_buttons[0])
            WebDriverWait(self.browser, 5).until(EC.staleness_of(rows[0]))

        return False