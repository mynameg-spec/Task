"""
conftest.py
Shared pytest fixtures and hooks:
- driver fixture (browser setup / teardown)
- credentials fixture (skips tests if credentials are not set)
- screenshot on failure attached to the pytest-html report
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from utils.config import HEADLESS, VALID_USERNAME, VALID_PASSWORD


@pytest.fixture
def driver():
    """Create a Chrome WebDriver before each test and quit it afterwards."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")

    try:
        browser = webdriver.Chrome(options=options)  # Selenium Manager handles chromedriver
    except WebDriverException as error:
        pytest.exit(f"Could not start Chrome browser: {error.msg}")

    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture
def credentials():
    """Return valid credentials, or skip the test if they are not configured."""
    if not VALID_USERNAME or not VALID_PASSWORD:
        pytest.skip("Set ZEN_USERNAME and ZEN_PASSWORD environment variables to run this test.")
    return {"username": VALID_USERNAME, "password": VALID_PASSWORD}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the HTML report when a test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        pytest_html = item.config.pluginmanager.getplugin("html")
        if browser and pytest_html:
            screenshot = browser.get_screenshot_as_base64()
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image(screenshot, "Failure screenshot"))
            report.extras = extras
