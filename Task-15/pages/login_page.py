"""
login_page.py
Page Object for the OrangeHRM Login page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.config import BASE_URL, DASHBOARD_URL_KEYWORD


class LoginPage(BasePage):
    """Page object representing the OrangeHRM login page."""

    # ---------- Locators ----------
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    INVALID_CREDENTIALS_MESSAGE = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
    REQUIRED_FIELD_MESSAGE = (By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')]")

    # ---------- Actions ----------
    def load(self):
        """Open the login page and wait until the username field is visible."""
        self.open_url(BASE_URL)
        self.find_visible_element(self.USERNAME_INPUT)

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Enter credentials and click Login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def wait_for_login_outcome(self):
        """
        Wait (explicitly) until the page shows ONE of these outcomes:
        - Dashboard URL (login successful)
        - 'Invalid credentials' message
        - 'Required' field message
        Returns True if the dashboard was reached, otherwise False.
        """
        try:
            self.wait.until(EC.any_of(
                EC.url_contains(DASHBOARD_URL_KEYWORD),
                EC.visibility_of_element_located(self.INVALID_CREDENTIALS_MESSAGE),
                EC.visibility_of_element_located(self.REQUIRED_FIELD_MESSAGE),
            ))
        except TimeoutException:
            return False
        return DASHBOARD_URL_KEYWORD in self.driver.current_url

    def get_error_message(self):
        """Return the invalid credentials message text, or empty string if not shown."""
        if self.is_element_visible(self.INVALID_CREDENTIALS_MESSAGE):
            return self.find_visible_element(self.INVALID_CREDENTIALS_MESSAGE).text
        return ""
