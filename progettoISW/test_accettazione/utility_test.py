from selenium.webdriver.common.by import By


def login(driver, user):

    username_field = driver.find_element(By.ID, "id_username")
    password_field = driver.find_element(By.ID, "id_password")

    username_field.send_keys(user[0])
    password_field.send_keys(user[1])

    login_button = driver.find_element(By.ID, "login_button")
    login_button.click()
