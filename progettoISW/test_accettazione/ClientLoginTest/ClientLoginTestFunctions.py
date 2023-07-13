import time

from selenium.webdriver.common.by import By


def log(driver, user):
    username_field = driver.find_element(By.ID, "id_username")
    username_field.clear()
    username_field.send_keys(user.username)

    password_field = driver.find_element(By.ID, "id_password")
    password_field.send_keys(user.password)

    send_form = driver.find_element(By.ID, "login_button")
    send_form.click()

    time.sleep(1)


def log_success(driver, user):
    log(driver, user)

    title = driver.title
    logged_user = driver.find_element(By.ID, "logged_user")

    cookie = driver.get_cookie("sessionid")

    assert cookie is not None
    assert logged_user.text == user.username
    assert title == "Vetrina"


def log_failure(driver, user, string_error):
    log(driver, user)

    username_field = driver.find_element(By.ID, "id_username")
    password_field = driver.find_element(By.ID, "id_password")

    username_field.clear()
    password_field.clear()

    title = driver.title

    cookie = driver.get_cookie("sessionid")

    assert cookie is None
    assert string_error in driver.page_source
    assert title == "Login"


def log_username_failure(driver, user):
    log_failure(driver, user, "Login fallito")


def log_pass_failure(driver, user):
    log_failure(driver, user, "Login fallito")
