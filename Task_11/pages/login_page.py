"""
login_page.py

This is the Page Object for two screens:
  1) The GUVI homepage (https://www.guvi.in/)
  2) The GUVI sign-in page (https://www.guvi.in/sign-in/)

It uses the reusable actions from base_page.py, plus the locators
from locators.py.
"""

from pages.base_page import BasePage
from pages.locators import HomePageLocators, LoginPageLocators

HOME_URL = "https://www.guvi.in/"
SIGN_IN_URL = "https://www.guvi.in/sign-in/"


class LoginPage(BasePage):

    def go_to_homepage(self):
        """Step 1: Visit the GUVI homepage, then dismiss any cookie banner."""
        self.open(HOME_URL)
        self.dismiss_cookie_banner()

    def click_login_button(self):
        """Step 2: Click the Login button on the homepage."""
        self.click_any(HomePageLocators.LOGIN_BUTTON_OPTIONS, description="the homepage Login button")

    def enter_username(self, username):
        self.type_text(LoginPageLocators.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.type_text(LoginPageLocators.PASSWORD_INPUT, password)

    def click_submit(self):
        self.click(LoginPageLocators.SUBMIT_BUTTON)

    def login(self, username, password):
        """Step 3: Fill the form and log in."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()

    # ---- Validation helper methods used by the pytest test cases ----

    def is_on_sign_in_url(self):
        """Check the browser URL matches the expected sign-in URL."""
        return "guvi.in/sign-in" in self.get_current_url()

    def is_username_field_ready(self):
        return self.is_visible(LoginPageLocators.USERNAME_INPUT) and \
               self.is_enabled(LoginPageLocators.USERNAME_INPUT)

    def is_password_field_ready(self):
        return self.is_visible(LoginPageLocators.PASSWORD_INPUT) and \
               self.is_enabled(LoginPageLocators.PASSWORD_INPUT)

    def is_submit_button_ready(self):
        return self.is_visible(LoginPageLocators.SUBMIT_BUTTON) and \
               self.is_enabled(LoginPageLocators.SUBMIT_BUTTON)

    def is_error_message_shown(self):
        return self.is_visible(LoginPageLocators.ERROR_MESSAGE)
