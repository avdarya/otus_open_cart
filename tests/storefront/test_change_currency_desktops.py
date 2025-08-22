import allure
import pytest
from selenium.webdriver.ie.webdriver import WebDriver

from pages.storefront.desktops_page import DesktopsPage

@allure.epic('Storefront')
@allure.feature('Currency management')
@allure.story('Change currency - Desktops page')
@allure.title('Prices update after change currency on Desktops page')
@pytest.mark.parametrize('initial_currency, currency_to_select', [
    ('$', '€'), ('$', '£'), ('£', '$')],
    ids=['Euro', 'Pound Sterling', 'Dollar']
)
def test_updated_prices_after_change_currency_desktops(
        browser: WebDriver,
        base_url: str,
        initial_currency: str,
        currency_to_select: str,
        logger
):
    desktops_page = DesktopsPage(browser, base_url)
    desktops_page.go_to_desktops_page()
    desktops_page.switch_currency(initial_currency)
    header_currency = desktops_page.get_header_currency()

    prices_new_before = desktops_page.get_all_prices_new()
    prices_old_before = desktops_page.get_all_prices_old()
    prices_tax_before = desktops_page.get_all_prices_tax()
    product_cards_before = desktops_page.get_product_cards()

    header_currency.click_currency_form().select_currency(currency_to_select)
    desktops_page.wait_currency_symbol(currency_to_select)

    prices_new_after = desktops_page.get_all_prices_new()
    prices_old_after = desktops_page.get_all_prices_old()
    prices_tax_after = desktops_page.get_all_prices_tax()
    product_cards_after = desktops_page.get_product_cards()

    assert len(product_cards_before) == len(product_cards_after)
    assert prices_new_before != prices_new_after
    assert prices_old_before != prices_old_after
    assert prices_tax_before != prices_tax_after
    assert desktops_page.get_all_currencies_new() == {currency_to_select}
    assert desktops_page.get_all_currencies_old() == {currency_to_select}
    assert desktops_page.get_all_currencies_tax() == {currency_to_select}

@allure.epic('Storefront')
@allure.feature('Currency management')
@allure.story('Change currency - Desktops page')
@allure.title('Update header currency symbol after currency change on Desktops page')
@pytest.mark.parametrize('initial_currency, currency_to_select', [
    ('$', '€'), ('$', '£'), ('£', '$')],
    ids=['Euro', 'Pound Sterling', 'Dollar']
)
def test_updated_header_currency_desktops(browser: WebDriver, base_url: str, initial_currency: str, currency_to_select: str):
    desktops_page = DesktopsPage(browser, base_url)
    desktops_page.go_to_desktops_page()
    desktops_page.switch_currency(initial_currency)
    header_currency = desktops_page.get_header_currency()
    sel_currency_before = header_currency.get_selected_currency()
    header_currency.click_currency_form().select_currency(currency_to_select)
    desktops_page.wait_currency_symbol(currency_to_select)
    sel_currency_after = header_currency.get_selected_currency()

    assert sel_currency_before != sel_currency_after
    assert sel_currency_after == currency_to_select