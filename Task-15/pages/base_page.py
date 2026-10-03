"""
base_page.py
BasePage contains common Selenium actions used by all page objects.
Every action uses Explicit Wait with Expected Conditions - no sleep() is used.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    WebDriverException,
)

from utils.config import EXPLICIT_WAIT


class BasePage:
    """Parent class for all page objects."""

    def __init__(self, driver, timeout=EXPLICIT_WAIT):
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
        """Wait for the element to be visible and return it."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not visible within {self.timeout}s: {locator}")

    def click_element(self, locator):
        """Wait for the element to be clickable and click it."""
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except ElementClickInterceptedException:
            element = self.find_visible_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            raise TimeoutException(f"Element not clickable within {self.timeout}s: {locator}")

    def enter_text(self, locator, text):
        """Clear the field and type the text."""
        element = self.find_visible_element(locator)
        try:
            element.clear()
            element.send_keys(text)
        except ElementNotInteractableException:
            raise ElementNotInteractableException(f"Cannot type into element: {locator}")

    def is_element_visible(self, locator):
        """Return True if the element becomes visible, otherwise False."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
