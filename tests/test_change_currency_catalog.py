import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import extract_price_data_from_products


@pytest.mark.parametrize('currency', ['€', '£'], ids=['Euro', 'Pound Sterling'])
def test_change_currency_catalog(browser: WebDriver, base_url: str, currency: str):
    browser.get(f'{base_url}/en-gb/catalog/desktops')

    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.price-new')))

    selector_price_new, selector_price_old, selector_price_tax = ('span.price-new', 'span.price-old', 'span.price-tax')

    selector_by_elements_before = {
        selector_price_new: (browser.find_elements(By.CSS_SELECTOR, 'span.price-new'), lambda t: t),
        selector_price_old: (browser.find_elements(By.CSS_SELECTOR, 'span.price-old'), lambda t: t),
        selector_price_tax: (
            browser.find_elements(By.CSS_SELECTOR, 'span.price-tax'),
            lambda t: t.split('Ex Tax: ')[1] if 'Ex Tax: ' in t else t)
    }
    price_data_before = extract_price_data_from_products(selector_by_elements_before)
    product_cards_before = browser.find_elements(By.CSS_SELECTOR, 'div.product-thumb')

    first_price = browser.find_element(By.CSS_SELECTOR, 'span.price-new')
    browser.find_element(By.CSS_SELECTOR, '#form-currency').click()
    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#form-currency ul.dropdown-menu')))
    browser.find_element(By.XPATH, f'//a[contains(text(), "{currency}")]').click()
    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.staleness_of(first_price))

    selector_by_elements_after = {
        selector_price_new: (browser.find_elements(By.CSS_SELECTOR, 'span.price-new'), lambda t: t),
        selector_price_old: (browser.find_elements(By.CSS_SELECTOR, 'span.price-old'), lambda t: t),
        selector_price_tax: (
            browser.find_elements(By.CSS_SELECTOR, 'span.price-tax'),
            lambda t: t.split('Ex Tax: ')[1] if 'Ex Tax: ' in t else t)
    }
    price_data_after = extract_price_data_from_products(selector_by_elements_after)
    product_cards_after = browser.find_elements(By.CSS_SELECTOR, 'div.product-thumb')

    assert len(product_cards_before) == len(product_cards_after)
    assert price_data_after[f'currency_{selector_price_new}'] == {currency}
    assert price_data_after[f'currency_{selector_price_tax}'] == {currency}
    assert (price_data_before[f'price_{selector_price_new}'] != price_data_after[f'price_{selector_price_new}'] or
           price_data_before[f'currency_{selector_price_new}'] != price_data_after[f'currency_{selector_price_new}'] )
    assert (price_data_before[f'price_{selector_price_old}'] != price_data_after[f'price_{selector_price_old}'] or
            price_data_before[f'currency_{selector_price_old}'] != price_data_after[f'currency_{selector_price_old}'])
    assert (price_data_before[f'price_{selector_price_tax}'] != price_data_after[f'price_{selector_price_tax}'] or
            price_data_before[f'currency_{selector_price_tax}'] != price_data_after[f'currency_{selector_price_tax}'] )

@pytest.mark.parametrize('currency', ['$'], ids=['Dollar'])
def test_change_dollar_currency_catalog(browser: WebDriver, base_url: str, currency: str):
    browser.get(f'{base_url}/en-gb/catalog/desktops')

    first_price = browser.find_element(By.CSS_SELECTOR, 'span.price-new')
    browser.find_element(By.CSS_SELECTOR, '#form-currency').click()
    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#form-currency ul.dropdown-menu')))
    browser.find_element(By.XPATH, '//a[contains(text(), "£")]').click()
    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.staleness_of(first_price))

    selector_price_new, selector_price_old, selector_price_tax = ('span.price-new', 'span.price-old', 'span.price-tax')

    selector_by_elements_before = {
        selector_price_new: (browser.find_elements(By.CSS_SELECTOR, 'span.price-new'), lambda t: t),
        selector_price_old: (browser.find_elements(By.CSS_SELECTOR, 'span.price-old'), lambda t: t),
        selector_price_tax: (
            browser.find_elements(By.CSS_SELECTOR, 'span.price-tax'),
            lambda t: t.split('Ex Tax: ')[1] if 'Ex Tax: ' in t else t)
    }
    price_data_before = extract_price_data_from_products(selector_by_elements_before)
    product_cards_before = browser.find_elements(By.CSS_SELECTOR, 'div.product-thumb')

    first_price = browser.find_element(By.CSS_SELECTOR, 'span.price-new')
    browser.find_element(By.CSS_SELECTOR, '#form-currency').click()
    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#form-currency ul.dropdown-menu')))
    browser.find_element(By.XPATH, f'//a[contains(text(), "{currency}")]').click()
    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.staleness_of(first_price))

    selector_by_elements_after = {
        selector_price_new: (browser.find_elements(By.CSS_SELECTOR, 'span.price-new'), lambda t: t),
        selector_price_old: (browser.find_elements(By.CSS_SELECTOR, 'span.price-old'), lambda t: t),
        selector_price_tax: (
            browser.find_elements(By.CSS_SELECTOR, 'span.price-tax'),
            lambda t: t.split('Ex Tax: ')[1] if 'Ex Tax: ' in t else t)
    }
    price_data_after = extract_price_data_from_products(selector_by_elements_after)
    product_cards_after = browser.find_elements(By.CSS_SELECTOR, 'div.product-thumb')

    assert len(product_cards_before) == len(product_cards_after)
    assert price_data_after[f'currency_{selector_price_new}'] == {currency}
    assert price_data_after[f'currency_{selector_price_tax}'] == {currency}
    assert (price_data_before[f'price_{selector_price_new}'] != price_data_after[f'price_{selector_price_new}'] or
           price_data_before[f'currency_{selector_price_new}'] != price_data_after[f'currency_{selector_price_new}'] )
    assert (price_data_before[f'price_{selector_price_old}'] != price_data_after[f'price_{selector_price_old}'] or
            price_data_before[f'currency_{selector_price_old}'] != price_data_after[f'currency_{selector_price_old}'])
    assert (price_data_before[f'price_{selector_price_tax}'] != price_data_after[f'price_{selector_price_tax}'] or
            price_data_before[f'currency_{selector_price_tax}'] != price_data_after[f'currency_{selector_price_tax}'] )
