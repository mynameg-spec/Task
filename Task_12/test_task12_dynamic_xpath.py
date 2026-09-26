"""
==============================================================================
 Pytest test cases for Task - 12 (Dynamic XPath on https://www.guvi.in/)
 Level : Beginner
==============================================================================

Each test function checks ONE requirement from the task sheet.
"pytest" automatically runs every function whose name starts with "test_".

HOW TO RUN AND GET THE HTML REPORT (required by the task):
    pytest test_task12_dynamic_xpath.py --html=report.html --self-contained-html -v

This will create a file called report.html - open it in your browser to see
a pass/fail summary of every test.
"""

import pytest

from task12_dynamic_xpath import (
    open_browser,
    find_target_element,
    get_parent_element,
    get_first_child_of_parent,
    get_second_sibling,
    get_parent_of_href_element,
    get_all_ancestors,
    get_all_following_siblings,
    get_all_preceding_elements,
)


@pytest.fixture(scope="module")
def driver():
    """
    This fixture opens the browser ONCE before all tests run, and closes it
    after all tests finish. Every test function below can use it by simply
    listing "driver" as a parameter.
    """
    drv = open_browser()
    yield drv
    drv.quit()


# --------------------------- Relative XPath tests ---------------------------

def test_parent_element_found(driver):
    """Check that the target element's parent can be located."""
    target = find_target_element(driver)
    parent = get_parent_element(target)
    assert parent is not None


def test_first_child_of_parent_found(driver):
    """Check that the parent's first child element can be located."""
    target = find_target_element(driver)
    parent = get_parent_element(target)
    first_child = get_first_child_of_parent(parent)
    assert first_child is not None


def test_second_sibling_found(driver):
    """Check that the target element has a second sibling."""
    target = find_target_element(driver)
    second_sibling = get_second_sibling(target)
    assert second_sibling is not None


def test_parent_of_href_element_found(driver):
    """Check that we can find the parent of an element with an href attribute."""
    parent = get_parent_of_href_element(driver)
    assert parent is not None


# ------------------------------- Axes tests ---------------------------------

def test_ancestor_elements_found(driver):
    """Check that at least one ancestor element is found (e.g. <html>, <body>)."""
    target = find_target_element(driver)
    ancestors = get_all_ancestors(target)
    assert len(ancestors) > 0


def test_following_sibling_elements_found(driver):
    """Check that following-sibling elements are found after the target."""
    target = find_target_element(driver)
    following_siblings = get_all_following_siblings(target)
    assert len(following_siblings) > 0


def test_preceding_elements_found(driver):
    """Check that preceding elements are found before the target."""
    target = find_target_element(driver)
    preceding_elements = get_all_preceding_elements(target)
    assert len(preceding_elements) > 0
