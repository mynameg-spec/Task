"""
locators.py

This file keeps every element locator (the "address" Selenium uses to find
a button, box, or link) in one place.

Why keep locators separate?
If GUVI ever changes their website design, we only fix this ONE file
instead of hunting through every test.

NOTE FOR GAYATRI:
GUVI's website is built with React, so class names can change without
warning. Before your final run, open https://www.guvi.in/ in Chrome,
right-click the Login button and Inspect it, then compare with the
locators below. Update anything that has changed.
"""

from selenium.webdriver.common.by import By


class HomePageLocators:
    # The "Login" link on the GUVI homepage — confirmed to be a plain
    # text link that says exactly "Login" (no icon/dropdown).
    LOGIN_BUTTON_OPTIONS = [
        (By.XPATH, "//a[normalize-space(text())='Login']"),
        (By.PARTIAL_LINK_TEXT, "Login"),
        (By.XPATH, "//a[contains(@href,'sign-in')]"),
        (By.XPATH, "//button[normalize-space(text())='Login']"),
    ]


class LoginPageLocators:
    # Username / Email input box
    USERNAME_INPUT = (
        By.XPATH,
        "//input[@type='text' or @type='email' or "
        "contains(@placeholder,'Username') or contains(@placeholder,'Email')]",
    )

    # Password input box
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")

    # Login / Submit button on the sign-in page
    SUBMIT_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Login')] | //*[@id='login-btn']",
    )

    # Error message shown after a failed login attempt
    ERROR_MESSAGE = (
        By.XPATH,
        "//*[contains(text(),'incorrect') or contains(text(),'Invalid') "
        "or contains(text(),'forgot your password')]",
    )
