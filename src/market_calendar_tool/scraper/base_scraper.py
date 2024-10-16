import requests
from loguru import logger

from .constants import Site, site_number_mapping
from .data_processor import DataProcessingError, DataProcessor


class BaseScraper:
    """
    A base scraper class for performing synchronous AJAX POST requests to fetch base calendar data.
    """

    def __init__(self, site: Site, date_from: str, date_to: str):
        """
        Initialize the BaseScraper with site and date range.

        Args:
            site (Site): The site enumeration for the scraper.
            date_from (str): The start date in 'YYYY-MM-DD' format.
            date_to (str): The end date in 'YYYY-MM-DD' format.
        """
        self.site = site
        self.date_from = date_from
        self.date_to = date_to
        self.base_url = site.value
        self.site_number = site_number_mapping.get(site, None)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Scraper/0.1 (+pavel@krusek.dk)",
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
        )

    def scrape(self):
        """
        Scrape base data by performing a synchronous AJAX POST request.

        Returns:
            dict: The scraped data parsed from JSON.
        """
        url = f"{self.base_url}/apply-settings/1"

        form_data = {
            "begin_date": self.date_from,
            "end_date": self.date_from,
        }

        try:
            response = self.session.post(
                url, data=form_data, headers=self.session.headers, timeout=10
            )
            response.raise_for_status()
            try:
                data = response.json()
                logger.info("Successfully scraped base data from", url)
                return self._process_data(data)
            except requests.exceptions.JSONDecodeError as e:
                logger.critical("Error decoding JSON from %s: %s", url, str(e))
                raise
        except requests.exceptions.RequestException as e:
            logger.critical("Error scraping base data: %s", str(e))
            raise

    def _process_data(self, data):
        """
        Process the raw JSON data and convert it into a pandas DataFrame.
        """
        try:
            processor = DataProcessor(data)
            df = processor.to_df()
            return df
        except DataProcessingError as e:
            logger.critical("Error processing data: %s", str(e))
            raise
