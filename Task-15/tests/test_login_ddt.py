"""
test_login_ddt.py
Data Driven login test for OrangeHRM.

Flow for every row in the Excel file:
 1. Read Test ID, Username and Password from Excel
 2. Open the OrangeHRM login page
 3. Login with the Excel credentials
 4. Write Date, Time of Test, Name of Tester and Test Result back to Excel
 5. Assert the result so it also appears in the pytest HTML report
"""
import os

import pytest

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import EXCEL_FILE_PATH, SHEET_NAME, TESTER_NAME
from utils.excel_utils import ExcelUtils
from utils.create_test_data import create_login_test_data_file

# Create the Excel file automatically if it does not exist yet
if not os.path.exists(EXCEL_FILE_PATH):
    create_login_test_data_file()

excel = ExcelUtils(EXCEL_FILE_PATH, SHEET_NAME)
LOGIN_DATA = excel.get_login_test_data()


@pytest.mark.parametrize("data", LOGIN_DATA, ids=[row["test_id"] for row in LOGIN_DATA])
def test_login_with_excel_data(driver, data):
    """Login using each username/password from Excel and record the result in Excel."""
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(data["username"], data["password"])

    login_successful = login_page.wait_for_login_outcome() and DashboardPage(driver).is_dashboard_displayed()

    result = "Test Passed" if login_successful else "Test Failed"
    excel.write_test_result(data["row"], TESTER_NAME, result)

    assert login_successful, (
        f"{data['test_id']}: Login failed for username '{data['username']}'. "
        f"Message: {login_page.get_error_message()}"
    )
