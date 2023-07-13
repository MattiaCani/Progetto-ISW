import json
import time

from selenium import webdriver
import ClientLoginTestFunctions
from types import SimpleNamespace


test_data = []

with open('test_accettazione/ClientLoginTest/ClientLoginTestData') as user_list:
    for json_user in user_list:
        test_data.append(json.loads(json_user, object_hook=lambda d: SimpleNamespace(**d)))

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

time.sleep(1)

for user in test_data:
    if user.test == "log_success":
        ClientLoginTestFunctions.log_success(driver, user)
        driver.delete_all_cookies()
        driver.back()
        time.sleep(1)
    elif user.test == "log_username_failure":
        ClientLoginTestFunctions.log_username_failure(driver, user)
        time.sleep(1)
    elif user.test == "log_pass_failure":
        ClientLoginTestFunctions.log_pass_failure(driver, user)
        time.sleep(1)

driver.quit()
