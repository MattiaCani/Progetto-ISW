import time

from selenium.webdriver.common.by import By
from test_accettazione import utility_test


def get_field(driver, field_name):
    field = driver.find_element(By.ID, field_name)
    field.clear()

    return field


def reg(driver, user):
    get_field(driver, "id_username").send_keys(user.username)
    get_field(driver, "id_email").send_keys(user.email)
    get_field(driver, "id_first_name").send_keys(user.first_name)
    get_field(driver, "id_last_name").send_keys(user.last_name)
    get_field(driver, "id_password1").send_keys(user.password1)
    get_field(driver, "id_password2").send_keys(user.password2)

    send_form = driver.find_element(By.ID, "signup_button")
    send_form.click()

    time.sleep(1)


def reg_success(driver, user):
    reg(driver, user)

    title = driver.title

    assert title == "Login"

    time.sleep(2)

    user_credential = "" + user.username, "" + user.password1
    utility_test.login(driver, user_credential)

    title = driver.title
    logged_user = driver.find_element(By.ID, "logged_user")
    cookie = driver.get_cookie("sessionid")

    assert cookie is not None
    assert logged_user.text == user.username
    assert title == "Vetrina"


def reg_failure(driver, user, error_message):
    reg(driver, user)

    title = driver.title
    cookie = driver.get_cookie("sessionid")

    assert cookie is None
    assert error_message in driver.page_source
    assert title == "Registrazione"


def reg_email_failure(driver, user):
    reg_failure(driver, user, "Enter a valid email address.")


def reg_username_failure(driver, user):
    reg_failure(driver, user, "A user with that username already exists.")


def reg_different_passwords(driver, user):
    reg_failure(driver, user, "The two password fields didn’t match.")


def reg_problem_password(driver, user):
    reg_failure(driver, user, "This password is too short. It must contain at least 8 characters.")

