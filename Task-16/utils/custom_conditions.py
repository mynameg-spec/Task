"""
custom_conditions.py
Custom Expected Condition used with WebDriverWait.
It lets us wait for the live counter to update without using sleep().
"""
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


class text_to_change_from:
    """
    Expected Condition: wait until the element's text is different from old_text.
    Returns the new text when it changes, otherwise False (so WebDriverWait keeps polling).
    """

    def __init__(self, locator, old_text):
        self.locator = locator
        self.old_text = old_text

    def __call__(self, driver):
        try:
            new_text = driver.find_element(*self.locator).text.strip()
        except (NoSuchElementException, StaleElementReferenceException):
            return False  # Element is re-rendering, try again on the next poll
        return new_text if new_text and new_text != self.old_text else False
