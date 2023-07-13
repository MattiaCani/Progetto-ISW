import json
import time

from selenium import webdriver
from types import SimpleNamespace

from test_accettazione.ClientSignUpTest import ClientSignUpTestFunctions

test_data = []

with open('test_accettazione/ClientSignUpTest/ClientSignUpTestData') as user_list:
    for json_user in user_list:
        test_data.append(json.loads(json_user, object_hook=lambda d: SimpleNamespace(**d)))

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/signup/")

time.sleep(1)

for user in test_data:
    if user.test == "reg_success":
        ClientSignUpTestFunctions.reg_success(driver, user)
        driver.delete_all_cookies()
        driver.get("http://127.0.0.1:8000/signup/")
        time.sleep(1)
    elif user.test == "reg_email_failure":
        ClientSignUpTestFunctions.reg_email_failure(driver, user)
        time.sleep(1)
    elif user.test == "reg_username_failure":
        ClientSignUpTestFunctions.reg_username_failure(driver, user)
        time.sleep(1)
    elif user.test == "reg_different_passwords":
        ClientSignUpTestFunctions.reg_different_passwords(driver, user)
        time.sleep(1)
    elif user.test == "reg_problem_password":
        ClientSignUpTestFunctions.reg_problem_password(driver, user)
        time.sleep(1)



driver.quit()
