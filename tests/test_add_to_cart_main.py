import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import scroll_shim, wait_until_in_viewport


@pytest.mark.parametrize('product, price', [('MacBook', 602.00)])
def test_add_to_cart_from_main(browser: WebDriver, base_url: str, product: str, price: float):
    browser.get(base_url)

    cart_button_text_before = browser.find_element(By.CSS_SELECTOR, '#header-cart button').text
    cart_counter_before = ' '.join(cart_button_text_before.split()).strip(' ')[0]
    cart_cost_before =  ' '.join(cart_button_text_before.split()).split('$')[1]

    selector_add_btn = f'//div[@class="product-thumb"][.//h4/a[text()="{product}"]]//button[contains(@formaction, "checkout/cart.add")]'
    add_button = browser.find_element(By.XPATH, selector_add_btn)

    scroll_shim(browser, add_button)
    wait_until_in_viewport(browser, add_button, timeout=5, fully=False, unobstructed=True)
    add_button.click()

    WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.invisibility_of_element((By.CSS_SELECTOR, 'div.alert')))

    cart_button_after = browser.find_element(By.CSS_SELECTOR, '#header-cart')

    scroll_shim(browser, cart_button_after)
    wait_until_in_viewport(browser, cart_button_after, timeout=10, fully=False, unobstructed=True)

    cart_button_text_after = browser.find_element(By.CSS_SELECTOR, '#header-cart button').text
    cart_counter_after = ' '.join(cart_button_text_after.split()).strip(' ')[0]
    cart_cost_after =  ' '.join(cart_button_text_after.split()).split('$')[1]

    cart_button_after.click()

    cart_link = WebDriverWait(
        driver=browser,
        timeout=10,
        poll_frequency=0.5
    ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.dropdown a[href*=cart]')))
    cart_link.click()

    product_name = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//td[@class="text-start text-wrap"]/a[contains(text(), "{product}")]')
        )
    )

    product_count = browser.find_element(By.CSS_SELECTOR, 'input[name="quantity"]')
    product_price = browser.find_element(By.XPATH, f'//td[@class="text-start text-wrap"]/a[text()="{product}"]/ancestor::tr/td[@class="text-end"][1]')

    assert int(cart_counter_before) + 1 == int(cart_counter_after)
    assert float(cart_cost_before) + price == float(cart_cost_after)
    assert product_name.text == product
    assert product_count.get_attribute('value') == '1'
    assert str(price) in product_price.text
