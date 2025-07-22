import os
import pathlib
import pytest
import dotenv
from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.ie.webdriver import WebDriver

dotenv.load_dotenv()
DRIVER_PATH = pathlib.Path(__file__).parent.resolve().parent / 'drivers'

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
    browser_name = request.config.getoption('--browser')
    driver_path = request.config.getoption('--driver')

    if browser_name in ('ch', 'chrome'):
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif browser_name in ('ff', 'firefox'):
        options = FFOptions()
        driver = webdriver.Firefox(options=options)
    elif browser_name in ('sf', 'safari'):
        driver = webdriver.Safari()
    elif browser_name in ('ya', 'yandex'):
        service = ChromeService(executable_path=f'{driver_path}/yandexdriver')
        options = ChromeOptions()
        # options.binary.location = ''
        driver = webdriver.Chrome(service=service, options=options)
    else:
        raise Exception('Driver not supported')

    request.addfinalizer(driver.quit)

    driver.set_window_size(1280, 800)

    return driver