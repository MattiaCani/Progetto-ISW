from selenium.webdriver.common.by import By


def logout(driver):
    logout_button = driver.find_element(By.ID, "logout_button")
    logout_button.click()

    cookie = driver.get_cookie("sessionid")

    assert cookie is None
    assert driver.title == "Login"
