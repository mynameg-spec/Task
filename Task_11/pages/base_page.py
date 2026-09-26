"""
base_page.py

This class holds actions that EVERY page needs — like clicking, typing,
and waiting for something to appear. Every other page file will reuse
these actions instead of repeating the same code again and again.
"""

import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Wait up to 15 seconds before giving up on finding an element
        self.wait = WebDriverWait(driver, 15)

    def open(self, url):
        """Open a given URL in the browser."""
        self.driver.get(url)

    def save_debug_info(self, name):
        """
        If something can't be found, save a screenshot + the page's HTML
        into a 'debug' folder. This lets us SEE exactly what the browser
        was looking at, instead of guessing why a locator failed.
        """
        os.makedirs("debug", exist_ok=True)
        try:
            self.driver.save_screenshot(f"debug/{name}.png")
            with open(f"debug/{name}.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print(f"Saved debug/{name}.png and debug/{name}.html for inspection.")
        except Exception as e:
            print(f"Could not save debug info: {e}")

    def dismiss_cookie_banner(self):
        """
        Many sites (including GUVI) show a cookie-consent banner on first
        load. We don't know the exact button wording, so we try several
        common ones. If none appear within a few seconds, we just move on
        — this never blocks the rest of the automation.
        """
        from selenium.webdriver.common.by import By

        possible_texts = [
            "Accept All", "Accept all", "Accept", "Accept Cookies",
            "I Agree", "Got it", "OK", "Allow all", "Allow All", "Close",
        ]
        short_wait = WebDriverWait(self.driver, 3)
        for text in possible_texts:
            locator = (By.XPATH, f"//*[self::button or self::a][normalize-space(text())='{text}']")
            try:
                element = short_wait.until(EC.element_to_be_clickable(locator))
                element.click()
                print(f"Cookie banner dismissed (clicked '{text}').")
                return
            except TimeoutException:
                continue
        print("No cookie banner found (or it used different wording) — continuing.")

    def click(self, locator):
        """Wait until an element can be clicked, then click it."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self._safe_click(element)
        except TimeoutException:
            self.save_debug_info("click_timeout")
            raise

    def click_any(self, locators, description="element"):
        """
        Try a LIST of possible locators one by one (websites often have
        more than one way an element could be built). Uses the first one
        that is found and clickable.
        """
        last_error = None
        for locator in locators:
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self._safe_click(element)
                return
            except TimeoutException as e:
                last_error = e
                continue
        # None of the locators worked — save debug info before failing
        self.save_debug_info("click_any_timeout")
        raise TimeoutException(
            f"Could not find/click {description} using any of the known locators. "
            f"Check debug/click_any_timeout.png and debug/click_any_timeout.html"
        ) from last_error

    def _safe_click(self, element):
        """
        Scrolls the element into view first, then clicks it. If something
        (like a leftover banner) is covering it and blocks a normal click,
        falls back to a direct JavaScript click.
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            print("Normal click was blocked by something on screen — using a JS click instead.")
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        """Find an input box, clear old text, and type new text into it."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def is_visible(self, locator):
        """Return True if the element is visible on the page, else False."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except Exception:
            return False

    def is_enabled(self, locator):
        """Return True if the element is visible AND clickable (enabled)."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_enabled()
        except Exception:
            return False

    def get_current_url(self):
        """Return the URL the browser is currently on."""
        return self.driver.current_url
