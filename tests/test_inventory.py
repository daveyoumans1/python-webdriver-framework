import pytest
from pages import InventoryPage


@pytest.fixture()
def inventory(authenticated_driver) -> InventoryPage:
    return InventoryPage(authenticated_driver)


def test_inventory_page_loads(inventory):
    assert inventory.is_loaded()
    assert inventory.get_page_title() == "Products"


def test_inventory_shows_six_items(inventory):
    assert inventory.get_item_count() == 6


def test_sort_by_name_ascending(inventory):
    inventory.sort_by("az")
    names = inventory.get_item_names()
    assert names == sorted(names)


def test_sort_by_name_descending(inventory):
    inventory.sort_by("za")
    names = inventory.get_item_names()
    assert names == sorted(names, reverse=True)


def test_sort_by_price_low_to_high(inventory):
    inventory.sort_by("lohi")
    prices = inventory.get_item_prices()
    assert prices == sorted(prices)


def test_sort_by_price_high_to_low(inventory):
    inventory.sort_by("hilo")
    prices = inventory.get_item_prices()
    assert prices == sorted(prices, reverse=True)


def test_add_single_item_updates_cart_badge(inventory):
    inventory.add_item_to_cart(0)
    assert inventory.get_cart_item_count() == 1


def test_add_all_items_updates_cart_badge(inventory):
    inventory.add_all_items_to_cart()
    assert inventory.get_cart_item_count() == 6
