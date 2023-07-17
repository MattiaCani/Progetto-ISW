from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def get_cart_products(self, driver):
    driver.get(f"{self.live_server_url}/carrello/")
    products = driver.find_elements(By.CLASS_NAME, "cart_product")

    list_products = []

    for product in products:
        nome = product.find_element(By.CLASS_NAME, "cart_nome").text

        new_product = {"Nome": nome}
        list_products.append(new_product)

    return list_products


def compile_order(driver):
    field_indirizzo = driver.find_element(By.ID, "id_indirizzo_spedizione")
    field_numero_carta = driver.find_element(By.ID, "id_numero_carta")
    field_intestatario = driver.find_element(By.ID, "id_intestatario")
    select_metodo = driver.find_element(By.ID, "id_nome_metodo")

    field_indirizzo.send_keys("Indirizzo di prova")
    field_numero_carta.send_keys("123456789")
    field_intestatario.send_keys("Intestatario di prova")

    select = Select(select_metodo)
    select.select_by_visible_text("Debito")


def confirm_order(self, driver, carrello):
    driver.get(f"{self.live_server_url}/ordine/")
    current_logged_user = driver.get_cookie("sessionid")

    compile_order(driver)

    order_button = driver.find_element(By.ID, "order_button")
    order_button.click()

    title = driver.title
    logged_user = driver.get_cookie("sessionid")

    assert title == "Vetrina"
    assert current_logged_user == logged_user

    driver.get(f"{self.live_server_url}/carrello/")
    nuovo_carrello = get_cart_products(self, driver)

    assert carrello != nuovo_carrello
    assert len(nuovo_carrello) == 0


def cancel_order(self, driver, carrello):
    driver.get(f"{self.live_server_url}/ordine/")
    current_logged_user = driver.get_cookie("sessionid")

    compile_order(driver)

    return_button = driver.find_element(By.CLASS_NAME, "fakeButton")
    return_button.click()

    title = driver.title
    logged_user = driver.get_cookie("sessionid")

    assert title == "Carrello"
    assert current_logged_user == logged_user

    driver.get(f"{self.live_server_url}/carrello/")
    nuovo_carrello = get_cart_products(self, driver)

    assert carrello == nuovo_carrello
    assert len(nuovo_carrello) > 0



