"""
login_page.py
Page Object for the Zen Portal Login page.
Contains locators and actions related only to the login screen.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL, SHORT_WAIT


class LoginPage(BasePage):
    """Page object representing the Zen Portal login page."""

    # ---------- Locators ----------
    USERNAME_INPUT = (By.XPATH, "//input[@type='email' or contains(@placeholder,'mail')]")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' or contains(normalize-space(),'Sign in')]")
    ERROR_MESSAGE = (
        By.XPATH,
        "//*[contains(@class,'invalid') or contains(@class,'error') "
        "or contains(text(),'Incorrect') or contains(text(),'Invalid')]",
    )

    LOGIN_URL_KEYWORD = "login"

    # ---------- Actions ----------
    def load(self):
        """Open the Zen Portal login page and wait for the username box."""
        self.open_url(BASE_URL)
        self.find_visible_element(self.USERNAME_INPUT)

    def enter_username(self, username):
        """Type the username into the username input box."""
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Type the password into the password input box."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_submit(self):
        """Click the Sign in / Submit button."""
        self.click_element(self.SUBMIT_BUTTON)

    def login(self, username, password):
        """Complete login flow: enter username, password and submit."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()

    # ---------- Validations ----------
    def is_username_box_displayed(self):
        return self.is_element_displayed(self.USERNAME_INPUT)

    def is_password_box_displayed(self):
        return self.is_element_displayed(self.PASSWORD_INPUT)

    def is_username_box_enabled(self):
        return self.is_element_enabled(self.USERNAME_INPUT)

    def is_password_box_enabled(self):
        return self.is_element_enabled(self.PASSWORD_INPUT)

    def is_submit_button_displayed(self):
        return self.is_element_displayed(self.SUBMIT_BUTTON)

    def is_submit_button_enabled(self):
        return self.is_element_enabled(self.SUBMIT_BUTTON)

    def get_username_value(self):
        return self.get_attribute_value(self.USERNAME_INPUT, "value")

    def get_password_value(self):
        return self.get_attribute_value(self.PASSWORD_INPUT, "value")

    def get_password_field_type(self):
        """Password field should be of type 'password' so input is masked."""
        return self.get_attribute_value(self.PASSWORD_INPUT, "type")

    def is_login_successful(self, timeout=None):
        """Login is successful when the app navigates away from the /login URL."""
        return self.wait_for_url_to_not_contain(self.LOGIN_URL_KEYWORD, timeout)

    def is_still_on_login_page(self):
        """Wait briefly, then confirm the user is still on the login page."""
        navigated_away = self.wait_for_url_to_not_contain(self.LOGIN_URL_KEYWORD, SHORT_WAIT)
        return not navigated_away

    def is_error_message_displayed(self):
        return self.is_element_displayed(self.ERROR_MESSAGE, timeout=SHORT_WAIT)
