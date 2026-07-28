import json
import pytest
from pages import LoginPage, InventoryPage


@pytest.fixture()
def login_page(driver) -> LoginPage:
    return LoginPage(driver).open()


def test_standard_user_can_login(login_page, driver):
    login_page.login("standard_user", "secret_sauce")
    assert InventoryPage(driver).is_loaded()


def test_locked_out_user_sees_error(login_page):
    login_page.login("locked_out_user", "secret_sauce")
    assert login_page.is_error_displayed()
    assert "locked out" in login_page.get_error_message().lower()


def test_invalid_credentials_show_error(login_page):
    login_page.login("invalid_user", "wrong_password")
    assert login_page.is_error_displayed()
    assert "Username and password do not match" in login_page.get_error_message()


@pytest.mark.parametrize("username,password", [
    ("", "secret_sauce"),
    ("standard_user", ""),
    ("", ""),
])
def test_empty_credentials_show_error(login_page, username, password):
    login_page.login(username, password)
    assert login_page.is_error_displayed()


def test_login_page_url(login_page, driver):
    assert driver.current_url == LoginPage.URL + "/"


def test_username_case_sensitivity(login_page):
    login_page.login("STANDARD_USER", "secret_sauce")
    assert login_page.is_error_displayed()
    assert "Username and password do not match" in login_page.get_error_message()


def test_password_case_sensitivity(login_page):
    login_page.login("standard_user", "SECRET_SAUCE")
    assert login_page.is_error_displayed()
    assert "Username and password do not match" in login_page.get_error_message()
