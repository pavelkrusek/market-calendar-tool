import requests
from loguru import logger

from .constants import Site, site_number_mapping
from .data_processor import DataProcessingError, DataProcessor


class BaseScraper:
    def __init__(self, site: Site, date_from: str, date_to: str):
        self.site = site
        self.date_from = date_from
        self.date_to = date_to
        self.base_url = site.value
        self.site_number = site_number_mapping.get(site, None)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "market-calendar-tool (+https://github.com/pavelkrusek/market-calendar-tool)",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def scrape(self):
        url = f"{self.base_url}/apply-settings/1"

        form_data = {
            "begin_date": self.date_from,
            "end_date": self.date_to,
        }

        try:
            response = self.session.post(
                url, json=form_data, headers=self.session.headers, timeout=10
            )
            response.raise_for_status()
            try:
                data = response.json()
                logger.info(f"Successfully scraped base data from {url}")
                return self._process_data(data)
            except requests.exceptions.JSONDecodeError as e:
                logger.critical(f"Error decoding JSON from {url}: {str(e)}")
                raise
        except requests.exceptions.RequestException as e:
            logger.critical(f"Error scraping base data: {str(e)}")
            raise

    def _process_data(self, data):
        try:
            processor = DataProcessor(data)
            df = processor.to_base_df()
            return df
        except DataProcessingError as e:
            logger.critical(f"Error processing data: {str(e)}")
            raise
