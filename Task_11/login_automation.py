"""
login_automation.py

Task 11 — Part 1: the plain Selenium automation script.

This file does exactly the 4 steps GUVI asked for:
  1) Visit https://www.guvi.in/
  2) Click the Login button -> migrates to https://www.guvi.in/sign-in/
  3) Log in using a valid Username and Password
  4) Close the browser and stop the automation

Your Username and Password are read from a local .env file — they are
NEVER typed directly into this script. See .env.example for the format.

Run it with:
    python login_automation.py
"""

import os
import sys
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage

load_dotenv()


def run_login_automation():
    username = os.environ.get("GUVI_USERNAME")
    password = os.environ.get("GUVI_PASSWORD")

    if not username or not password:
        print("ERROR: GUVI_USERNAME / GUVI_PASSWORD not found.")
        print("Copy .env.example to .env and fill in your real GUVI login details.")
        sys.exit(1)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        login_page = LoginPage(driver)

        # Step 1: Visit the homepage
        login_page.go_to_homepage()
        print("Step 1 done: Homepage opened.")

        # Step 2: Click Login -> migrates to the sign-in URL
        login_page.click_login_button()
        time.sleep(1)  # small pause so the sign-in page fully loads
        print(f"Step 2 done: Now on {login_page.get_current_url()}")

        # Step 3: Log in with valid credentials
        login_page.login(username, password)
        time.sleep(2)  # give the site a moment to process the login
        print("Step 3 done: Login form submitted.")

    finally:
        # Step 4: Close the browser and stop the automation
        driver.quit()
        print("Step 4 done: Browser closed. Automation stopped.")


if __name__ == "__main__":
    run_login_automation()
