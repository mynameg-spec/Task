# We check 3 things, each with one POSITIVE test and one NEGATIVE test:
#   1. Title of the webpage
#   2. URL of the homepage
#   3. URL after login (dashboard page)

# To run this file and create an HTML report, use this command:
# pytest test_saucedemo_simple.py --html=report.html --self-contained-html -v

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# The details we expect
homepage_url = "https://www.saucedemo.com/"
expected_title = "Swag Labs"
dashboard_url = "https://www.saucedemo.com/inventory.html"


# ---------- TEST 1: Title of the webpage ----------

def test_title_positive():
    # POSITIVE CASE: title should match "Swag Labs"
    driver = webdriver.Chrome()
    driver.get(homepage_url)
    time.sleep(2)

    assert driver.title == expected_title

    driver.quit()


def test_title_negative():
    # NEGATIVE CASE: title should NOT match a wrong value
    driver = webdriver.Chrome()
    driver.get(homepage_url)
    time.sleep(2)

    assert driver.title != "Wrong Title"

    driver.quit()


# ---------- TEST 2: URL of the homepage ----------

def test_homepage_url_positive():
    # POSITIVE CASE: URL should match the homepage URL
    driver = webdriver.Chrome()
    driver.get(homepage_url)
    time.sleep(2)

    assert driver.current_url == homepage_url

    driver.quit()


def test_homepage_url_negative():
    # NEGATIVE CASE: homepage URL should NOT be the dashboard URL
    driver = webdriver.Chrome()
    driver.get(homepage_url)
    time.sleep(2)

    assert driver.current_url != dashboard_url

    driver.quit()


# ---------- TEST 3: URL after login (dashboard) ----------

def test_dashboard_url_positive():
    # POSITIVE CASE: after correct login, URL should change to dashboard URL
    driver = webdriver.Chrome()
    driver.get(homepage_url)
    time.sleep(2)

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    assert driver.current_url == dashboard_url

    driver.quit()


def test_dashboard_url_negative():
    # NEGATIVE CASE: wrong login should NOT reach the dashboard URL
    driver = webdriver.Chrome()
    driver.get(homepage_url)
    time.sleep(2)

    driver.find_element(By.ID, "user-name").send_keys("wrong_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    assert driver.current_url != dashboard_url

    driver.quit()
