import pytest

from market_calendar_tool.scraper.base_scraper import BaseScraper
from market_calendar_tool.scraper.constants import Site, site_number_mapping


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
    assert (
        scraper.session.headers["Content-Type"]
        == "application/x-www-form-urlencoded; charset=UTF-8"
    )
