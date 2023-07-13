import json
import time
from types import SimpleNamespace

from selenium import webdriver

from test_accettazione import utility_test
from test_accettazione.ProductsTest import ProductsTestFunctions

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

test_data = []

with open('test_accettazione/CheckoutTest/CheckoutTestData') as user_list:
    for json_user in user_list:
        test_data.append(json.loads(json_user, object_hook=lambda d: SimpleNamespace(**d)))

user_login = "admin", "admin"
utility_test.login(driver, user_login)

time.sleep(1)

ProductsTestFunctions.insert_product_success(driver, test_data[0])
ProductsTestFunctions.insert_product_failure(driver, test_data[1])

ProductsTestFunctions.modify_product_failure(driver, test_data[0], -50)
ProductsTestFunctions.modify_product_success(driver, test_data[0], 6565984)

ProductsTestFunctions.remove_product_success(driver, test_data[0])

driver.quit()