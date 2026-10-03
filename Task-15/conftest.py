"""
conftest.py
Shared pytest fixtures and hooks:
- driver fixture: opens and closes Chrome for every test
- screenshot of failed tests attached to the HTML report
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from utils.config import HEADLESS


@pytest.fixture
def driver():
    """Start Chrome before each test and quit it after the test."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    try:
        browser = webdriver.Chrome(options=options)  # Selenium Manager downloads the driver
    except WebDriverException as error:
        pytest.exit(f"Could not start Chrome browser: {error.msg}")

    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the pytest-html report when a test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        pytest_html = item.config.pluginmanager.getplugin("html")
        if browser and pytest_html:
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image(browser.get_screenshot_as_base64(), "Screenshot"))
            report.extras = extras
