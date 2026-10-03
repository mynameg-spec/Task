"""
driver_factory.py
Creates the Chrome WebDriver used by both the script and the pytest tests.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config import HEADLESS


def create_chrome_driver():
    """Return a configured Chrome WebDriver (Selenium Manager downloads the driver)."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver
