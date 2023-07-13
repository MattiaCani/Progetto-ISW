import time

from selenium.webdriver.common.by import By


def get_products(driver):
    products = driver.find_elements(By.CLASS_NAME, "admin_product")

    list_products = []

    for product in products:
        nome = product.find_element(By.CLASS_NAME, "admin_product_nome").text
        tipologia = product.find_element(By.CLASS_NAME, "admin_product_tipologia").text
        descrizione = product.find_element(By.CLASS_NAME, "admin_product_descrizione").text
        prezzo = product.find_element(By.CLASS_NAME, "admin_product_prezzo").text
        disponibilita = product.find_element(By.CLASS_NAME, "admin_product_disponibilita").text

        new_product = {"nome": nome, "tipologia": tipologia, "descrizione": descrizione,
                       "prezzo": float(prezzo.replace('€', '')), "disponibilita": float(disponibilita)}

        list_products.append(new_product)

    return list_products


def insert_product(driver, prodotto):
    insert_button = driver.find_element(By.ID, "insert_button")
    insert_button.click()

    time.sleep(1)

    field_nome = driver.find_element(By.ID, "id_nome")
    field_nome.send_keys(prodotto.nome)

    field_codice_seriale = driver.find_element(By.ID, "id_codice_seriale")
    field_codice_seriale.send_keys(prodotto.codice_seriale)

    field_tipologia = driver.find_element(By.ID, "id_tipologia")
    field_tipologia.send_keys(prodotto.tipologia)

    field_descrizione = driver.find_element(By.ID, "id_descrizione")
    field_descrizione.send_keys(prodotto.descrizione)

    field_prezzo = driver.find_element(By.ID, "id_prezzo")
    field_prezzo.send_keys(prodotto.prezzo)

    field_disponibilita = driver.find_element(By.ID, "id_disponibilita")
    field_disponibilita.send_keys(prodotto.disponibilita)

    insert_new_button = driver.find_element(By.ID, "add_new_product")
    insert_new_button.click()


def remove_product(driver, nome_prodotto):
    product = driver.find_element(By.ID, nome_prodotto)

    remove_button = product.find_element(By.LINK_TEXT, "Rimuovi prodotto")
    remove_button.click()


def modify_product(driver, nome_prodotto, cambio_valore_prezzo):
    product = driver.find_element(By.ID, nome_prodotto)

    modify_button = product.find_element(By.LINK_TEXT, "Modifica prodotto")
    modify_button.click()

    field_prezzo = driver.find_element(By.ID, "id_prezzo")
    field_prezzo.clear()
    field_prezzo.send_keys(cambio_valore_prezzo)

    modify_button = driver.find_element(By.ID, "modify_button")
    modify_button.click()


def insert_product_success(driver, prodotto):
    user_before = driver.get_cookie("sessionid")
    old_products = get_products(driver)

    insert_product(driver, prodotto)

    user_after = driver.get_cookie("sessionid")
    title = driver.title

    new_products = get_products(driver)
    old_products.append({"nome": prodotto.nome, "tipologia": prodotto.tipologia, "descrizione": prodotto.descrizione,
                         "prezzo": prodotto.prezzo, "disponibilita": prodotto.disponibilita})

    assert len(old_products) == len(new_products) and all(d in new_products for d in old_products) and all(
        d in old_products for d in new_products)
    assert title == "Vetrina Amministratore"
    assert user_before == user_after


def insert_product_failure(driver, prodotto):
    user_before = driver.get_cookie("sessionid")
    old_products = get_products(driver)

    insert_product(driver, prodotto)

    user_after = driver.get_cookie("sessionid")
    title = driver.title

    error_message = driver.find_element(By.CLASS_NAME, "errorlist")

    driver.get("http://127.0.0.1:8000/vetrina_amministratore")
    new_products = get_products(driver)

    assert error_message is not None
    assert old_products == new_products
    assert title == "Aggiungi Prodotto"
    assert user_before == user_after


def remove_product_success(driver, prodotto):
    user_before = driver.get_cookie("sessionid")
    old_products = get_products(driver)

    remove_product(driver, prodotto.nome)

    user_after = driver.get_cookie("sessionid")
    title = driver.title

    new_products = get_products(driver)
    removed_old_products = [d for d in old_products if d.get('nome') != prodotto.nome]

    assert len(removed_old_products) == len(new_products) and all(d in new_products for d in removed_old_products) and all(
        d in removed_old_products for d in new_products)
    assert title == "Vetrina Amministratore"
    assert user_before == user_after


def modify_product_success(driver, prodotto, cambio_prezzo):
    user_before = driver.get_cookie("sessionid")
    old_products = get_products(driver)

    modify_product(driver, prodotto.nome, cambio_prezzo)

    user_after = driver.get_cookie("sessionid")
    title = driver.title

    new_products = get_products(driver)
    modifyed_old_products = [{**d, 'prezzo': cambio_prezzo} if d.get('nome') == prodotto.nome else d for d in old_products]

    assert all(d in new_products for d in modifyed_old_products) and all(d in modifyed_old_products for d in new_products)
    assert title == "Vetrina Amministratore"
    assert user_before == user_after


def modify_product_failure(driver, prodotto, cambio_prezzo):
    user_before = driver.get_cookie("sessionid")
    old_products = get_products(driver)

    modify_product(driver, prodotto.nome, cambio_prezzo)

    user_after = driver.get_cookie("sessionid")
    title = driver.title

    error_message = driver.find_element(By.CLASS_NAME, "errorlist")

    driver.get("http://127.0.0.1:8000/vetrina_amministratore")
    new_products = get_products(driver)

    assert old_products == new_products
    assert error_message is not None
    assert title == "Modifica Prodotto"
    assert user_before == user_after
