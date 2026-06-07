import os
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class BasePage:
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 10))

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator: tuple) -> List[WebElement]:
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple) -> None:
        self.find_clickable(locator).click()

    def type(self, locator: tuple, text: str) -> None:
        el = self.find_clickable(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text

    def is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url(self, url_fragment: str) -> None:
        self.wait.until(EC.url_contains(url_fragment))

    def take_screenshot(self, name: str) -> None:
        os.makedirs("screenshots", exist_ok=True)
        self.driver.save_screenshot(f"screenshots/{name}.png")
