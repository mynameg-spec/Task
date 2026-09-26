"""
drag_drop_automation.py
------------------------------------------------------------------------------
Task 13 : Drag-and-Drop automation on https://jqueryui.com/droppable/
          using Selenium WebDriver + ActionChains.

This module is the reusable "core" automation layer (a light Page Object).
It contains no test assertions itself -- it only knows HOW to open the page,
find the two boxes, and perform a drag-and-drop. The Pytest suite in
test_drag_drop.py imports these functions and adds the actual test
assertions (both positive and negative scenarios) on top of them.

Keeping the automation logic and the test logic in separate files is a
standard, interview-friendly design choice: it lets the same drag-and-drop
routine be reused from a script, a test suite, or a CI job without any
duplication.
------------------------------------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --------------------------------------------------------------------------- #
# Configuration constants (kept at module level so both the automation code
# and the test suite reference a single source of truth for locators/text).
# --------------------------------------------------------------------------- #
DROPPABLE_DEMO_URL = "https://jqueryui.com/droppable/"
DEMO_IFRAME_SELECTOR = "iframe.demo-frame"    # jqueryui.com wraps every live demo in this iframe
DRAGGABLE_ELEMENT_ID = "draggable"            # White rectangular box: "Drag me to my target"
DROPPABLE_ELEMENT_ID = "droppable"            # Yellow rectangular box: "Drop here"
DROPPED_TEXT = "Dropped!"                     # Text shown inside the box after a successful drop
DEFAULT_TEXT = "Drop here"                    # Text shown inside the box before any drop
HIGHLIGHT_CLASS = "ui-state-highlight"        # CSS class jQuery UI adds to the box on a successful drop
DEFAULT_TIMEOUT = 15                          # seconds, used for every explicit wait below


def get_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Build and return a configured Chrome WebDriver instance.

    :param headless: run Chrome without a visible UI window (True for CI/CD).
    :return: a ready-to-use selenium.webdriver.Chrome instance.
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")

    # Selenium 4.6+ ships "Selenium Manager", which resolves and downloads the
    # matching chromedriver binary automatically -- no manual driver path needed.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    return driver


def open_droppable_page(driver: webdriver.Chrome) -> None:
    """Navigate the browser to the jQuery UI Droppable demo page."""
    driver.get(DROPPABLE_DEMO_URL)


def switch_to_demo_frame(driver: webdriver.Chrome) -> None:
    """
    The live widget lives inside <iframe class="demo-frame"> on jqueryui.com.
    Selenium must switch context into that iframe before it can see
    #draggable / #droppable -- they do not exist in the outer document.
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    driver.switch_to.default_content()
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, DEMO_IFRAME_SELECTOR)))
    driver.switch_to.frame(iframe)


def get_draggable_element(driver: webdriver.Chrome):
    """Locate the white draggable rectangle. Raises NoSuchElementException if absent/removed."""
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    return wait.until(EC.presence_of_element_located((By.ID, DRAGGABLE_ELEMENT_ID)))


def get_droppable_element(driver: webdriver.Chrome):
    """Locate the yellow droppable rectangle. Raises NoSuchElementException if absent/removed."""
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    return wait.until(EC.presence_of_element_located((By.ID, DROPPABLE_ELEMENT_ID)))


def get_droppable_text(driver: webdriver.Chrome) -> str:
    """Return the current label text shown inside the droppable box."""
    droppable = get_droppable_element(driver)
    return droppable.find_element(By.TAG_NAME, "p").text.strip()


def is_drop_successful(driver: webdriver.Chrome) -> bool:
    """
    A drop is only considered successful when BOTH of the following are true:
        1) the droppable box's text has changed to 'Dropped!'
        2) jQuery UI has added the 'ui-state-highlight' class to the box.

    Checking both signals (not just the text) avoids a false positive that
    a text-only check could miss -- e.g. a page-load race condition.
    """
    droppable = get_droppable_element(driver)
    text_ok = droppable.find_element(By.TAG_NAME, "p").text.strip() == DROPPED_TEXT
    class_ok = HIGHLIGHT_CLASS in droppable.get_attribute("class")
    return text_ok and class_ok


def perform_drag_and_drop(driver: webdriver.Chrome, release_offset: tuple = None) -> bool:
    """
    CORE TASK FUNCTION.
    Drags the white box (#draggable) onto the yellow box (#droppable) using
    Selenium ActionChains and reports whether jQuery UI registered the drop.

    A single ActionChains.drag_and_drop() call is unreliable against jQuery
    UI widgets, because they listen for intermediate mousemove events rather
    than a single jump from A to B. The interaction is therefore broken into
    explicit steps:

        click_and_hold(source) -> move_to_element(target) -> pause -> release()

    :param driver: an active Selenium WebDriver, already switched into the demo iframe.
    :param release_offset: optional (x, y) pixel offset applied on top of the
                            target element's centre when moving the mouse.
                            Used by negative tests to simulate a release that
                            lands OUTSIDE the droppable box's boundaries.
    :return: True if jQuery UI reports a successful drop, False otherwise.
    """
    source = get_draggable_element(driver)
    target = get_droppable_element(driver)

    action = ActionChains(driver)
    if release_offset:
        action.click_and_hold(source).move_to_element_with_offset(
            target, release_offset[0], release_offset[1]
        ).pause(0.3).release()
    else:
        action.click_and_hold(source).move_to_element(target).pause(0.3).release()
    action.perform()

    return is_drop_successful(driver)


def run_full_scenario(headless: bool = True) -> bool:
    """
    Convenience entry point used when this file is executed directly
    (`python drag_drop_automation.py`): opens the page, performs the
    drag-and-drop, prints the outcome, and cleans up the browser.
    """
    driver = get_chrome_driver(headless=headless)
    try:
        open_droppable_page(driver)
        switch_to_demo_frame(driver)
        result = perform_drag_and_drop(driver)
        status = "SUCCEEDED" if result else "FAILED"
        print(f"Drag-and-drop {status}. Droppable box now reads: '{get_droppable_text(driver)}'")
        return result
    finally:
        driver.quit()


if __name__ == "__main__":
    run_full_scenario(headless=True)
