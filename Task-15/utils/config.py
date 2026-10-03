"""
config.py
Central configuration for the OrangeHRM Data Driven Testing framework.
"""
import os

# Application under test
BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
DASHBOARD_URL_KEYWORD = "dashboard"

# Project root folder (one level above utils)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Excel test data file details
EXCEL_FILE_PATH = os.path.join(PROJECT_ROOT, "test_data", "login_test_data.xlsx")
SHEET_NAME = "LoginData"

# Name written in the "Name of Tester" column
TESTER_NAME = os.getenv("TESTER_NAME", "Gayatri")

# Explicit wait timeout in seconds
EXPLICIT_WAIT = 20

# Run browser without UI if HEADLESS=true
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
