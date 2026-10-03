"""
config.py
Central configuration for the World Population Clock task.
"""
import os

# Page under test
BASE_URL = ("https://www.theworldcounts.com/challenges/planet-earth/"
            "state-of-the-planet/world-population-clock-live")
EXPECTED_TITLE_KEYWORD = "Population"

# Explicit wait timeouts (seconds)
PAGE_LOAD_WAIT = 30      # wait for the counter to appear on page load
COUNTER_CHANGE_WAIT = 10  # wait for the counter value to change

# Number of readings captured in the pytest run (the script itself runs until CTRL+C)
TEST_READINGS = 5

# Sanity limit: world population is above 7 billion
MINIMUM_EXPECTED_POPULATION = 7_000_000_000

# Run Chrome without a visible window if HEADLESS=true
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
