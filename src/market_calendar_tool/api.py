from datetime import datetime, timedelta

import pandas as pd

from .scraper import BaseScraper, ExtendedScraper, ScrapeResult, Site


def scrape_calendar(
    site: Site = Site.FOREXFACTORY,
    date_from: str = None,
    date_to: str = None,
    extended: bool = False,
) -> pd.DataFrame | ScrapeResult:
    """
    Scrape calendar data from the specified site.

    Args:
        site (Site): The site enumeration.
        date_from (str): The start date in 'YYYY-MM-DD' format.
        date_to (str): The end date in 'YYYY-MM-DD' format.
        extended (bool): Whether to scrape extended data.

    Returns:
        list: Scraped data.
    """

    def validate_and_format_date(date_str, default_date):
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Date {date_str} is not in the format YYYY-MM-DD")
        return default_date

    today = datetime.now()
    date_from = validate_and_format_date(date_from, today)
    date_to = validate_and_format_date(date_to, (today + timedelta(days=7)))

    if date_to < date_from:
        raise ValueError(
            f"End date (date_to: {date_to.strftime('%Y-%m-%d')}) cannot be earlier than start date (date_from: {date_from.strftime('%Y-%m-%d')})."
        )

    date_from = date_from.strftime("%Y-%m-%d")
    date_to = date_to.strftime("%Y-%m-%d")

    base_scraper = BaseScraper(site, date_from, date_to)
    if extended:
        return ExtendedScraper(base_scraper).scrape()
    else:
        return base_scraper.scrape()
