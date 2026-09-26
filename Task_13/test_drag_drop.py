"""
test_drag_drop.py
------------------------------------------------------------------------------
Task 13 : Pytest suite for the Selenium drag-and-drop automation on
          https://jqueryui.com/droppable/

Run with (generates a mandatory HTML report as required by the task):

    pytest test_drag_drop.py --html=report.html --self-contained-html -v

The suite is split into two clearly-marked groups:

    POSITIVE  -> the feature behaves correctly under valid conditions
                 (the box IS dragged fully onto the target and IS marked
                 as dropped).

    NEGATIVE  -> the feature correctly refuses to register a drop when the
                 interaction is invalid, incomplete, or targets a locator
                 that does not exist -- proving the automation does not
                 produce false positives.
------------------------------------------------------------------------------
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from drag_drop_automation import (
    perform_drag_and_drop,
    get_droppable_text,
    get_draggable_element,
    get_droppable_element,
    is_drop_successful,
    DEFAULT_TEXT,
    DROPPED_TEXT,
    HIGHLIGHT_CLASS,
)


# =============================================================================
# POSITIVE TEST CASES
# =============================================================================

@pytest.mark.positive
def test_page_title_loads_correctly(driver):
    """Sanity check: the jQuery UI Droppable demo page must load with the expected title."""
    driver.switch_to.default_content()
    assert "Droppable" in driver.title
    # restore iframe context so the fixture teardown / later assertions stay consistent
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe.demo-frame"))


@pytest.mark.positive
def test_draggable_and_droppable_elements_are_present(driver):
    """Both the white draggable box and the yellow droppable box must exist and be visible."""
    draggable = get_draggable_element(driver)
    droppable = get_droppable_element(driver)
    assert draggable.is_displayed()
    assert droppable.is_displayed()


@pytest.mark.positive
def test_droppable_shows_default_text_before_any_drop(driver):
    """Before any interaction, the droppable box must show its default placeholder text."""
    assert get_droppable_text(driver) == DEFAULT_TEXT


@pytest.mark.positive
def test_drag_and_drop_success(driver):
    """
    MAIN TASK SCENARIO.
    Dragging the white box fully onto the yellow box must:
        1) change the box's text to 'Dropped!'
        2) be reported as successful by is_drop_successful().
    """
    result = perform_drag_and_drop(driver)
    assert result is True
    assert get_droppable_text(driver) == DROPPED_TEXT


@pytest.mark.positive
def test_droppable_gains_highlight_class_after_successful_drop(driver):
    """After a successful drop, jQuery UI must visually mark the box with the highlight class."""
    perform_drag_and_drop(driver)
    droppable = get_droppable_element(driver)
    assert HIGHLIGHT_CLASS in droppable.get_attribute("class")


# =============================================================================
# NEGATIVE TEST CASES
# =============================================================================

@pytest.mark.negative
def test_drop_is_not_registered_without_any_interaction(driver):
    """Simply loading the page must NEVER, by itself, report a successful drop."""
    assert is_drop_successful(driver) is False
    assert get_droppable_text(driver) == DEFAULT_TEXT


@pytest.mark.negative
def test_releasing_outside_the_droppable_area_does_not_register_a_drop(driver):
    """
    Dragging the white box and releasing it well outside the yellow box's
    boundaries must NOT trigger jQuery UI's drop event.
    """
    result = perform_drag_and_drop(driver, release_offset=(250, 0))
    assert result is False
    assert get_droppable_text(driver) == DEFAULT_TEXT


@pytest.mark.negative
def test_click_without_dragging_does_not_trigger_a_drop(driver):
    """A plain click-and-release on the draggable box (zero movement) must not
    be misinterpreted as a completed drag-and-drop."""
    source = get_draggable_element(driver)
    ActionChains(driver).click_and_hold(source).pause(0.2).release().perform()
    assert is_drop_successful(driver) is False
    assert get_droppable_text(driver) == DEFAULT_TEXT


@pytest.mark.negative
def test_locating_a_nonexistent_element_raises_no_such_element_exception(driver):
    """
    Requesting a locator that does not exist on the page must raise
    NoSuchElementException -- not silently return None or fail with an
    unrelated / misleading error, which is critical for reliable automation.
    """
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.ID, "this-id-does-not-exist-on-page")
