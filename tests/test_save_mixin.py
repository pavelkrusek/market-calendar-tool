import os
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from market_calendar_tool.mixins.save_mixin import SaveFormat
from market_calendar_tool.scraper.models import ScrapeResult, Site


@pytest.fixture
def scrape_result():
    return ScrapeResult(
        site=Site.CRYPTOCRAFT,
        date_from="2024-10-21",
        date_to="2024-10-22",
        base=pd.DataFrame({"data": [1, 2, 3]}),
        specs=pd.DataFrame(),
        history=pd.DataFrame({"history": ["H1", "H2"]}),
        news=pd.DataFrame(),
    )


def test_site_prefix():
    assert Site.FOREXFACTORY.prefix == "forexfactory"
    assert Site.METALSMINE.prefix == "metalsmine"
    assert Site.ENERGYEXCH.prefix == "energyexch"
    assert Site.CRYPTOCRAFT.prefix == "cryptocraft"


@patch("os.path.exists")
@patch("os.makedirs")
@patch.object(pd.DataFrame, "to_parquet")
@patch.object(pd.DataFrame, "to_csv")
def test_save_skips_empty_dataframes(
    mock_to_csv, mock_to_parquet, mock_makedirs, mock_exists, scrape_result, tmp_path
):
    mock_exists.return_value = True
    scrape_result.save_to_dataframes(
        save_format=SaveFormat.PARQUET, output_dir=str(tmp_path)
    )

    assert mock_to_parquet.call_count == 2
    mock_to_parquet.assert_any_call(
        os.path.join(
            str(tmp_path),
            f"{scrape_result.site.prefix}__{scrape_result.date_from}_{scrape_result.date_to}_{datetime.fromtimestamp(scrape_result.scraped_at).strftime('%Y%m%d%H%M%S')}_base.parquet",
        ),
        index=False,
    )
    mock_to_parquet.assert_any_call(
        os.path.join(
            str(tmp_path),
            f"{scrape_result.site.prefix}__{scrape_result.date_from}_{scrape_result.date_to}_{datetime.fromtimestamp(scrape_result.scraped_at).strftime('%Y%m%d%H%M%S')}_history.parquet",
        ),
        index=False,
    )

    mock_to_csv.assert_not_called()


@patch("os.path.exists")
@patch("os.makedirs")
@patch.object(pd.DataFrame, "to_parquet")
@patch.object(pd.DataFrame, "to_csv")
def test_save_correct_file_extensions(
    mock_to_csv, mock_to_parquet, mock_makedirs, mock_exists, scrape_result, tmp_path
):
    mock_exists.return_value = True

    scrape_result.save_to_dataframes(
        save_format=SaveFormat.CSV, output_dir=str(tmp_path)
    )

    assert mock_to_csv.call_count == 2
    mock_to_csv.assert_any_call(
        os.path.join(
            str(tmp_path),
            f"{scrape_result.site.prefix}__{scrape_result.date_from}_{scrape_result.date_to}_{datetime.fromtimestamp(scrape_result.scraped_at).strftime('%Y%m%d%H%M%S')}_base.csv",
        ),
        index=False,
    )
    mock_to_csv.assert_any_call(
        os.path.join(
            str(tmp_path),
            f"{scrape_result.site.prefix}__{scrape_result.date_from}_{scrape_result.date_to}_{datetime.fromtimestamp(scrape_result.scraped_at).strftime('%Y%m%d%H%M%S')}_history.csv",
        ),
        index=False,
    )

    mock_to_parquet.assert_not_called()


@patch("os.path.exists")
@patch("os.makedirs")
@patch.object(pd.DataFrame, "to_parquet")
@patch.object(pd.DataFrame, "to_csv")
def test_save_creates_output_dir_if_not_exists(
    mock_to_csv, mock_to_parquet, mock_makedirs, mock_exists, scrape_result, tmp_path
):
    mock_exists.return_value = False

    scrape_result.save_to_dataframes(
        save_format=SaveFormat.PARQUET, output_dir=str(tmp_path)
    )

    mock_makedirs.assert_called_once_with(str(tmp_path))

    assert mock_to_parquet.call_count == 2
    mock_to_parquet.assert_any_call(
        os.path.join(
            str(tmp_path),
            f"{scrape_result.site.prefix}__{scrape_result.date_from}_{scrape_result.date_to}_{datetime.fromtimestamp(scrape_result.scraped_at).strftime('%Y%m%d%H%M%S')}_base.parquet",
        ),
        index=False,
    )
    mock_to_parquet.assert_any_call(
        os.path.join(
            str(tmp_path),
            f"{scrape_result.site.prefix}__{scrape_result.date_from}_{scrape_result.date_to}_{datetime.fromtimestamp(scrape_result.scraped_at).strftime('%Y%m%d%H%M%S')}_history.parquet",
        ),
        index=False,
    )

    mock_to_csv.assert_not_called()
