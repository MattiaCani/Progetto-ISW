from selenium.webdriver.common.by import By


def login(driver, username, password):

    username_field = driver.find_element(By.ID, "id_username")
    password_field = driver.find_element(By.ID, "id_password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "login_button")
    login_button.click()
