from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Upgrade 6 | Page Object Pattern - reusable page class
class LoginPage:
    URL = "https://myoppd.com"

    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self):
        self.driver.get(self.URL)

    # handles waits and locators
    def is_loaded(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        self.scroll_into_view(element)
        return element.is_displayed()

    # Upgrade 5: handles scrolling
    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )