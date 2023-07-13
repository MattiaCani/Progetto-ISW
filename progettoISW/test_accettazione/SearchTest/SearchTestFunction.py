import time
from selenium.webdriver.common.by import By
from test_accettazione.FilterTest.FilterTestFunctions import get_products


def search(driver, testo_ricerca):
    old_products = get_products(driver)

    search_box = driver.find_element(By.NAME, "search_query")
    search_box.clear()

    search_button = driver.find_element(By.ID, "search_button")

    search_box.send_keys(testo_ricerca)
    search_button.click()

    time.sleep(1)

    new_products = get_products(driver)

    return old_products, new_products


def search_success(driver, testo_ricerca):
    old_products, new_products = search(driver, testo_ricerca)
    old_products_filtered = [product for product in old_products if testo_ricerca.capitalize() in product["Nome"]]

    assert old_products_filtered == new_products
    assert len(new_products) > 0


def search_failure(driver, testo_ricerca):
    old_products, new_products = search(driver, testo_ricerca)
    old_products_filtered = [product for product in old_products if testo_ricerca.capitalize() in product["Nome"]]

    assert old_products_filtered == new_products
    assert len(new_products) == 0

