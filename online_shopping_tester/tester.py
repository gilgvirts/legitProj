from online_shopping_tester.infra import *


def test_online_shopping(num_of_test_products: int):
    """Test online shopping process."""
    driver = set_driver()
    driver.get(URL)
    sign_in(driver)
    sleep(2)  # Adding a delay for the page to load completely
    verify_shopping_page(driver)
    bought = add_products(driver, num_of_test_products)
    click_cart(driver)
    verify_cart(driver, bought)
    click_checkout(driver)
    enter_shipping_address(driver)
    complete_checkout(driver)
    driver.quit()


def bug_catch(num_of_test_products: int):
    """There is a bug where if you move directly
    to /cart wothout clicking tab, cart is empty.
    this test verifies it"""
    driver = set_driver()
    driver.get(URL)
    sign_in(driver)
    sleep(2)  # Adding a delay for the page to load completely
    verify_shopping_page(driver)
    bought = add_products(driver, num_of_test_products)
    go_to_cart(driver)
    verify_cart(driver, bought)
    click_checkout(driver)
    enter_shipping_address(driver)
    complete_checkout(driver)
    driver.quit()