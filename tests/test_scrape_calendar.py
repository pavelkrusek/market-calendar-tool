from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from market_calendar_tool.api import scrape_calendar
from market_calendar_tool.scraper.base_scraper import Site
from market_calendar_tool.scraper.models import ScrapeOptions


@pytest.fixture
def mock_base_scraper(mocker):
    return mocker.patch("market_calendar_tool.api.BaseScraper")


@pytest.fixture
def mock_extended_scraper(mocker):
    return mocker.patch("market_calendar_tool.api.ExtendedScraper")


@pytest.fixture
def scrape_options():
    return ScrapeOptions(max_parallel_tasks=5)


@freeze_time("2024-10-19")
def test_scrape_calendar_default_dates(mock_base_scraper):
    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    scrape_calendar()

    mock_base_scraper.assert_called_with(Site.FOREXFACTORY, today, next_week)


def test_scrape_calendar_custom_date_range(mock_base_scraper):
    custom_from = "2024-11-01"
    custom_to = "2024-11-07"

    scrape_calendar(date_from=custom_from, date_to=custom_to)

    mock_base_scraper.assert_called_with(Site.FOREXFACTORY, custom_from, custom_to)


def test_scrape_calendar_invalid_date_from():
    with pytest.raises(ValueError) as exc_info:
        scrape_calendar(date_from="2024/10/19")

    assert "Date 2024/10/19 is not in the format YYYY-MM-DD" in str(exc_info.value)


def test_scrape_calendar_invalid_date_to():
    with pytest.raises(ValueError) as exc_info:
        scrape_calendar(date_to="19-10-2024")

    assert "Date 19-10-2024 is not in the format YYYY-MM-DD" in str(exc_info.value)


def test_scrape_calendar_date_to_earlier_than_date_from():
    with pytest.raises(ValueError) as exc_info:
        scrape_calendar(date_from="2024-10-20", date_to="2024-10-19")

    expected_message = "End date (date_to: 2024-10-19) cannot be earlier than start date (date_from: 2024-10-20)."
    assert expected_message in str(exc_info.value)


@freeze_time("2024-10-20")
def test_scrape_calendar_only_date_from(mock_base_scraper):
    custom_from = datetime.now().strftime("%Y-%m-%d")
    expected_to = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    scrape_calendar(date_from=custom_from)

    mock_base_scraper.assert_called_with(Site.FOREXFACTORY, custom_from, expected_to)


@freeze_time("2024-10-20")
def test_scrape_calendar_only_date_to(mock_base_scraper):
    custom_to = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    expected_from = datetime.now().strftime("%Y-%m-%d")

    scrape_calendar(date_to=custom_to)

    mock_base_scraper.assert_called_with(Site.FOREXFACTORY, expected_from, custom_to)


@freeze_time("2024-10-20")
def test_scrape_calendar_different_site(mock_base_scraper):
    alternative_site = Site.CRYPTOCRAFT

    scrape_calendar(site=alternative_site)

    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    mock_base_scraper.assert_called_with(alternative_site, today, next_week)


@freeze_time("2024-10-20")
def test_scrape_calendar_extended(mock_base_scraper, mock_extended_scraper):
    mock_extended_instance = MagicMock()
    mock_extended_scraper.return_value = mock_extended_instance

    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    scrape_calendar(extended=True)

    custom_options = ScrapeOptions(max_parallel_tasks=5)

    mock_base_scraper.assert_called_with(Site.FOREXFACTORY, today, next_week)
    mock_extended_scraper.assert_called_with(
        mock_base_scraper.return_value, options=custom_options
    )
    mock_extended_instance.scrape.assert_called_once()
