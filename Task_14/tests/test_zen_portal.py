"""
test_zen_portal.py
Positive and negative test cases for Zen Portal login and logout,
written using the Page Object Model.

Covered scenarios:
 a) Successful login
 b) Unsuccessful login
 c) Validate Username and Password input boxes
 d) Validate Submit button working
 e) Validate Logout button functionality
"""
import pytest

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import INVALID_USERNAME, INVALID_PASSWORD


class TestZenPortal:
    """Test suite for Zen Portal authentication."""

    # ---------- a) Successful Login ----------
    @pytest.mark.positive
    def test_successful_login_with_valid_credentials(self, driver, credentials):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(credentials["username"], credentials["password"])

        assert login_page.is_login_successful(), "User was not redirected after valid login"
        assert DashboardPage(driver).is_dashboard_loaded(), "Dashboard did not load after login"

    # ---------- b) Unsuccessful Login ----------
    @pytest.mark.negative
    def test_unsuccessful_login_with_invalid_credentials(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

        assert login_page.is_still_on_login_page(), "User should stay on login page with invalid credentials"

    @pytest.mark.negative
    def test_unsuccessful_login_with_valid_username_wrong_password(self, driver, credentials):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(credentials["username"], INVALID_PASSWORD)

        assert login_page.is_still_on_login_page(), "User should not log in with a wrong password"

    # ---------- c) Validate Username and Password input boxes ----------
    @pytest.mark.positive
    def test_username_and_password_boxes_are_displayed_and_enabled(self, driver):
        login_page = LoginPage(driver)
        login_page.load()

        assert login_page.is_username_box_displayed(), "Username box is not displayed"
        assert login_page.is_username_box_enabled(), "Username box is not enabled"
        assert login_page.is_password_box_displayed(), "Password box is not displayed"
        assert login_page.is_password_box_enabled(), "Password box is not enabled"

    @pytest.mark.positive
    def test_username_and_password_boxes_accept_input(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.enter_username(INVALID_USERNAME)
        login_page.enter_password(INVALID_PASSWORD)

        assert login_page.get_username_value() == INVALID_USERNAME, "Username box did not accept input"
        assert login_page.get_password_value() == INVALID_PASSWORD, "Password box did not accept input"

    @pytest.mark.positive
    def test_password_box_masks_input(self, driver):
        login_page = LoginPage(driver)
        login_page.load()

        assert login_page.get_password_field_type() == "password", "Password input is not masked"

    # ---------- d) Validate Submit button ----------
    @pytest.mark.positive
    def test_submit_button_is_displayed_and_enabled(self, driver):
        login_page = LoginPage(driver)
        login_page.load()

        assert login_page.is_submit_button_displayed(), "Submit button is not displayed"
        assert login_page.is_submit_button_enabled(), "Submit button is not enabled"

    @pytest.mark.negative
    def test_submit_button_with_empty_fields(self, driver):
        login_page = LoginPage(driver)
        login_page.load()
        login_page.click_submit()

        assert login_page.is_still_on_login_page(), "User should not log in with empty fields"

    # ---------- e) Validate Logout functionality ----------
    @pytest.mark.positive
    def test_logout_functionality(self, driver, credentials):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.load()
        login_page.login(credentials["username"], credentials["password"])
        assert login_page.is_login_successful(), "Login failed, cannot test logout"

        dashboard_page.logout()

        assert login_page.wait_for_url_to_contain("login"), "User was not redirected to login page after logout"
        assert login_page.is_username_box_displayed(), "Login form not shown after logout"
