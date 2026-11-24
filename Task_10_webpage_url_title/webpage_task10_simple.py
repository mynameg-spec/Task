# Task - 10
#   1. Opens https://www.saucedemo.com/
#   2. Logs in using username and password
#   3. Prints the title of the page
#   4. Prints the current URL
#   5. Saves the full page content into a text file

# Step 1: Import the tools we need
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Step 2: Open the Chrome browser
driver = webdriver.Chrome()

# Step 3: Go to the website
driver.get("https://www.saucedemo.com/")

# Give the page a little time to load
time.sleep(2)

# Step 4: Find the username box and type the username
username_box = driver.find_element(By.ID, "user-name")
username_box.send_keys("standard_user")

# Step 5: Find the password box and type the password
password_box = driver.find_element(By.ID, "password")
password_box.send_keys("secret_sauce")

# Step 6: Find the login button and click it
login_button = driver.find_element(By.ID, "login-button")
login_button.click()

# Give the page a little time to load after login
time.sleep(2)

# Step 7: Get the title of the webpage
page_title = driver.title
print("Title of the webpage is:", page_title)

# Step 8: Get the current URL of the webpage
current_url = driver.current_url
print("Current URL of the webpage is:", current_url)

# Step 9: Get the entire content (HTML) of the webpage
page_content = driver.page_source

# Step 10: Save the content into a text file
file = open("Webpage_task_11.txt", "w", encoding="utf-8")
file.write(page_content)
file.close()

print("Webpage content saved successfully in Webpage_task_11.txt")

# Step 11: Close the browser
driver.quit()
