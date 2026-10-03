"""
create_test_data.py
Creates test_data/login_test_data.xlsx with 5 sets of username and password.
Run once:  python -m utils.create_test_data
"""
from utils.config import EXCEL_FILE_PATH, SHEET_NAME
from utils.excel_utils import ExcelUtils

# 5 login combinations: 1 valid and 4 invalid
LOGIN_TEST_DATA = [
    ("TC_01", "Admin", "admin123"),         # Valid username and password
    ("TC_02", "Admin", "wrongpass123"),     # Valid username, invalid password
    ("TC_03", "InvalidUser", "admin123"),   # Invalid username, valid password
    ("TC_04", "TestUser01", "Test@1234"),   # Invalid username and password
    ("TC_05", "Admin", "ADMIN123"),         # Password in wrong case
]


def create_login_test_data_file():
    """Create the Excel file used by the data driven tests."""
    ExcelUtils(EXCEL_FILE_PATH, SHEET_NAME).create_test_data_file(LOGIN_TEST_DATA)
    print(f"Test data file created: {EXCEL_FILE_PATH}")


if __name__ == "__main__":
    create_login_test_data_file()
