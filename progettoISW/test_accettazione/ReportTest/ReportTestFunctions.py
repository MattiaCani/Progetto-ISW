import time

from selenium.webdriver.common.by import By

from test_accettazione.FilterTest import FilterTestFunctions


def open_report(driver):
    driver.get("http://127.0.0.1:8000/vetrina_amministratore")

    report_button = driver.find_element(By.ID, "resoconto")
    report_button.click()

    time.sleep(1)

    assert driver.title == "Resoconto Vendite"


def add_report_filter(driver, filter_type, valore):
    FilterTestFunctions.add_filter(driver, filter_type, valore)


def remove_report_filter(driver, filter_type):
    FilterTestFunctions.remove_filter(driver, filter_type)


def remove_all_report_filters(driver, original_products):
    FilterTestFunctions.remove_all_filter(driver, original_products)