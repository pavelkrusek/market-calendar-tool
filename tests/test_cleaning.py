import pandas as pd
import pytest

from market_calendar_tool.cleaning.cleaner import (
    camel_to_snake,
    clean_base,
    clean_data,
    clean_history,
    clean_news,
    clean_specs,
    is_valid_currency,
)
from market_calendar_tool.scraper.models import ScrapeResult, Site


def test_is_valid_currency():
    assert is_valid_currency("USD")
    assert is_valid_currency("EUR")
    assert not is_valid_currency("ABC")
    assert is_valid_currency("all")
    assert not is_valid_currency("")
    assert not is_valid_currency(None)


def test_camel_to_snake():
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("CamelCaseTest") == "camel_case_test"
    assert camel_to_snake("test") == "test"
    assert camel_to_snake("TestHTTPResponse") == "test_http_response"
    assert camel_to_snake("") == ""
    assert camel_to_snake("aB") == "a_b"


@pytest.fixture
def sample_base_df():
    data = {
        "id": [135817, 139414, 142315],
        "name": ["Event1", "Event2", "Event3"],
        "currency": ["USD", "All", "EUR"],
        "dateline": [1729515300, 1729547100, 1729600200],
        "impactTitle": [
            "Low Impact Expected",
            "High Impact Expected",
            "Medium Impact Expected",
        ],
        "actual": [100, 200, 300],
        "previous": [90, 190, 290],
        "revision": [95, 195, 295],
        "forecast": [105, 205, 305],
        "actualBetterWorse": [0, 2, 1],
        "revisionBetterWorse": [0, 1, 2],
        "siteId": [1, 1, 1],
    }
    return pd.DataFrame(data)


def test_clean_base(sample_base_df):
    cleaned_df = clean_base(sample_base_df)

    expected_columns = [
        "id",
        "name",
        "currency",
        "datetime",
        "impact",
        "actual",
        "previous",
        "revision",
        "forecast",
        "actual_better_worse",
        "revision_better_worse",
        "site_id",
    ]
    assert list(cleaned_df.columns) == expected_columns

    assert cleaned_df.loc[1, "currency"] == "WORLD"

    assert cleaned_df.loc[0, "impact"] == "low"
    assert cleaned_df.loc[1, "impact"] == "high"
    assert cleaned_df.loc[2, "impact"] == "medium"

    assert cleaned_df.loc[0, "datetime"] == pd.Timestamp(
        "2024-10-21 12:55:00+0000", tz="UTC"
    )
    assert cleaned_df.loc[1, "datetime"] == pd.Timestamp(
        "2024-10-21 21:45:00+0000", tz="UTC"
    )
    assert cleaned_df.loc[2, "datetime"] == pd.Timestamp(
        "2024-10-22 12:30:00+0000", tz="UTC"
    )


@pytest.fixture
def sample_specs_df():
    data = {
        "order": [10, 20],
        "title": ["Spec1", "Spec2"],
        "html": [
            '<a href="/calendar?day=nov18.2024#detail=135818">Nov 18, 2024</a>',
            '<a rel="nofollow noopener" target="_blank" href="https://www.rba.gov.au/">Reserve Bank of Australia</a> (<a rel="nofollow noopener" target="_blank" href="https://www.rba.gov.au/speeches/list.html">latest release</a>)',
        ],
        "is_notice": [None, "Yes"],
        "id": [135817, 135817],
    }
    return pd.DataFrame(data)


def test_clean_specs(sample_specs_df):
    cleaned_specs_df = clean_specs(sample_specs_df)

    expected_columns = ["order", "title", "description", "id"]
    assert list(cleaned_specs_df.columns) == expected_columns

    assert "is_notice" not in cleaned_specs_df.columns

    expected_descriptions = [
        "Nov 18, 2024 (/calendar?day=nov18.2024#detail=135818)",
        "Reserve Bank of Australia (https://www.rba.gov.au/) ( latest release (https://www.rba.gov.au/speeches/list.html) )",
    ]
    assert list(cleaned_specs_df["description"]) == expected_descriptions


@pytest.fixture
def sample_history_df():
    data = {
        "event_id": [135816, 135815, 141725],
        "impact": ["low", "low", "low"],
        "impact_class": [
            "icon--ff-impact-yel",
            "icon--ff-impact-yel",
            "icon--ff-impact-yel",
        ],
        "date": ["Sep 16, 2024", "Aug 19, 2024", "Oct 8, 2024"],
        "url": [
            "/calendar?day=sep16.2024#detail=135816",
            "/calendar?day=aug19.2024#detail=135815",
            "/calendar?day=oct8.2024#detail=141725",
        ],
        "actual": ["0.8%", "-1.5%", ""],
        "previous": ["-1.5%", "-0.4%", ""],
        "revision": ["", "", ""],
        "forecast": ["", "", ""],
        "actualBetterWorse": [0.0, 0.0, ""],
        "revisionBetterWorse": [0.0, 0.0, ""],
        "description": [
            "",
            "",
            "Due to speak at the Walkley Foundation, in Sydney. Audience questions expected;",
        ],
        "id": [135817, 135817, 1],
    }
    return pd.DataFrame(data)


