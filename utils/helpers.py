import re
from typing import Callable

from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


def _parse_price_parts(price_text: str) -> tuple[str, float]:
    match = re.match(r'([^\d.,]*)([\d.,]+)([^\d.,]*)', price_text)
    if not match:
        raise ValueError(f'Failed to extract currency and price from {price_text}')

    prefix = match.group(1)
    number = match.group(2)
    suffix = match.group(3)

    currency = prefix if prefix else suffix
    price = float(number.replace(',', ''))

    return currency, price

def get_parsed_currency(price_text: str) -> str:
    return _parse_price_parts(price_text)[0]

def get_parsed_price(price_text: str) -> float:
    return _parse_price_parts(price_text)[1]

def extract_price_data_from_products(selectors: dict[str, tuple[list[WebElement], Callable]]) -> dict[str, str|float]:
    result = {}

    for k, (elements, transform) in selectors.items():
        texts = [transform(el.text) for el in elements]
        result[f'price_{k}'] = [get_parsed_price(t) for t in texts]
        result[f'currency_{k}'] = {get_parsed_currency(t) for t in texts}

    return result

def scroll_shim(driver: WebDriver, element: WebElement):
    x = element.location['x']
    y = element.location['y']
    driver.execute_script(
        "window.scrollTo(arguments[0], arguments[1] - window.innerHeight / 2);",
        x, y
    )

def _in_viewport(driver, element, fully=False):
    return driver.execute_script("""
        const el = arguments[0];
        const fully = arguments[1];
        const rect = el.getBoundingClientRect();
        const vh = window.innerHeight || document.documentElement.clientHeight;
        const vw = window.innerWidth  || document.documentElement.clientWidth;
        if (fully) {
            return rect.top >= 0 && rect.left >= 0 &&
                   rect.bottom <= vh && rect.right <= vw;
        } else {
            return rect.bottom > 0 && rect.right > 0 &&
                   rect.top    < vh && rect.left  < vw;
        }
    """, element, fully)

def _centerpoint_visible(driver, element):
    return driver.execute_script("""
        const el   = arguments[0];
        const rect = el.getBoundingClientRect();
        const cx = rect.left + rect.width  / 2;
        const cy = rect.top  + rect.height / 2;
        const e = document.elementFromPoint(cx, cy);
        for (let n = e; n; n = n.parentElement) {
            if (n === el) return true;
        }
        return false;
    """, element)

def wait_until_in_viewport(
        driver: WebDriver,
        element: WebElement,
        timeout: float = 5,
        fully: bool = False,
        unobstructed: bool = False
):
    def _cond(drv):
        if not _in_viewport(drv, element, fully=fully):
            return False
        if unobstructed and not _centerpoint_visible(drv, element):
            return False
        return True
    WebDriverWait(driver, timeout).until(_cond)
    return element