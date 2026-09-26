"""
test_login.py

Task 11 — GUVI Selenium + Pytest Automation

What this file does (matches the task steps):
  1) Visit https://www.guvi.in/
  2) Click Login -> lands on https://www.guvi.in/sign-in/
  3) Log in with a valid Username and Password
  4) Browser closes automatically after every test (see conftest.py)

Then it checks these 3 things, using both POSITIVE (should work) and
NEGATIVE (should correctly fail / show an error) test cases:
  A) The Login button correctly leads to the https://www.guvi.in/sign-in/ URL
  B) The Username and Password boxes are visible and enabled
  C) The Submit/Login button works properly

Run this file with:
    pytest tests/test_login.py -v --html=reports/report.html --self-contained-html
"""

import pytest
from pages.login_page import LoginPage, SIGN_IN_URL


# ---------------------------------------------------------------------
# A) VALIDATE THE LOGIN BUTTON URL
# ---------------------------------------------------------------------

@pytest.mark.positive
def test_login_button_navigates_to_correct_signin_url(driver):
    """POSITIVE: Clicking Login on the homepage should open the sign-in URL."""
    login_page = LoginPage(driver)
    login_page.go_to_homepage()
    login_page.click_login_button()

    assert login_page.is_on_sign_in_url(), (
        f"Expected the URL to contain 'guvi.in/sign-in' but got "
        f"'{login_page.get_current_url()}'"
    )


@pytest.mark.negative
def test_direct_wrong_url_is_not_treated_as_signin_page(driver):
    """NEGATIVE: A random/incorrect URL must NOT be mistaken for the sign-in page."""
    login_page = LoginPage(driver)
    login_page.open("https://www.guvi.in/about-us/")

    assert not login_page.is_on_sign_in_url(), (
        "The about-us page should NOT be identified as the sign-in page."
    )


# ---------------------------------------------------------------------
# B) VALIDATE USERNAME AND PASSWORD FIELDS ARE VISIBLE AND ENABLED
# ---------------------------------------------------------------------

@pytest.mark.positive
def test_username_and_password_fields_are_visible_and_enabled(driver):
    """POSITIVE: Both login fields should be visible and enabled for typing."""
    login_page = LoginPage(driver)
    login_page.open(SIGN_IN_URL)

    assert login_page.is_username_field_ready(), "Username field is not visible/enabled"
    assert login_page.is_password_field_ready(), "Password field is not visible/enabled"


@pytest.mark.negative
def test_fields_are_not_wrongly_reported_ready_on_homepage(driver):
    """NEGATIVE: On the homepage (no login form), fields must correctly show as NOT ready."""
    login_page = LoginPage(driver)
    login_page.open("https://www.guvi.in/")

    assert not login_page.is_username_field_ready(), (
        "Username field should not exist/be ready on the homepage."
    )


# ---------------------------------------------------------------------
# C) VALIDATE THE SUBMIT / LOGIN BUTTON WORKS PROPERLY
# ---------------------------------------------------------------------

@pytest.mark.positive
def test_submit_button_is_visible_and_clickable(driver):
    """POSITIVE: The Login/Submit button should be visible and enabled."""
    login_page = LoginPage(driver)
    login_page.open(SIGN_IN_URL)

    assert login_page.is_submit_button_ready(), "Submit button is not visible/enabled"


@pytest.mark.positive
def test_valid_login_completes_successfully(driver, guvi_credentials):
    """
    POSITIVE (full end-to-end flow, task steps 1-4):
    Visit homepage -> click Login -> sign in with a VALID account
    -> confirm we leave the sign-in page (login succeeded).
    """
    login_page = LoginPage(driver)
    login_page.go_to_homepage()
    login_page.click_login_button()
    login_page.login(guvi_credentials["username"], guvi_credentials["password"])

    assert not login_page.is_on_sign_in_url(), (
        "Still on the sign-in page — valid login did not succeed."
    )


@pytest.mark.negative
def test_invalid_password_shows_error_and_blocks_login(driver, guvi_credentials):
    """NEGATIVE: A wrong password should show an error and NOT log the user in."""
    login_page = LoginPage(driver)
    login_page.open(SIGN_IN_URL)
    login_page.login(guvi_credentials["username"], "wrong_password_123")

    assert login_page.is_on_sign_in_url(), (
        "User was logged in with a wrong password — this should never happen."
    )


@pytest.mark.negative
def test_empty_credentials_login_is_blocked(driver):
    """NEGATIVE: Submitting the form with empty fields should not log anyone in."""
    login_page = LoginPage(driver)
    login_page.open(SIGN_IN_URL)
    login_page.click_submit()

    assert login_page.is_on_sign_in_url(), (
        "Login went through with empty fields — this should never happen."
    )
