"""
conftest.py

Pytest automatically finds this file and runs the code inside it
before/after every test. It handles:
  1) Opening a fresh Chrome browser before each test
  2) Closing the browser after each test (Step 4 of the task: "Close the
     browser and stop the automation")
  3) Safely loading your GUVI username/password from a local .env file
     (never hardcoded in the test code itself)
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load GUVI_USERNAME and GUVI_PASSWORD from a local .env file (see .env.example)
load_dotenv()


@pytest.fixture
def driver():
    """Creates a Chrome browser, hands it to the test, then closes it."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=options)

    yield chrome_driver  # the test runs here

    chrome_driver.quit()  # runs after the test finishes (pass or fail)


@pytest.fixture
def guvi_credentials():
    """Reads real login credentials from environment variables, not code."""
    username = os.environ.get("GUVI_USERNAME")
    password = os.environ.get("GUVI_PASSWORD")

    if not username or not password:
        pytest.skip(
            "GUVI_USERNAME / GUVI_PASSWORD not set. "
            "Copy .env.example to .env and fill in your real details."
        )

    return {"username": username, "password": password}
