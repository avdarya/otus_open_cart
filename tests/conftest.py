import os
import pathlib
from dataclasses import dataclass

import pytest
import dotenv
from _pytest.fixtures import FixtureRequest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.remote.webdriver import WebDriver

from pages.admin_panel.dashboard_page import DashboardPage
from pages.admin_panel.login_page import LoginPage
from pages.admin_panel.products.product_form_page import ProductFormPage
from pages.admin_panel.products.product_list_page import ProductListPage

dotenv.load_dotenv()
DRIVER_PATH = pathlib.Path(__file__).parent.resolve().parent / 'drivers'
fake: Faker = Faker()

@dataclass
class CustomerData:
    first_name: str
    last_name: str
    email: str
    password: str

@dataclass
class ProductData:
    name: str
    meta_tag: str
    description: str
    model: str
    price: float
    quantity: int
    keyword: str

def pytest_addoption(parser):
    parser.addoption('--browser', default='ch')
    parser.addoption('--base_url', default=f'http://{os.getenv("LOCAL_IP")}:{os.getenv("OPENCART_PORT")}')
    parser.addoption('--driver', default=DRIVER_PATH)

@pytest.fixture(scope='session')
def base_url(request: FixtureRequest):
    return request.config.getoption('--base_url')

@pytest.fixture
def username(request: FixtureRequest) -> str:
    return os.getenv('OPENCART_USERNAME')

@pytest.fixture
def password(request: FixtureRequest) -> str:
    return os.getenv('OPENCART_PASSWORD')

@pytest.fixture
def browser(request: FixtureRequest) -> WebDriver:
    url = request.config.getoption('--base_url')
    browser_name = request.config.getoption('--browser')
    driver_path = request.config.getoption('--driver')

    if browser_name in ('ch', 'chrome'):
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif browser_name in ('ff', 'firefox'):
        options = FFOptions()
        driver = webdriver.Firefox(options=options)
    elif browser_name in ('ya', 'yandex'):
        service = ChromeService(executable_path=f'{driver_path}/yandexdriver')
        options = ChromeOptions()
        # options.binary.location = ''
        driver = webdriver.Chrome(service=service, options=options)
    else:
        raise Exception('Driver not supported')

    request.addfinalizer(driver.quit)

    driver.set_window_size(1280, 800)

    driver.get(url)

    return driver

@pytest.fixture
def admin_browser(browser: WebDriver, base_url: str, username: str, password: str) -> WebDriver:
    LoginPage(browser, base_url) \
        .open_login_page() \
        .fill_username(username) \
        .fill_password(password) \
        .click_submit_button()
    return browser

@pytest.fixture
def generate_customer_data() -> CustomerData:
        return CustomerData(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password=fake.password()
    )

@pytest.fixture
def generate_product_data() -> ProductData:
    name = fake.word().capitalize()
    return ProductData(
        name=name,
        meta_tag=name,
        description=fake.paragraph(nb_sentences=2),
        model=fake.bothify(text='Model-##??'),
        price=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
        quantity=fake.random_int(min=1, max=100),
        keyword=fake.slug()
    )

@pytest.fixture
def added_product(admin_browser: WebDriver, generate_product_data: ProductData) -> ProductData:
    DashboardPage(admin_browser) \
        .get_navigation_menu() \
        .click_catalog() \
        .click_products()
    ProductListPage(admin_browser).click_add_new()
    product_form_page = ProductFormPage(admin_browser)
    product_form_page \
        .fill_product_name(generate_product_data.name) \
        .fill_description(generate_product_data.description) \
        .fill_meta_tag_title(generate_product_data.meta_tag) \
        .click_tab_data() \
        .fill_model(generate_product_data.model) \
        .fill_price(generate_product_data.price) \
        .fill_quantity(generate_product_data.quantity) \
        .click_tab_seo() \
        .fill_keyword(generate_product_data.keyword) \
        .click_save()
    return generate_product_data