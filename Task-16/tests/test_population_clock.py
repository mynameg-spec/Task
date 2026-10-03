"""
test_population_clock.py
Pytest test cases for the World Population Clock (Task 16).
"""
from population_clock import stream_population_count
from utils.config import EXPECTED_TITLE_KEYWORD, MINIMUM_EXPECTED_POPULATION, TEST_READINGS


class TestPopulationClock:
    """Tests for extracting the live world population count."""

    def test_page_opens_with_correct_title(self, population_page):
        """The page should load and the title should mention Population."""
        assert EXPECTED_TITLE_KEYWORD in population_page.get_page_title()

    def test_population_counter_is_displayed(self, population_page):
        """The 'World population' heading and its counter should be visible."""
        assert population_page.is_population_title_displayed(), "Population title not visible"
        assert population_page.is_population_counter_displayed(), "Population counter not visible"

    def test_population_count_is_valid_number(self, population_page):
        """The counter should be a number greater than 7 billion."""
        population = population_page.get_population_count()
        print(f"Population extracted: {population:,}")
        assert population > MINIMUM_EXPECTED_POPULATION, f"Unexpected population value: {population}"

    def test_population_count_is_increasing(self, population_page):
        """The counter is live, so the next value should be higher than the first."""
        first_text = population_page.get_population_text()
        next_text = population_page.wait_for_population_change(first_text)

        assert next_text is not None, "Population counter did not update"
        assert population_page.convert_to_number(next_text) > population_page.convert_to_number(first_text)

    def test_extract_live_population_readings(self, population_page):
        """Extract several live readings and print them on the console."""
        readings = stream_population_count(population_page, max_readings=TEST_READINGS)

        assert len(readings) == TEST_READINGS, "Did not capture the expected number of readings"
        assert readings == sorted(readings), "Population readings should never decrease"

    def test_extraction_stops_on_ctrl_c(self, population_page, monkeypatch):
        """Simulate CTRL+C and check the extraction stops gracefully without an error."""
        original_wait = population_page.wait_for_population_change
        calls = {"count": 0}

        def wait_then_press_ctrl_c(old_text):
            calls["count"] += 1
            if calls["count"] == 3:
                raise KeyboardInterrupt  # Same exception Python raises on CTRL+C
            return original_wait(old_text)

        monkeypatch.setattr(population_page, "wait_for_population_change", wait_then_press_ctrl_c)
        readings = stream_population_count(population_page)  # No limit: runs until CTRL+C

        assert len(readings) == 3, "Extraction should stop right after CTRL+C"
