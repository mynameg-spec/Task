"""
conftest.py
------------------------------------------------------------------------------
Shared Pytest configuration for the Task 13 drag-and-drop test suite.

Contains:
    * `driver` fixture -- hands every test a FRESH browser session that is
      already navigated to the demo page and switched into the iframe.
    * A `pytest_runtest_makereport` hook -- on any test failure, grabs a
      screenshot of the browser at the moment of failure and embeds it
      directly into the pytest-html report, so a failure can be diagnosed
      without re-running anything.
------------------------------------------------------------------------------
"""

import pytest
import pytest_html

from drag_drop_automation import (
    get_chrome_driver,
    open_droppable_page,
    switch_to_demo_frame,
)


@pytest.fixture(scope="function")
def driver():
    """
    Yield a ready-to-use Chrome driver, already on the droppable demo page
    and switched into the iframe.

    Scope is deliberately FUNCTION-level (a brand-new browser per test),
    not session/module level. The page's state (the box's text/CSS class)
    is mutated by a successful drop, so a shared browser across tests would
    make later tests depend on the order earlier tests ran in -- exactly the
    kind of flaky, order-dependent test suite good QA practice avoids.
    """
    drv = get_chrome_driver(headless=True)
    open_droppable_page(drv)
    switch_to_demo_frame(drv)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the HTML report whenever a test fails."""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            try:
                screenshot_b64 = drv.get_screenshot_as_base64()
                extras.append(pytest_html.extras.image(screenshot_b64, name="Failure Screenshot"))
            except Exception:
                pass  # reporting must never mask the real test failure

    report.extras = extras


def pytest_html_report_title(report):
    """Give the generated HTML report a descriptive title instead of the default 'report.html'."""
    report.title = "Task 13 - Drag and Drop Automation Report (jqueryui.com/droppable)"
