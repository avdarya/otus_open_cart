import json
import logging
import os
import pathlib
import hashlib
import re
from dataclasses import dataclass
from typing import Generator, Any

import allure
import pytest
import dotenv
from _pytest.reports import TestReport
from pytest import Item, FixtureRequest
from _pytest.runner import CallInfo
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
    parser.addoption('--project_log_level', default='INFO')
    parser.addoption("--log_to_file", action="store_true")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo[Any]):
    outcome = yield
    rep: TestReport = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(autouse=True)
def screenshot_on_failure(browser: WebDriver, request: FixtureRequest):
    yield
    rep = getattr(request.node, 'rep_call', None)

    if rep and rep.failed and not getattr(rep, 'wasxfail', False):
        try:
            allure.attach(
                name='failure_screenshot',
                body=browser.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass
        try:
            allure.attach(
                name='page_source',
                body=browser.page_source,
                attachment_type=allure.attachment_type.HTML
            )
        except Exception:
            pass

def _safe_name(nodeid: str) -> str:
    name = re.sub(r'[\\/: ]', '_', nodeid)
    return (name[:60] + '_' + hashlib.md5(name.encode()).hexdigest()[:8]) if len(name) > 70 else name

@pytest.fixture
def logger(request: FixtureRequest) -> logging.Logger:
    log_level = request.config.getoption('--project_log_level')
    log_to_file = request.config.getoption('--log_to_file')

    root = logging.getLogger()
    root.setLevel(logging.WARNING)

    app = logging.getLogger('pages')
    app.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    app.propagate = False

    for h in list(app.handlers):
        if isinstance(h, (logging.FileHandler, logging.StreamHandler)):
            app.removeHandler(h)
            try:
                h.close()
            except Exception:
                pass

    if log_to_file:
        os.makedirs('logs', exist_ok=True)
        fname = os.path.abspath(f'logs/{_safe_name(request.node.nodeid)}.log')
        fh = logging.FileHandler(fname, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s'))
        app.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s'))
    app.addHandler(sh)

    return logging.getLogger('tests')

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
def browser(request: FixtureRequest) -> Generator[WebDriver, Any, None]:
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

    # request.addfinalizer(driver.quit) # for return

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities, indent=4, ensure_ascii=False),
        attachment_type=allure.attachment_type.JSON
    )

    driver.set_window_size(1280, 800)
    driver.get(url)

    yield driver

    driver.quit()

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