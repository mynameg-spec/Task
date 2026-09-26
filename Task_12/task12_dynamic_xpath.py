"""
==============================================================================
 Task - 12 : Dynamic XPath Validation on https://www.guvi.in/
 Level    : Beginner
 Author   : Gayatri
==============================================================================

WHAT THIS SCRIPT DOES (in plain English)
-----------------------------------------
GUVI's home page has a top menu bar with links: Courses, Live Classes,
Practice, Resources, Our Solutions, Login, Signup.

We pick ONE of these links -> "Courses" -> and call it our "target element".
Starting from that one element, we use XPath to walk around the HTML page:

  RELATIVE XPATH (moving to elements connected to our target)
    1. Go UP to its parent element.
    2. From that parent, get its FIRST child element.
    3. Get the SECOND sibling of our target (the next link after it).
    4. Find an element that has an "href" attribute, then get ITS parent.

  AXES (a way to say "give me a whole group of related elements")
    5. Get ALL ancestor elements (parent, grandparent, ... up to <html>).
    6. Get ALL following-sibling elements (every link that comes after it).
    7. Get ALL preceding elements (everything before it in the HTML).

Quick XPath cheat-sheet used below:
    ..                    -> go to the parent element
    *[1]                  -> the 1st child element
    following-sibling::*  -> siblings that come AFTER this element
    preceding::*          -> every element that comes BEFORE this one
    ancestor::*           -> every parent/grandparent/... up to <html>
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# The GUVI page we are testing
GUVI_URL = "https://www.guvi.in/"

# The nav-bar link we are using as our "target element".
# (This is the first item in the red-underlined menu shown in the task image.)
TARGET_LINK_TEXT = "Courses"


def open_browser():
    """
    Step 1: Open Chrome and go to the GUVI website.
    Returns the driver so we can use it in later steps.
    """
    options = Options()
    options.add_argument("--start-maximized")
    # Uncomment the next line if you want the test to run without opening
    # a visible browser window:
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get(GUVI_URL)

    # Wait up to 10 seconds for the page to load before doing anything else
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    return driver


def find_target_element(driver):
    """
    Step 2: Find our target element -> the "Courses" link.
    We use a simple XPath: an <a> tag whose visible text is "Courses".
    """
    target_xpath = f"//a[text()='{TARGET_LINK_TEXT}']"
    target_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, target_xpath))
    )
    return target_element


# -----------------------------------------------------------------------
# PART A : RELATIVE XPATH
# -----------------------------------------------------------------------

def get_parent_element(target_element):
    """Go UP one level from the target element to reach its parent."""
    return target_element.find_element(By.XPATH, "./..")


def get_first_child_of_parent(parent_element):
    """From the parent element, get its FIRST child element."""
    return parent_element.find_element(By.XPATH, "./*[1]")


def get_second_sibling(target_element):
    """
    Get the SECOND sibling of the target element.
    Our target itself counts as sibling #1, so its "2nd sibling" is the
    very next element after it -> following-sibling::*[1]
    """
    try:
        return target_element.find_element(By.XPATH, "./following-sibling::*[1]")
    except Exception:
        # No second sibling exists
        return None


def get_parent_of_href_element(driver):
    """
    Find the first element on the page that has an "href" attribute
    (this will normally be a link, <a href="...">), then return ITS
    parent element.
    """
    href_element = driver.find_element(By.XPATH, "//*[@href][1]")
    return href_element.find_element(By.XPATH, "./..")


# -----------------------------------------------------------------------
# PART B : AXES
# -----------------------------------------------------------------------

def get_all_ancestors(target_element):
    """Get every ancestor of the target element (parent, grandparent, ...)."""
    return target_element.find_elements(By.XPATH, "./ancestor::*")


def get_all_following_siblings(target_element):
    """Get every element that comes AFTER the target at the same level."""
    return target_element.find_elements(By.XPATH, "./following-sibling::*")


def get_all_preceding_elements(target_element):
    """Get every element that appears BEFORE the target in the HTML."""
    return target_element.find_elements(By.XPATH, "./preceding::*")


# -----------------------------------------------------------------------
# MAIN : run everything step by step and print the results
# -----------------------------------------------------------------------

def main():
    driver = open_browser()

    try:
        target_element = find_target_element(driver)
        print(f"Target element found -> <{target_element.tag_name}> "
              f"text = '{target_element.text}'")

        # ---- Relative XPath ----
        parent_element = get_parent_element(target_element)
        print(f"\n1) Parent element        -> <{parent_element.tag_name}>")

        first_child = get_first_child_of_parent(parent_element)
        print(f"2) Parent's first child  -> <{first_child.tag_name}> "
              f"text = '{first_child.text}'")

        second_sibling = get_second_sibling(target_element)
        if second_sibling is not None:
            print(f"3) Second sibling        -> <{second_sibling.tag_name}> "
                  f"text = '{second_sibling.text}'")
        else:
            print("3) Second sibling        -> not found")

        href_parent = get_parent_of_href_element(driver)
        print(f"4) Parent of [href] tag  -> <{href_parent.tag_name}>")

        # ---- Axes ----
        ancestors = get_all_ancestors(target_element)
        print(f"\n5) Ancestor elements found        : {len(ancestors)}")

        following_siblings = get_all_following_siblings(target_element)
        print(f"6) Following-sibling elements found: {len(following_siblings)}")

        preceding_elements = get_all_preceding_elements(target_element)
        print(f"7) Preceding elements found        : {len(preceding_elements)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
