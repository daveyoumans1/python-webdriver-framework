import os
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from utils.driver_factory import DriverFactory


def pytest_addoption(parser):
    parser.addoption("--browser", default=os.getenv("BROWSER", "chrome"), help="Browser to run tests on")
    parser.addoption("--headless", action="store_true", default=os.getenv("HEADLESS", "false").lower() == "true")


@pytest.fixture(scope="session")
def browser(request) -> str:
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request) -> bool:
    return request.config.getoption("--headless")


@pytest.fixture()
def driver(browser, headless) -> WebDriver:
    drv = DriverFactory.create(browser=browser, headless=headless)
    drv.set_window_size(1920, 1080)
    yield drv
    drv.quit()


@pytest.fixture()
def authenticated_driver(driver):
    """Driver pre-authenticated to Sauce Demo."""
    from pages import LoginPage
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    yield driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("authenticated_driver")
        if driver:
            safe_name = item.nodeid.replace("/", "_").replace("::", "__")
            driver.save_screenshot(f"screenshots/FAIL__{safe_name}.png")
