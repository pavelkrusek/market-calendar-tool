# Market Calendar Tool

A Python package for scraping economic calendar data from various financial websites.

## Legal Notice

Please note that scraping data from websites must comply with the site's terms of service and legal requirements. The robots.txt files of the supported sites do not explicitly restrict scraping, but users should ensure they comply with local regulations and the website's terms.

## Features

- **Multi-Site Support**: Scrape data from multiple sites:
  - [ForexFactory](https://www.forexfactory.com/calendar)
  - [MetalsMine](https://www.metalsmine.com/calendar)
  - [EnergyExch](https://www.energyexch.com/calendar)
  - [CryptoCraft](https://www.cryptocraft.com/calendar)

- **Flexible Date Range**: Specify custom date ranges for scraping.
- **Extended Data Retrieval**: Option to retrieve extended data for each event.
- **Configurable Concurrency**: Use `ScrapeOptions` to configure the number of concurrent asyncio tasks (`max_parallel_tasks`), optimizing scraping performance based on system capabilities.
- **Easy-to-Use API**: Simple and intuitive function to get you started quickly.
- **DataFrame Output**: Returns raw data scraped from the website as *pandas* DataFrame(s) for further processing.
- **Data Handling**: Always returns scraped data encapsulated in a `ScrapeResult` object for consistent data management.
- **Data Cleaning and Validation**: Provides functionality to clean and validate scraped data for further processing, ensuring data quality and consistency.

## Installation

Install the package via pip:

```bash
pip install market-calendar-tool
```

## Requirements

- **Python Version**: Python **3.12** or higher is required.
- **Dependencies**:

| Dependency | Version |
|------------|---------|
| loguru     | ^0.7.2  |
| requests   | ^2.32.3 |
| pandas     | ^2.2.3  |
| asyncio    | ^3.4.3  |
| aiohttp    | ^3.10.10 |
| pycountry  | ^24.6.1 |
| beautifulsoup4 | ^4.12.3 |

## Usage

Import the package and use the `scrape_calendar` function with optional `ScrapeOptions` for advanced configurations.

```python
from market_calendar_tool import scrape_calendar, clean_calendar_data, Site, ScrapeOptions

# Stage 1: Scrape raw data from today to one week ahead from ForexFactory
raw_data = scrape_calendar()

# Stage 2: Clean the data
cleaned_data = clean_calendar_data(raw_data)

# Specify a different site
raw_data = scrape_calendar(site=Site.METALSMINE)
cleaned_data = clean_calendar_data(raw_data)

# Specify date range
raw_data = scrape_calendar(date_from="2024-01-01", date_to="2024-01-07")
cleaned_data = clean_calendar_data(raw_data)

# Retrieve extended data
result = scrape_calendar(extended=True)
print(result.base)     # Basic event data
print(result.specs)    # Event specifications
print(result.history)  # Historical data
print(result.news)     # Related news articles

# Advanced usage: configure asyncio task concurrency
custom_options = ScrapeOptions(max_parallel_tasks=10)
raw_data = scrape_calendar(options=custom_options)
cleaned_data = clean_calendar_data(raw_data)
```

## Parameters

- `site` (optional): The website to scrape data from. Default is `Site.FOREXFACTORY`.
  - Options:
    - `Site.FOREXFACTORY`
    - `Site.METALSMINE`
    - `Site.ENERGYEXCH`
    - `Site.CRYPTOCRAFT`
- `date_from` (optional): Start date in "YYYY-MM-DD" format.
- `date_to` (optional): End date in "YYYY-MM-DD" format.
- `extended` (optional): Boolean flag to retrieve extended data. Default is `False`.
- `options` (optional): An instance of `ScrapeOptions` to configure advanced scraping settings.

## Return Values

`scrape_calendar`: Always returns a `ScrapeResult` object containing the raw scraped data.
`clean_calendar_data`: Returns a `ScrapeResult` object containing the cleaned data.

## API Reference

### `scrape_calendar`

Function to scrape raw calendar data from the specified site within the given date range.

**Signature:**

```python
def scrape_calendar(
    site: Site = Site.FOREXFACTORY,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    extended: bool = False,
    options: Optional[ScrapeOptions] = None,
) -> ScrapeResult:
    ...
```

**Parameters**:

- `site` (Site): The target site to scrape. Defaults to `Site.FOREXFACTORY`.
- `date_from` (Optional[str]): The start date for scraping in 'YYYY-MM-DD' format.
- `date_to` (Optional[str]): The end date for scraping in 'YYYY-MM-DD' format.
- `extended` (bool): Whether to perform extended scraping. Defaults to `False`.
- `options` (Optional[ScrapeOptions]): Additional scraping configurations.

**Returns**:

- `ScrapeResult`: The raw scraped data encapsulated in a ScrapeResult object.

### `clean_calendar_data`

Function to clean the scraped calendar data.

**Signature**:

```python
def clean_calendar_data(scrape_result: ScrapeResult) -> ScrapeResult:
    ...
```

**Parameters**:

- `scrape_result` (`ScrapeResult`): The raw scraped data to be cleaned.

**Returns**:

- `ScrapeResult`: The cleaned data encapsulated in a `ScrapeResult` object.

### `Site` Enum

Enumeration of supported websites.

- `Site.FOREXFACTORY`
- `Site.METALSMINE`
- `Site.ENERGYEXCH`
- `Site.CRYPTOCRAFT`

### `ScrapeOptions` Data Class

Contains configurable options for scraping.

**Attributes**:

- `max_parallel_tasks` (`int`): The maximum number of concurrent asyncio tasks. Default is `5`.

**Example**:

```python
from market_calendar_tool import ScrapeOptions

# Create custom options with increased concurrency
custom_options = ScrapeOptions(max_parallel_tasks=10)
```

### `ScrapeResult` Data Class

Contains extended data when `extended=True`.

- `base` (`pd.DataFrame`): Basic event data.
- `specs` (`pd.DataFrame`): Event specifications.
- `history` (`pd.DataFrame`): Historical data.
- `news` (`pd.DataFrame`): Related news articles.

## Configuration

### `ScrapeOptions`

The `ScrapeOptions` dataclass allows you to configure advanced scraping settings.

**Parameters**:

- `max_parallel_tasks` (`int`, `optional`): The number of concurrent asyncio tasks to run. Increasing this number can speed up the scraping process but may lead to higher resource usage. Default is `5`.

**Usage Example**:

```python
from market_calendar_tool import scrape_calendar, ScrapeOptions

# Configure scraper to use 10 parallel asyncio tasks
options = ScrapeOptions(max_parallel_tasks=10)
result = scrape_calendar(extended=True, options=options)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to customize this package to better suit your project's needs!
