import allure
from selenium.webdriver.ie.webdriver import WebDriver
from pages.admin_panel.dashboard_page import DashboardPage
from pages.admin_panel.login_page import LoginPage


@allure.epic('Admin panel')
@allure.feature('Authorization')
@allure.story('Valid credentials')
@allure.title('Authorization with admin credentials')
def test_login_admin(browser: WebDriver, base_url: str, username: str, password: str):
    LoginPage(browser, base_url) \
        .open_login_page() \
        .fill_username(username) \
        .fill_password(password) \
        .click_submit_button()
    profile_name = DashboardPage(browser).get_profile_name()
    DashboardPage(browser).click_logout_button()

    assert 'John Doe' in profile_name
    assert LoginPage(browser, base_url).is_visible_username_input()
    assert LoginPage(browser, base_url).is_visible_password_input()
    assert LoginPage(browser, base_url).is_visible_submit_button()