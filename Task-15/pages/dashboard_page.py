"""
dashboard_page.py
Page Object for the OrangeHRM Dashboard (shown after successful login).
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page object representing the OrangeHRM dashboard."""

    # ---------- Locators ----------
    DASHBOARD_HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    USER_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[normalize-space()='Logout']")

    # ---------- Actions ----------
    def is_dashboard_displayed(self):
        """Return True if the Dashboard header is visible."""
        return self.is_element_visible(self.DASHBOARD_HEADER)

    def logout(self):
        """Log out from the application."""
        self.click_element(self.USER_DROPDOWN)
        self.click_element(self.LOGOUT_LINK)
