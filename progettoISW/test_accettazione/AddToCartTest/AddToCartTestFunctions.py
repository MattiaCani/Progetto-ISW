import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from test_accettazione.CheckoutTest import CheckoutTestFunctions


def add_new_product(self, driver, product_name, quantita):
    product = driver.find_element(By.ID, product_name)

    select_quantita = Select(product.find_element(By.ID, "id_quantita_acquisto"))
    select_quantita.select_by_value(quantita)

    add_button = product.find_element(By.NAME, "add_product")
    add_button.click()

    time.sleep(1)

    product = driver.find_element(By.ID, product_name)
    add_button = product.find_element(By.NAME, "add_product")

    assert driver.title == "Vetrina"
    assert not add_button.is_enabled()

    check_cart(driver)

    time.sleep(1)

    product = driver.find_element(By.ID, product_name)

    select_quantita = Select(product.find_element(By.ID, "id_quantita_acquisto"))
    quantita_aggiunta = select_quantita.first_selected_option.text

    assert product is not None
    assert quantita_aggiunta == quantita

    driver.get(f"{self.live_server_url}/vetrina/")


def add_product(driver, product_name):
    product = driver.find_element(By.ID, product_name)

    add_button = product.find_element(By.NAME, "add_product")

    assert driver.title == "Vetrina"
    assert not add_button.is_enabled()


def check_cart(driver):
    cart_button = driver.find_element(By.ID, "cart_button")
    cart_button.click()

    assert driver.title == "Carrello"


def remove_product(self, driver, product_name):
    check_cart(driver)

    old_cart = CheckoutTestFunctions.get_cart_products(self, driver)

    product = driver.find_element(By.ID, product_name)
    remove_button = product.find_element(By.LINK_TEXT, "Rimuovi")

    remove_button.click()

    new_cart = CheckoutTestFunctions.get_cart_products(self, driver)
    modified_old_cart = [product for product in old_cart if product.get("Nome") != product_name]

    assert modified_old_cart == new_cart
    assert driver.title == "Carrello"


def change_quantity(self, driver, product_name, nuova_quantita):
    check_cart(driver)

    product = driver.find_element(By.ID, product_name)
    select_quantita = Select(product.find_element(By.ID, "id_quantita_acquisto"))

    vecchia_quantita = select_quantita.first_selected_option.text
    vecchio_prezzo = product.find_element(By.CLASS_NAME, "cart_prezzo").text.split("€")[0]

    prezzo_al_pezzo = float(vecchio_prezzo)/float(vecchia_quantita)

    select_quantita.select_by_value(nuova_quantita)

    product = driver.find_element(By.ID, product_name)
    nuovo_prezzo = product.find_element(By.CLASS_NAME, "cart_prezzo").text.split("€")[0]

    assert prezzo_al_pezzo * float(nuova_quantita) == float(nuovo_prezzo)
    assert driver.title == "Carrello"

    driver.get(f"{self.live_server_url}/vetrina/")
