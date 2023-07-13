import time
from selenium import webdriver
from test_accettazione import utility_test
from test_accettazione.LogoutTest import LogoutTestFunctions

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

client_credentials = "Luigi88", "pavimento9H1"
admin_credentials = "admin", "admin"

credentials = [client_credentials, admin_credentials]

for user in credentials:

    utility_test.login(driver, user)

    time.sleep(1)

    LogoutTestFunctions.logout(driver)

    time.sleep(1)

driver.quit()
