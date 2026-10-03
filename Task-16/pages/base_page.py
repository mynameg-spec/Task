"""
base_page.py
BasePage holds common Selenium actions shared by all page objects.
All waits are Explicit Waits using Expected Conditions - no sleep() is used.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from utils.config import PAGE_LOAD_WAIT


class BasePage:
    """Parent class for all page objects."""

    def __init__(self, driver, timeout=PAGE_LOAD_WAIT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open_url(self, url):
        """Open the given URL."""
        try:
            self.driver.get(url)
        except WebDriverException as error:
            raise WebDriverException(f"Unable to open URL '{url}': {error.msg}")

    def find_visible_element(self, locator):
        """Wait until the element is visible and return it."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not visible within {self.timeout}s: {locator}")

    def get_element_text(self, locator):
        """Return the visible text of an element."""
        return self.find_visible_element(locator).text.strip()

    def is_element_visible(self, locator):
        """Return True if the element becomes visible, otherwise False."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_page_title(self):
        """Return the browser tab title."""
        return self.driver.title
