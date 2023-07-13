import time
from selenium import webdriver

from test_accettazione import utility_test
from test_accettazione.SearchTest import SearchTestFunction

driver = webdriver.Edge()
driver.get("http://127.0.0.1:8000/")

user_login = "Mario25", "palle9H1"
utility_test.login(driver, user_login)


time.sleep(1)

SearchTestFunction.search_success(driver, "final")
SearchTestFunction.search_failure(driver, "asdfasdfas")


time.sleep(1)


driver.quit()