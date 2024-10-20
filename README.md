# Market Calendar Tool

A Python package for scraping economic calendar data from various financial websites.

## Legal notice

Please note that scraping data from websites must comply with the site's terms of service and legal requirements. The robots.txt files of the supported sites do not explicitly restrict scraping, but users should ensure they comply with local regulations and the website's terms.

## Features

- **Multi-Site Support**: Scrape data from multiple sites:
  - [ForexFactory](https://www.forexfactory.com/calendar)
  - [MetalsMine](https://www.metalsmine.com/calendar)
  - [EnergyExch](https://www.energyexch.com/calendar)
  - [CryptoCraft](https://www.cryptocraft.com/calendar)

- **Flexible Date Range**: Specify custom date ranges for scraping.
- **Extended Data Retrieval**: Option to retrieve extended data for each event.
- **Easy-to-Use API**: Simple and intuitive function to get you started quickly.
- **DataFrame Output**: Returns raw data scraped from the website as pandas DataFrame(s) for further processing.

## Installation

Install the package via pip:

```bash
pip install market-calendar-tool
```

## Requirements

- **Python Version**: Python **3.12** or higher is required.
- **Dependencies**:
  - The package relies on several libraries such as `loguru`, `requests`, `pandas`, `asyncio`, and `aiohttp`.
  - These libraries will be automatically installed when you install the package.

## Usage

Import the package and use the `scrape_calendar` function.

```python
from market_calendar_tool import scrape_calendar, Site, ScrapeResult

# Basic usage: scrape data from today to one week ahead from ForexFactory
df = scrape_calendar()

# Specify a different site
df = scrape_calendar(site=Site.METALSMINE)

# Specify date range
df = scrape_calendar(date_from="2023-01-01", date_to="2023-01-07")

# Retrieve extended data
result = scrape_calendar(extended=True)
print(result.base)     # Basic event data
print(result.specs)    # Event specifications
print(result.history)  # Historical data
print(result.news)     # Related news articles
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

## Return Values

- When `extended=False`: Returns a `pandas.DataFrame` containing basic event data.
- When `extended=True`: Returns a `ScrapeResult` object with the following attributes:
  - `base`: DataFrame with basic event data.
  - `specs`: DataFrame with event specifications.
  - `history`: DataFrame with historical data.
  - `news`: DataFrame with related news articles.

## API Reference

### `scrape_calendar`

Function to scrape calendar data.

**Signature:**

```python
def scrape_calendar(
    site: Site = Site.FOREXFACTORY,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    extended: bool = False,
) -> Union[pd.DataFrame, ScrapeResult]:
    ...
```

### `Site` Enum

Enumeration of supported websites.

- `Site.FOREXFACTORY`
- `Site.METALSMINE`
- `Site.ENERGYEXCH`
- `Site.CRYPTOCRAFT`

### `ScrapeResult` Data Class

Contains extended data when `extended=True`.

- `base`: Basic event data (`pd.DataFrame`)
- `specs`: Event specifications (`pd.DataFrame`)
- `history`: Historical data (`pd.DataFrame`)
- `news`: Related news articles (`pd.DataFrame`)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to customize this package to better suit your project's needs!
