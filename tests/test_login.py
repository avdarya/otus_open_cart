from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login_administration(browser: WebDriver, base_url: str, username: str, password: str):
    browser.get(f'{base_url}/administration')

    browser.find_element(By.CSS_SELECTOR, '#input-username').send_keys(username)
    browser.find_element(By.CSS_SELECTOR, '#input-password').send_keys(password)
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    profile_name = WebDriverWait(
            driver=browser,
            timeout=5,
            poll_frequency=0.5
        ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#nav-profile'))).text

    logout_button = WebDriverWait(
            driver=browser,
            timeout=5,
            poll_frequency=0.5
        ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#nav-logout')))

    logout_button.click()

    username_input = WebDriverWait(
            driver=browser,
            timeout=5,
            poll_frequency=0.5
        ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#input-username')))
    password_input = WebDriverWait(
            driver=browser,
            timeout=5,
            poll_frequency=0.5
        ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#input-password')))
    login_button = WebDriverWait(
            driver=browser,
            timeout=5,
            poll_frequency=0.5
        ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

    assert 'John Doe' in profile_name
    assert username_input.is_displayed()
    assert password_input.is_displayed()
    assert login_button.is_displayed()