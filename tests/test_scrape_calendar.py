from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from market_calendar_tool.api import scrape_calendar
from market_calendar_tool.scraper.base_scraper import BaseScraper, Site


@patch("market_calendar_tool.api.BaseScraper")
def test_scrape_calendar_default_dates(mock_base_scraper):
    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    scrape_calendar()

    mock_base_scraper.assert_called_with(Site.FOREXFACTORY, today, next_week)
