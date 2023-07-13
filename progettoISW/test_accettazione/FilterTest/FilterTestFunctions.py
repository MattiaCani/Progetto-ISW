import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def get_products(driver):
    products = driver.find_elements(By.CLASS_NAME, "shop_product")

    list_products = []

    for product in products:
        nome = product.find_element(By.CLASS_NAME, "shop_nome").text
        tipologia = product.find_element(By.CLASS_NAME, "shop_tipologia").text
        prezzo = product.find_element(By.CLASS_NAME, "shop_prezzo").text

        new_product = {"Nome": nome, "Tipologia": tipologia, "Prezzo": float(prezzo.replace('€', ''))}
        list_products.append(new_product)

    return list_products


def select_filtering(driver, filter_type, valore):
    old_products = get_products(driver)

    chosen_filter = driver.find_element(By.NAME, filter_type)
    select = Select(chosen_filter)
    select.select_by_visible_text(valore)

    time.sleep(1)

    form = driver.find_element(By.NAME, "form_filtri")
    filter_button = form.find_element(By.XPATH, "//button[@id='filter_button']")
    filter_button.click()

    time.sleep(1)

    new_products = get_products(driver)

    return old_products, new_products


def number_filtering(driver, filter_type, valore):
    old_products = get_products(driver)

    chosen_filter = driver.find_element(By.NAME, filter_type)

    if valore == "":
        chosen_filter.clear()
    else:
        chosen_filter.send_keys(valore)

    time.sleep(1)

    form = driver.find_element(By.NAME, "form_filtri")
    filter_button = form.find_element(By.XPATH, "//button[@id='filter_button']")
    filter_button.click()

    time.sleep(1)

    new_products = get_products(driver)

    return old_products, new_products


def add_filter(driver, filter_type, valore):
    if filter_type == 'tipologia':
        old_products, new_products = select_filtering(driver, filter_type, valore)

        old_products_filtered = [product for product in old_products if product["Tipologia"] == valore]
        assert old_products_filtered == new_products

    elif filter_type == 'disponibilita':
        select_filtering(driver, filter_type, valore)

    elif filter_type == 'prezzo_min':
        old_products, new_products = number_filtering(driver, filter_type, valore)

        old_products_filtered = [product for product in old_products if product["Prezzo"] >= valore]
        assert old_products_filtered == new_products

    elif filter_type == 'prezzo_max':
        old_products, new_products = number_filtering(driver, filter_type, valore)

        old_products_filtered = [product for product in old_products if product["Prezzo"] <= valore]
        assert old_products_filtered == new_products


def remove_filter(driver, filter_type):
    if filter_type == 'tipologia':
        vecchio_filtro = Select(driver.find_element(By.NAME, "tipologia")).first_selected_option.text
        old_products, new_products = select_filtering(driver, filter_type, "Tutte le tipologie")

        new_products_filtered = [product for product in new_products if product["Tipologia"] == vecchio_filtro]
        assert old_products == new_products_filtered

    elif filter_type == 'disponibilita':
        select_filtering(driver, filter_type, "Qualsiasi disponibilità")

    elif filter_type == 'prezzo_min':
        vecchio_filtro = driver.find_element(By.NAME, "prezzo_min").get_attribute("value")
        old_products, new_products = number_filtering(driver, filter_type, "")

        new_products_filtered = [product for product in new_products if product["Prezzo"] >= float(vecchio_filtro)]
        assert old_products == new_products_filtered

    elif filter_type == 'prezzo_max':
        vecchio_filtro = driver.find_element(By.NAME, "prezzo_max").get_attribute("value")
        old_products, new_products = number_filtering(driver, filter_type, "")

        new_products_filtered = [product for product in new_products if product["Prezzo"] <= float(vecchio_filtro)]
        assert old_products == new_products_filtered


def remove_all_filter(driver, original_products):
    driver.find_element(By.LINK_TEXT, "Azzeramento filtri").click()
    unfiltered_products = get_products(driver)

    tipologia_filter = driver.find_element(By.NAME, "tipologia")
    disponibilita_filter = driver.find_element(By.NAME, "disponibilita")
    prezzo_min_filter = driver.find_element(By.NAME, "prezzo_min")
    prezzo_max_filter = driver.find_element(By.NAME, "prezzo_max")

    assert original_products == unfiltered_products
    assert Select(tipologia_filter).first_selected_option.text == "Tutte le tipologie"
    assert Select(disponibilita_filter).first_selected_option.text == "Qualsiasi disponibilità"
    assert prezzo_min_filter.get_attribute("value") == ""
    assert prezzo_max_filter.get_attribute("value") == ""


