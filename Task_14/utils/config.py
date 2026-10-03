"""
config.py
Central place for test configuration.
Real credentials are read from environment variables so they are never
committed to GitHub (code hygiene + security).
"""
import os

# Zen Portal login page URL
BASE_URL = "https://v2.zenclass.in/login"

# Valid credentials (set these as environment variables before running)
VALID_USERNAME = os.getenv("ZEN_USERNAME", "")
VALID_PASSWORD = os.getenv("ZEN_PASSWORD", "")

# Invalid credentials used for negative test cases
INVALID_USERNAME = "invalid.user@example.com"
INVALID_PASSWORD = "WrongPassword@123"

# Explicit wait timeouts (seconds)
EXPLICIT_WAIT = 15
SHORT_WAIT = 5

# Run browser in headless mode if HEADLESS=true
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
