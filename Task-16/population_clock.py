"""
population_clock.py
Main script for Task 16.

Opens the World Population Clock and keeps printing the live population
count on the console until the user presses CTRL+C.

Run:  python population_clock.py
"""
from datetime import datetime

from selenium.common.exceptions import WebDriverException, TimeoutException

from pages.population_page import PopulationPage
from utils.driver_factory import create_chrome_driver


def stream_population_count(population_page, max_readings=None):
    """
    Print the population count every time it changes.

    max_readings=None  -> run forever (until CTRL+C)
    max_readings=5     -> stop after 5 readings (used by pytest)

    Returns the list of population values that were printed.
    """
    readings = []

    try:
        current_text = population_page.get_population_text()
        while max_readings is None or len(readings) < max_readings:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] World Population: {current_text}", flush=True)
            readings.append(population_page.convert_to_number(current_text))

            # Explicit wait for the next update instead of sleep()
            new_text = population_page.wait_for_population_change(current_text)
            if new_text is not None:
                current_text = new_text
    except KeyboardInterrupt:
        print("\nCTRL+C pressed. Stopping population tracking.")

    return readings


def main():
    """Start the browser, stream the population count and always close the browser."""
    driver = None
    try:
        driver = create_chrome_driver()
        population_page = PopulationPage(driver)
        population_page.load()
        print("Live World Population (press CTRL+C to stop)\n")
        stream_population_count(population_page)
    except KeyboardInterrupt:
        print("\nCTRL+C pressed before tracking started.")
    except (TimeoutException, WebDriverException) as error:
        print(f"Browser error: {error}")
    finally:
        close_browser(driver)


def close_browser(driver):
    """
    Quit the browser safely. On CTRL+C the terminal may also stop the chromedriver
    process, so quit() can fail - that should not show a traceback to the user.
    """
    if driver is None:
        return
    try:
        driver.quit()
        print("Browser closed.")
    except (KeyboardInterrupt, Exception):  # noqa: BLE001 - shutdown must never crash
        print("Browser was already closed.")


if __name__ == "__main__":
    main()
