import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from test_accettazione import utility_test
from test_accettazione.CheckoutTest import CheckoutTestFunctions

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

user_login = "Mario25", "palle9H1"
utility_test.login(driver, user_login)

driver.get("http://127.0.0.1:8000/vetrina/")
product = driver.find_element(By.ID, "Final Fantasy 16")
add_product = product.find_element(By.NAME, "add_product")
add_product.click()

time.sleep(1)

cart_products = CheckoutTestFunctions.get_cart_products(driver)
CheckoutTestFunctions.cancel_order(driver, cart_products)

time.sleep(1)

driver.get("http://127.0.0.1:8000/vetrina/")
product = driver.find_element(By.ID, "Final Fantasy 16")
add_product = product.find_element(By.NAME, "add_product")
add_product.click()


time.sleep(1)

cart_products = CheckoutTestFunctions.get_cart_products(driver)
CheckoutTestFunctions.confirm_order(driver, cart_products)

driver.quit()