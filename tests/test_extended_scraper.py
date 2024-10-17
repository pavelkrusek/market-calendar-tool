from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest

from market_calendar_tool.scraper.base_scraper import BaseScraper
from market_calendar_tool.scraper.constants import Site
from market_calendar_tool.scraper.extended_scraper import ExtendedScraper


@pytest.fixture
def mock_base_scraper():
    df = pd.DataFrame({"id": [1, 2]})

    with patch(
        "market_calendar_tool.scraper.base_scraper.BaseScraper", autospec=True
    ) as MockBaseScraper:
        mock_scraper = MockBaseScraper.return_value
        mock_scraper.scrape.return_value = df

        mock_scraper.site = Site.FOREXFACTORY
        mock_scraper.site_number = 1
        mock_scraper.session = MagicMock()
        mock_scraper.session.headers = {
            "User-Agent": "Scraper/0.1 (+pavel@krusek.dk)",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        yield mock_scraper


def test_extended_scraper_initialization(
    mock_base_scraper,
):
    extended_scraper = ExtendedScraper(base_scraper=mock_base_scraper)

    assert extended_scraper.base_scraper == mock_base_scraper


def test_extended_scraper_getattr(mock_base_scraper):
    extended_scraper = ExtendedScraper(base_scraper=mock_base_scraper)

    assert (
        extended_scraper.site == Site.FOREXFACTORY
    ), "Attribute 'site' should be delegated to base_scraper"

    assert (
        extended_scraper.site_number == 1
    ), "Attribute 'site_number' should be delegated to base_scraper"

    assert (
        extended_scraper.session.headers["User-Agent"]
        == "Scraper/0.1 (+pavel@krusek.dk)"
    ), "Header 'User-Agent' should be correctly delegated"
    assert (
        extended_scraper.session.headers["Accept"] == "application/json"
    ), "Header 'Accept' should be correctly delegated"
    assert (
        extended_scraper.session.headers["Content-Type"]
        == "application/x-www-form-urlencoded; charset=UTF-8"
    ), "Header 'Content-Type' should be correctly delegated"
