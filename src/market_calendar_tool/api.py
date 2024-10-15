# import asyncio

from .scraper import BaseScraper, Site


def scrape_calendar(site: Site, date_from: str, date_to: str, extended: bool = False):
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
    base_scraper = BaseScraper(site, date_from, date_to)
    return base_scraper.scrape()
    # if extended:
    #     extended_scraper = ExtendedScraper(base_scraper)
    #     return asyncio.run(extended_scraper.scrape())
    # else:
    #     return base_scraper.scrape()
