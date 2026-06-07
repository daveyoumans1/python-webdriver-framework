import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverFactory:
    _SUPPORTED = ("chrome", "firefox", "edge")

    @staticmethod
    def create(browser: str = "chrome", headless: bool = False) -> webdriver.Remote:
        browser = browser.lower()
        if browser not in DriverFactory._SUPPORTED:
            raise ValueError(f"Unsupported browser '{browser}'. Choose from {DriverFactory._SUPPORTED}")

        if browser == "chrome":
            return DriverFactory._chrome(headless)
        if browser == "firefox":
            return DriverFactory._firefox(headless)
        return DriverFactory._edge(headless)

    @staticmethod
    def _chrome(headless: bool) -> webdriver.Chrome:
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1920,1080")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)

    @staticmethod
    def _firefox(headless: bool) -> webdriver.Firefox:
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("--headless")
        return webdriver.Firefox(service=webdriver.firefox.service.Service(GeckoDriverManager().install()), options=opts)

    @staticmethod
    def _edge(headless: bool) -> webdriver.Edge:
        opts = EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
        return webdriver.Edge(service=webdriver.edge.service.Service(EdgeChromiumDriverManager().install()), options=opts)
