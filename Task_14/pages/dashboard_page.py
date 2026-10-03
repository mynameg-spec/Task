"""
dashboard_page.py
Page Object for the Zen Portal Dashboard (page shown after login).
Contains the logout flow.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page object representing the Zen Portal dashboard."""

    # ---------- Locators ----------
    PROFILE_MENU = (
        By.XPATH,
        "//*[contains(@class,'avatar') or contains(@class,'profile') or contains(@alt,'profile')]",
    )
    LOGOUT_OPTION = (
        By.XPATH,
        "//*[normalize-space()='Log out' or normalize-space()='Logout' or normalize-space()='Log Out']",
    )

    # ---------- Actions ----------
    def is_dashboard_loaded(self):
        """Dashboard is loaded when the profile menu is visible."""
        return self.is_element_displayed(self.PROFILE_MENU)

    def open_profile_menu(self):
        """Click the profile icon to open the dropdown menu."""
        self.click_element(self.PROFILE_MENU)

    def click_logout(self):
        """Click the Log out option from the profile dropdown."""
        self.click_element(self.LOGOUT_OPTION)

    def logout(self):
        """Complete logout flow: open profile menu and click Log out."""
        self.open_profile_menu()
        self.click_logout()
