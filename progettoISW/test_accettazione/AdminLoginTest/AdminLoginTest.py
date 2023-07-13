import json
import time

from types import SimpleNamespace
from selenium import webdriver

from test_accettazione.AdminLoginTest import AdminLoginTestFunctions

test_data = []

with open('test_accettazione/AdminLoginTest/AdminLoginTestData') as admin_list:
    for json_admin in admin_list:
        test_data.append(json.loads(json_admin, object_hook=lambda d: SimpleNamespace(**d)))

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

time.sleep(1)

for admin in test_data:
    if admin.test == "log_success":
        AdminLoginTestFunctions.a_log_success(driver, admin)
        driver.delete_all_cookies()
        driver.back()
        time.sleep(1)
    elif admin.test == "log_username_failure":
        AdminLoginTestFunctions.a_log_email_failure(driver, admin)
        time.sleep(1)
    elif admin.test == "log_pass_failure":
        AdminLoginTestFunctions.a_log_pass_failure(driver, admin)
        time.sleep(1)

driver.quit()
