from unittest import mock
from unittest.mock import Mock

import pytest
import requests

from market_calendar_tool.scraper.base_scraper import BaseScraper
from market_calendar_tool.scraper.constants import Site, site_number_mapping
from market_calendar_tool.scraper.data_processor import DataProcessingError


@pytest.fixture
def scraper():
    return BaseScraper(
        site=Site.FOREXFACTORY, date_from="2024-01-01", date_to="2024-01-31"
    )


def test_initialization(scraper):
    assert scraper.site == Site.FOREXFACTORY
    assert scraper.date_from == "2024-01-01"
    assert scraper.date_to == "2024-01-31"
    assert scraper.base_url == Site.FOREXFACTORY.value
    assert scraper.site_number == site_number_mapping.get(Site.FOREXFACTORY)
    assert scraper.session.headers["Accept"] == "application/json"
    assert scraper.session.headers["Content-Type"] == "application/json"


def test_scrape_successful(scraper):
    with mock.patch.object(scraper.session, "post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        with mock.patch.object(
            scraper, "_process_data", return_value="processed_data"
        ) as mock_process:
            result = scraper.scrape()
            assert result == "processed_data"
            mock_process.assert_called_once_with({"data": "test_data"})

        expected_url = f"{scraper.base_url}/apply-settings/1"
        expected_data = {
            "begin_date": scraper.date_from,
            "end_date": scraper.date_to,
        }
        mock_post.assert_called_once_with(
            expected_url,
            json=expected_data,
            headers=scraper.session.headers,
            timeout=10,
        )


def test_scrape_json_decode_error(scraper):
    with mock.patch.object(scraper.session, "post") as mock_post:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "Expecting value", "", 0
        )
        mock_post.return_value = mock_response

        with mock.patch.object(scraper, "_process_data") as mock_process:
            with pytest.raises(requests.exceptions.JSONDecodeError):
                scraper.scrape()
            mock_process.assert_not_called()


def test_scrape_request_exception(scraper):
    with mock.patch.object(scraper.session, "post") as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        with mock.patch.object(scraper, "_process_data") as mock_process:
            with pytest.raises(requests.exceptions.RequestException):
                scraper.scrape()
            mock_process.assert_not_called()


def test_process_data_success(scraper):
    data = {"key": "value"}

    with mock.patch(
        "market_calendar_tool.scraper.base_scraper.DataProcessor"
    ) as MockDataProcessor:
        mock_processor_instance = MockDataProcessor.return_value
        mock_processor_instance.to_base_df.return_value = "processed_dataframe"

        result = scraper._process_data(data)
        assert result == "processed_dataframe"
        MockDataProcessor.assert_called_once_with(data)
        mock_processor_instance.to_base_df.assert_called_once()


def test_process_data_error(scraper):
    data = {"key": "value"}

    with mock.patch(
        "market_calendar_tool.scraper.base_scraper.DataProcessor"
    ) as MockDataProcessor:
        MockDataProcessor.side_effect = DataProcessingError("Processing error")

        with pytest.raises(DataProcessingError):
            scraper._process_data(data)
        MockDataProcessor.assert_called_once_with(data)
