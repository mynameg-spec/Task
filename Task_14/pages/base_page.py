"""
base_page.py
BasePage holds reusable Selenium actions shared by every page object.
All element interactions use Explicit Waits (WebDriverWait + expected_conditions)
and handle Selenium exceptions in one place.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
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
        """Open the given URL in the browser."""
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

    def click_element(self, locator):
        """Wait until the element is clickable and click it."""
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            # Fallback: another element is on top, or the DOM refreshed - click via JavaScript
            element = self.find_visible_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            raise TimeoutException(f"Element not clickable within {self.timeout}s: {locator}")

    def enter_text(self, locator, text):
        """Clear the input field and type the given text."""
        element = self.find_visible_element(locator)
        try:
            element.clear()
            element.send_keys(text)
        except ElementNotInteractableException:
            raise ElementNotInteractableException(f"Cannot type into element: {locator}")

    def get_attribute_value(self, locator, attribute):
        """Return the value of an attribute of a visible element."""
        return self.find_visible_element(locator).get_attribute(attribute)

    def is_element_displayed(self, locator, timeout=None):
        """Return True if the element becomes visible within the timeout, else False."""
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            return wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_enabled(self, locator):
        """Return True if the element is visible and enabled."""
        try:
            return self.find_visible_element(locator).is_enabled()
        except TimeoutException:
            return False

    def wait_for_url_to_not_contain(self, text, timeout=None):
        """Return True if the current URL stops containing the text within the timeout."""
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            return wait.until(lambda driver: text not in driver.current_url)
        except TimeoutException:
            return False

    def wait_for_url_to_contain(self, text, timeout=None):
        """Return True if the current URL contains the text within the timeout."""
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            return wait.until(EC.url_contains(text))
        except TimeoutException:
            return False

    def get_current_url(self):
        """Return the current page URL."""
        return self.driver.current_url
