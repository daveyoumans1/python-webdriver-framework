from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com"

    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self) -> "LoginPage":
        self.driver.get(self.URL)
        return self

    def login(self, username: str, password: str) -> None:
        self.type(self._USERNAME, username)
        self.type(self._PASSWORD, password)
        self.click(self._LOGIN_BTN)

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MSG)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self._ERROR_MSG)
