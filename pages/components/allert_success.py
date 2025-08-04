from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AlertSuccess:
    SUCCESS_ALERT = By.CSS_SELECTOR, '.alert-success'
    CLOSE_BUTTON = By.CSS_SELECTOR, '.btn-close'

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.alert = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located(self.SUCCESS_ALERT))

    def close_alert(self) -> None:
        self.alert.find_element(*self.CLOSE_BUTTON).click()

    def get_alert_text(self) -> str:
        return self.alert.text
