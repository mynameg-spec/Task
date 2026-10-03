"""
conftest.py
Shared pytest fixtures and hooks:
- driver fixture: opens Chrome before each test and closes it afterwards
- population_page fixture: page object with the page already loaded
- screenshot attached to the HTML report when a test fails
"""
import pytest
from selenium.common.exceptions import WebDriverException

from pages.population_page import PopulationPage
from utils.driver_factory import create_chrome_driver


@pytest.fixture
def driver():
    """Create and later quit the Chrome browser."""
    try:
        browser = create_chrome_driver()
    except WebDriverException as error:
        pytest.exit(f"Could not start Chrome browser: {error.msg}")
    yield browser
    browser.quit()


@pytest.fixture
def population_page(driver):
    """Return a PopulationPage with the URL already opened."""
    page = PopulationPage(driver)
    page.load()
    return page


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