def test_clean_history(sample_history_df):
    cleaned_history_df = clean_history(sample_history_df)

    expected_columns = [
        "event_id",
        "impact",
        "date",
        "url",
        "actual",
        "previous",
        "revision",
        "forecast",
        "actual_better_worse",
        "revision_better_worse",
        "description",
        "id",
    ]
    assert list(cleaned_history_df.columns) == expected_columns

    assert "impact_class" not in cleaned_history_df.columns

    expected_dates = [
        pd.Timestamp("2024-09-16 00:00:00+0000", tz="UTC"),
        pd.Timestamp("2024-08-19 00:00:00+0000", tz="UTC"),
        pd.Timestamp("2024-10-08 00:00:00+0000", tz="UTC"),
    ]
    assert list(cleaned_history_df["date"]) == expected_dates


@pytest.fixture
def sample_news_df():
    data = {
        "news_id": [1309993],
        "html": [
            """
            <div>
                <div class="flexposts__story-title">
                    <a href="/news/1309993-number-of-homes-sold-in-uk-up-by"
                    title="Number of homes sold in UK up by a third, says Rightmove">
                        Number of homes sold in UK up by a third, says Rightmove
                    </a>
                </div>
                <div class="flexposts__storydisplay-info">
                    <span class="flexposts__caption">
                        <a href="/news/1309993-number-of-homes-sold-in-uk-up-by/hit" target="_blank" rel="nofollow">
                            From theguardian.com
                        </a>
                        <span>| Oct 21, 2024</span>
                    </span>
                    <p class="flexposts__preview">The number of homes being sold is up almost a third, year on year...</p>
                </div>
            </div>
            """
        ],
        "id": [135817],
    }
    return pd.DataFrame(data)


def test_clean_news(sample_news_df):
    cleaned_news_df = clean_news(sample_news_df)

    expected_columns = ["news_id", "text", "id"]
    assert list(cleaned_news_df.columns) == expected_columns

    expected_text_start = "Number of homes sold in UK up by a third, says Rightmove"

    assert cleaned_news_df["text"].iloc[0].startswith(expected_text_start)


@pytest.fixture
def sample_scrape_result(
    sample_base_df, sample_specs_df, sample_history_df, sample_news_df
):
    return ScrapeResult(
        site=Site.FOREXFACTORY,
        date_from="",
        date_to="",
        base=sample_base_df,
        specs=sample_specs_df,
        history=sample_history_df,
        news=sample_news_df,
    )


def test_clean_data(sample_scrape_result):
    cleaned = clean_data(sample_scrape_result)

    assert isinstance(cleaned, ScrapeResult)
    assert "base" in cleaned.__dataclass_fields__
    assert "specs" in cleaned.__dataclass_fields__
    assert "history" in cleaned.__dataclass_fields__
    assert "news" in cleaned.__dataclass_fields__

    cleaned_base = cleaned.base
    assert cleaned_base.shape[0] == 3

    cleaned_specs = cleaned.specs
    assert cleaned_specs.shape[0] == 2

    cleaned_history = cleaned.history
    assert cleaned_history.shape[0] == 2

    cleaned_news = cleaned.news
    assert cleaned_news.shape[0] == 1


def test_clean_data_with_empty_dfs(sample_base_df):
    scrape_result = ScrapeResult(
        site=Site.FOREXFACTORY, date_from="", date_to="", base=sample_base_df
    )

    cleaned = clean_data(scrape_result)

    assert isinstance(cleaned, ScrapeResult)

    assert "base" in cleaned.__dataclass_fields__
    assert "specs" in cleaned.__dataclass_fields__
    assert "history" in cleaned.__dataclass_fields__
    assert "news" in cleaned.__dataclass_fields__

    cleaned_base = cleaned.base
    expected_columns = [
        "id",
        "name",
        "currency",
        "datetime",
        "impact",
        "actual",
        "previous",
        "revision",
        "forecast",
        "actual_better_worse",
        "revision_better_worse",
        "site_id",
    ]
    assert list(cleaned_base.columns) == expected_columns

    assert cleaned.specs.empty, "Specs DataFrame should be empty"
    assert cleaned.history.empty, "History DataFrame should be empty"
    assert cleaned.news.empty, "News DataFrame should be empty"
