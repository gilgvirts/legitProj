from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, \
    TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://main.d2t1pk7fjag8u6.amplifyapp.com/"
INPUT_FIELD = "//input[@{}='{}']"
CREDS = {"username": "gilgvirts@gmail.com", "password": "123456gG!"}


def set_driver():
    """Set up Chrome WebDriver"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def keys_to_input(driver, input_id, keys, attribute="name"):
    """Find input field by attribute and input text."""
    fields = driver.find_elements(By.XPATH, INPUT_FIELD.format(attribute, input_id))
    if len(fields) > 0:
        fields[0].send_keys(keys)
    else:
        raise Exception(f"Couldn't find field {input_id}")


def find_and_click(driver: webdriver, locator: str, by: By = By.XPATH):
    """Find element and click on it."""
    try:
        btn = driver.find_element(by, locator)
        btn.click()
    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException):
        print(f"Failed finding or clicking {locator}")
        exit(1)


def find_and_click_btn(driver: webdriver, btn_text: str):
    find_and_click(driver, f"//button[contains(text(),'{btn_text}')]")


def find_and_click_link(driver: webdriver, link_txt: str):
    find_and_click(driver, by=By.LINK_TEXT, locator=link_txt)


def sign_in(driver: webdriver):
    """Sign in to the website using provided credentials."""
    for cred in CREDS.keys():
        keys_to_input(driver, cred, CREDS[cred])
    find_and_click(driver, "//button[contains(text(),'Sign in')]")


def add_product(product):
    """Add a product to the cart."""
    product_text = product.text.split("\n")[0]
    try:
        btn = product.find_element(By.XPATH, "*[contains(text(), 'Add to Cart')]")
        btn.click()
        return product_text
    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException):
        print(f"Failed to add {product_text} to cart")
        return None


def add_products(driver: webdriver, num_of_products_to_add: int):
    """Add specified number of products to the cart."""
    products_bought = []
    products = driver.find_elements(By.XPATH, "//li[contains(text(), 'Product')]")
    for product in products[:num_of_products_to_add]:
        product_name = add_product(product)
        if product_name:
            products_bought.append(product_name)
    return products_bought


def verify_shopping_page(driver: webdriver):
    """Verify shopping page loaded"""
    header = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'Online Shopping Website')]")))
    if header:
        return True
    else:
        raise Exception("Couldn't load shopping page in given time")


def go_to_cart(driver: webdriver):
    """Try and get directly to cart page - bug found :)"""
    driver.get(URL + "/cart")


def verify_cart(driver: webdriver, products_added: list):
    """Verify products in the cart."""
    products = driver.find_elements(By.XPATH, "//li[contains(text(), 'Product')]")
    if len(products) != len(products_added):
        print(f"Found in cart {len(products)} while {len(products_added)} were placed")
    products_in_cart = [product.text.split("(")[0].strip() for product in products]
    if products_added != products_in_cart:
        print("Products were not added properly to cart")


def go_to_checkout(driver: webdriver):
    driver.get(URL + "/checkout")


def click_checkout(driver: webdriver):
    """Complete the checkout process."""
    find_and_click_link(driver, "Checkout")


def click_cart(driver: webdriver):
    """Navigate to the cart page."""
    find_and_click_link(driver, "Shopping Cart")


def complete_checkout(driver: webdriver):
    """Submit checkout ad verify."""
    find_and_click_btn(driver, "Complete Checkout")
    verify_order(driver)


def enter_shipping_address(driver: webdriver):
    """Enter shipping address during checkout."""
    keys_to_input(driver, "shipping-address-text", "My shipping address", "id")


def verify_order(driver: webdriver):
    """Verify order confirmation."""
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       "No checkout confirmation")
        alert = driver.switch_to.alert
        text_appeared = alert.text
        if "checkout complete" not in text_appeared:
            print(f"Failed placing order. Received confirmation: {text_appeared}")
        alert.accept()
    except TimeoutException:
        print("Checkout confirmation wasn't presented")


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


if __name__ == '__main__':
    test_online_shopping(2)
