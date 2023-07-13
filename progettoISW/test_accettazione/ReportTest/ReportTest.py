import time
from selenium import webdriver
from test_accettazione import utility_test
from test_accettazione.FilterTest import FilterTestFunctions
from test_accettazione.ReportTest import ReportTestFunctions

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

user_login = "admin", "admin"
utility_test.login(driver, user_login)

time.sleep(1)

ReportTestFunctions.open_report(driver)

time.sleep(1)

original_products = FilterTestFunctions.get_products(driver)

FilterTestFunctions.add_filter(driver, "tipologia", "Videogioco")
FilterTestFunctions.remove_filter(driver, "tipologia")

FilterTestFunctions.add_filter(driver, "disponibilita", "Disponibile")
FilterTestFunctions.remove_filter(driver, "disponibilita")

FilterTestFunctions.add_filter(driver, "prezzo_min", 20)
FilterTestFunctions.remove_filter(driver, "prezzo_min")

FilterTestFunctions.add_filter(driver, "prezzo_max", 60)
FilterTestFunctions.remove_filter(driver, "prezzo_max")

FilterTestFunctions.remove_all_filter(driver, original_products)

driver.quit()

