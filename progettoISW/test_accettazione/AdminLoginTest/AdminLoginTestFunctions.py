from test_accettazione.ClientLoginTest import ClientLoginTestFunctions
from selenium.webdriver.common.by import By


def a_log_success(driver, admin):
    ClientLoginTestFunctions.log(driver, admin)

    title = driver.title
    logged_user = driver.find_element(By.ID, "logged_user")

    cookie = driver.get_cookie("sessionid")

    assert cookie is not None
    assert logged_user.text == admin.username
    assert title == "Vetrina Amministratore"


def a_log_email_failure(driver, admin):
    ClientLoginTestFunctions.log_failure(driver, admin, "Login fallito")


def a_log_pass_failure(driver, admin):
    ClientLoginTestFunctions.log_failure(driver, admin, "Login fallito")
