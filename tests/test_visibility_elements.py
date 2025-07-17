from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver


def test_main_page(browser: WebDriver, base_url: str):
    browser.get(base_url)

    product = 'MacBook'
    expected_desc = 'Intel Core 2 Duo processor Powered by an Intel Core 2 Duo processor at speeds up to 2.16GHz, t..'
    expected_price = '$602.00'

    product_card = browser.find_element(By.XPATH, f'//div[@class="product-thumb"][.//h4/a[text()="{product}"]]')
    product_title = browser.find_element(By.CSS_SELECTOR, 'div.description a')
    product_description = browser.find_element(By.CSS_SELECTOR, 'div.description p')
    product_price = browser.find_element(By.CSS_SELECTOR, 'span.price-new')
    add_button = browser.find_element(By.CSS_SELECTOR, 'button[formaction*="cart.add"]')

    assert product_card.is_displayed()
    assert product_title.text == product
    assert ' '.join(product_description.text.split()) == expected_desc
    assert product_price.text == expected_price
    assert add_button.is_displayed()


def test_catalog(browser: WebDriver, base_url: str):
    browser.get(f'{base_url}/en-gb/catalog/desktops')

    catalog_title = browser.find_element(By.CSS_SELECTOR, '#content h2')
    compare_button = browser.find_element(By.CSS_SELECTOR, '#compare-total')
    sort_input = browser.find_element(By.CSS_SELECTOR, '#input-sort')
    count_input = browser.find_element(By.CSS_SELECTOR, '#input-limit')
    product_cards = browser.find_elements(By.CSS_SELECTOR, 'div.product-thumb')

    assert catalog_title.text =='Desktops'
    assert compare_button.is_displayed()
    assert sort_input.is_displayed()
    assert count_input.is_displayed()
    assert len(product_cards) == 10

def test_product_page(browser: WebDriver, base_url: str):
    browser.get(f'{base_url}/en-gb/product/iphone')

    title = browser.find_element(By.CSS_SELECTOR, '#content h1')
    price_new = browser.find_element(By.CSS_SELECTOR, 'span.price-new')
    add_button = browser.find_element(By.CSS_SELECTOR, '#button-cart')
    reviews = browser.find_elements(By.CSS_SELECTOR, 'span.fa-stack')
    description = browser.find_element(By.CSS_SELECTOR, '#tab-description p.intro')

    assert title.text == 'iPhone'
    assert add_button.is_displayed()
    assert price_new.text == '$123.20'
    assert len(reviews) == 5
    assert ' '.join(description.text.split()) == 'iPhone is a revolutionary new mobile phone that allows you to make a call by simply tapping a name or number in your address book, a favorites list, or a call log. It also automatically syncs all your contacts from a PC, Mac, or Internet service. And it lets you select and listen to voicemail messages in whatever order you want just like email.'

def test_login_administration(browser: WebDriver, base_url: str):
    browser.get(f'{base_url}/administration')

    username_input = browser.find_element(By.CSS_SELECTOR, '#input-username')
    user_icon = browser.find_element(By.CSS_SELECTOR, 'i.fa-user')
    password_input = browser.find_element(By.CSS_SELECTOR, '#input-password')
    password_icon = browser.find_element(By.CSS_SELECTOR, 'form[id="form-login"] i.fa-lock')
    login_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    assert username_input.is_displayed()
    assert user_icon.is_displayed()
    assert password_input.is_displayed()
    assert password_icon.is_displayed()
    assert login_button.is_displayed()

def test_register_account(browser: WebDriver, base_url: str):
    browser.get(f'{base_url}/index.php?route=account/register')

    first_name_input = browser.find_element(By.CSS_SELECTOR, '#input-firstname')
    last_name_input = browser.find_element(By.CSS_SELECTOR, '#input-lastname')
    email_input = browser.find_element(By.CSS_SELECTOR, '#input-email')
    password_input = browser.find_element(By.CSS_SELECTOR, '#input-password')
    continue_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    assert first_name_input.is_displayed()
    assert last_name_input.is_displayed()
    assert email_input.is_displayed()
    assert password_input.is_displayed()
    assert continue_button.is_displayed()
