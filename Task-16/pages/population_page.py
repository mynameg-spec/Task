"""
population_page.py
Page Object for the World Population Clock Live page.
Only XPATH locators are used, as required by the task.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.config import BASE_URL, COUNTER_CHANGE_WAIT
from utils.custom_conditions import text_to_change_from


class PopulationPage(BasePage):
    """Page object representing the World Population Clock page."""

    # ---------- Locators (XPATH only) ----------
    POPULATION_TITLE = (By.XPATH, "//h1[normalize-space()='World population']")
    POPULATION_COUNTER = (
        By.XPATH,
        "//h1[normalize-space()='World population']"
        "/preceding-sibling::div[contains(@class,'counter-ticker')]",
    )

    # ---------- Actions ----------
    def load(self):
        """Open the page and wait until the population counter is visible."""
        self.open_url(BASE_URL)
        self.find_visible_element(self.POPULATION_COUNTER)

    def is_population_counter_displayed(self):
        return self.is_element_visible(self.POPULATION_COUNTER)

    def is_population_title_displayed(self):
        return self.is_element_visible(self.POPULATION_TITLE)

    def get_population_text(self):
        """Return the population exactly as shown on the page, e.g. '8,277,114,522'."""
        return self.get_element_text(self.POPULATION_COUNTER)

    def get_population_count(self):
        """Return the population as an integer, e.g. 8277114522."""
        return self.convert_to_number(self.get_population_text())

    def wait_for_population_change(self, old_text):
        """
        Explicitly wait until the counter shows a value different from old_text.
        Returns the new text, or None if it did not change within the timeout.
        """
        try:
            return WebDriverWait(self.driver, COUNTER_CHANGE_WAIT).until(
                text_to_change_from(self.POPULATION_COUNTER, old_text)
            )
        except TimeoutException:
            return None

    @staticmethod
    def convert_to_number(population_text):
        """Convert text like '8,277,114,522' into the integer 8277114522."""
        digits = population_text.replace(",", "").strip()
        if not digits.isdigit():
            raise ValueError(f"Population value is not a number: '{population_text}'")
        return int(digits)
