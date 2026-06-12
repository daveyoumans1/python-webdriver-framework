from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class InventoryPage(BasePage):
    URL_FRAGMENT = "inventory"

    _TITLE = (By.CLASS_NAME, "title")
    _ITEMS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _ADD_TO_CART_BTNS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def is_loaded(self) -> bool:
        return self.is_visible(self._TITLE)

    def get_page_title(self) -> str:
        return self.get_text(self._TITLE)

    def get_item_count(self) -> int:
        return len(self.find_all(self._ITEMS))

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self._ITEM_NAMES)]

    def get_item_prices(self) -> list[float]:
        return [float(el.text.replace("$", "")) for el in self.find_all(self._ITEM_PRICES)]

    def sort_by(self, option: str) -> None:
        """option values: 'az', 'za', 'lohi', 'hilo'"""
        Select(self.find(self._SORT_DROPDOWN)).select_by_value(option)

    def _scroll_and_click(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.click()

    def add_item_to_cart(self, index: int = 0) -> None:
        buttons = self.wait.until(EC.visibility_of_all_elements_located(self._ADD_TO_CART_BTNS))
        self._scroll_and_click(buttons[index])

    def add_all_items_to_cart(self) -> None:
        count = len(self.wait.until(EC.visibility_of_all_elements_located(self._ADD_TO_CART_BTNS)))
        for _ in range(count):
            btn = self.wait.until(EC.visibility_of_all_elements_located(self._ADD_TO_CART_BTNS))[0]
            self._scroll_and_click(btn)

    def get_cart_item_count(self) -> int:
        if not self.is_visible(self._CART_BADGE, timeout=self.DEFAULT_TIMEOUT):
            return 0
        return int(self.get_text(self._CART_BADGE))

    def go_to_cart(self) -> None:
        self.click(self._CART_LINK)
