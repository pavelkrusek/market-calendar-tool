from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from market_calendar_tool.scraper.extended_scraper import ExtendedScraper, ScrapeResult
from market_calendar_tool.scraper.models import ScrapeOptions, Site


@pytest.fixture
def mock_base_scraper():
    df = pd.DataFrame({"id": [1, 2]})

    with patch(
        "market_calendar_tool.scraper.base_scraper.BaseScraper", autospec=True
    ) as MockBaseScraper:
        mock_scraper = MockBaseScraper.return_value
        mock_scraper.scrape.return_value = ScrapeResult(
            site=Site.FOREXFACTORY, date_from="", date_to="", base=df
        )

        mock_scraper.site = Site.FOREXFACTORY
        mock_scraper.site_number = 1
        mock_scraper.session = MagicMock()
        mock_scraper.session.headers = {
            "User-Agent": "market-calendar-tool (+https://github.com/pavelkrusek/market-calendar-tool)",
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        yield mock_scraper


@pytest.fixture
def mock_data_processor():
    with patch(
        "market_calendar_tool.scraper.extended_scraper.DataProcessor", autospec=True
    ) as MockDataProcessor:
        mock_processor = MockDataProcessor.return_value
        mock_processor.to_specs_df.return_value = pd.DataFrame({"specs": [1, 2]})
        mock_processor.to_history_df.return_value = pd.DataFrame({"history": [3, 4]})
        mock_processor.to_news_df.return_value = pd.DataFrame({"news": [5, 6]})
        yield mock_processor


def test_extended_scraper_initialization(
    mock_base_scraper,
):
    extended_scraper = ExtendedScraper(
        base_scraper=mock_base_scraper, options=ScrapeOptions(max_parallel_tasks=1)
    )

    assert extended_scraper.base_scraper == mock_base_scraper


def test_extended_scraper_getattr(mock_base_scraper):
    extended_scraper = ExtendedScraper(
        base_scraper=mock_base_scraper, options=ScrapeOptions(max_parallel_tasks=1)
    )

    assert (
        extended_scraper.site == Site.FOREXFACTORY
    ), "Attribute 'site' should be delegated to base_scraper"

    assert (
        extended_scraper.site_number == 1
    ), "Attribute 'site_number' should be delegated to base_scraper"

    assert (
        extended_scraper.session.headers["User-Agent"]
        == "market-calendar-tool (+https://github.com/pavelkrusek/market-calendar-tool)"
    ), "Header 'User-Agent' should be correctly delegated"
    assert (
        extended_scraper.session.headers["Accept"] == "application/json"
    ), "Header 'Accept' should be correctly delegated"
    assert (
        extended_scraper.session.headers["Content-Type"]
        == "application/x-www-form-urlencoded; charset=UTF-8"
    ), "Header 'Content-Type' should be correctly delegated"


@pytest.mark.asyncio
async def test_async_scrape(mock_base_scraper, mock_data_processor):
    extended_scraper = ExtendedScraper(
        base_scraper=mock_base_scraper, options=ScrapeOptions(max_parallel_tasks=1)
    )

    async def mock_get(url, headers):
        class MockResponse:
            async def json(self):
                return {"data": "mocked"}

            def raise_for_status(self):
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

        return MockResponse()

    with patch("aiohttp.ClientSession.get", new=mock_get):
        result = await extended_scraper._async_scrape()

    assert isinstance(result, ScrapeResult)
    assert not result.base.empty
    assert not result.specs.empty
    assert not result.history.empty
    assert not result.news.empty

    assert result.specs.equals(mock_data_processor.to_specs_df.return_value)
    assert result.history.equals(mock_data_processor.to_history_df.return_value)
    assert result.news.equals(mock_data_processor.to_news_df.return_value)
