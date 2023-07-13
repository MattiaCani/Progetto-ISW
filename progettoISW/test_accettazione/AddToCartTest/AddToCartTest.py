import time
from selenium import webdriver

from test_accettazione import utility_test
from test_accettazione.AddToCartTest import AddToCartTestFunctions

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

user_login = "Mario25", "palle9H1"
utility_test.login(driver, user_login)

time.sleep(1)

AddToCartTestFunctions.add_new_product(driver, "Final Fantasy 16", "5")

time.sleep(1)

AddToCartTestFunctions.change_quantity(driver, "Final Fantasy 16", "9")

time.sleep(1)

AddToCartTestFunctions.add_product(driver, "Final Fantasy 16")

time.sleep(1)

AddToCartTestFunctions.remove_product(driver, "Final Fantasy 16")

driver.quit()
