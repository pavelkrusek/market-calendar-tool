import re
from enum import Enum
from functools import wraps
from typing import Optional

import pandas as pd
import pycountry
from bs4 import BeautifulSoup
from loguru import logger

from market_calendar_tool.scraper.extended_scraper import ScrapeResult


class ImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    NON_ECONOMIC = "non-economic"


impact_mapping = {
    "Low Impact Expected": ImpactLevel.LOW.value,
    "Medium Impact Expected": ImpactLevel.MEDIUM.value,
    "High Impact Expected": ImpactLevel.HIGH.value,
    "Non-Economic": ImpactLevel.NON_ECONOMIC.value,
}


def handle_empty(func):
    @wraps(func)
    def wrapper(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            logger.debug(
                f"{func.__name__} received an empty DataFrame; skipping cleaning."
            )
            return df
        return func(df)

    return wrapper


def is_valid_currency(currency: Optional[str]) -> bool:
    if currency is None:
        return False
    try:
        return pycountry.currencies.get(alpha_3=currency.upper()) is not None
    except Exception as e:
        logger.error(f"Error in is_valid_currency: {e}")
        return False


def camel_to_snake(name: str) -> str:
    return re.sub(
        r"([A-Z]+)([A-Z][a-z])", r"\1_\2", re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    ).lower()


def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for a in soup.find_all("a"):
        text = a.get_text()
        href = a.get("href", "")
        replacement = f"{text} ({href})" if href else text
        a.replace_with(replacement)

    return soup.get_text(separator=" ", strip=True)


def clean_data(scrape_result: ScrapeResult) -> ScrapeResult:
    cleaned_base = clean_base(scrape_result.base)

    valid_ids = set(cleaned_base["id"])

    cleaned_specs = clean_specs(scrape_result.specs)
    if not cleaned_specs.empty:
        cleaned_specs = cleaned_specs[cleaned_specs["id"].isin(valid_ids)]

    cleaned_history = clean_history(scrape_result.history)
    if not cleaned_history.empty:
        cleaned_history = cleaned_history[cleaned_history["id"].isin(valid_ids)]

    cleaned_news = clean_news(scrape_result.news)
    if not cleaned_history.empty:
        cleaned_news = cleaned_news[cleaned_news["id"].isin(valid_ids)]

    return ScrapeResult(
        base=cleaned_base,
        specs=cleaned_specs,
        history=cleaned_history,
        news=cleaned_news,
    )


def clean_base(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_validate = ["currency", "dateline", "impactTitle"]
    df = df.rename(columns={col: f"{col}_raw" for col in columns_to_validate})

    df["datetime"] = pd.to_datetime(
        df["dateline_raw"], unit="s", utc=True, errors="coerce"
    )

    df["impact"] = df["impactTitle_raw"].map(impact_mapping)

    df = df.dropna(subset=["datetime"])
    df = df.dropna(subset=["impact"])

    if "currency_raw" in df.columns:
        df["currency"] = df["currency_raw"].where(
            df["currency_raw"].apply(is_valid_currency)
        )
        df = df.dropna(subset=["currency"])

    df = df.drop(columns=[f"{col}_raw" for col in columns_to_validate])

    columns_to_keep = [
        "id",
        "name",
        "currency",
        "datetime",
        "impact",
        "actual",
        "previous",
        "revision",
        "forecast",
        "actualBetterWorse",
        "revisionBetterWorse",
        "siteId",
    ]
    df["currency"] = df["currency"].replace("All", "WORLD")
    df = df[columns_to_keep]
    df = df.rename(columns=lambda col: camel_to_snake(col))

    return df


@handle_empty
def clean_specs(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=["is_notice"]).rename(columns={"html": "description"})
    df["description"] = df["description"].apply(clean_html)
    return df


@handle_empty
def clean_history(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=["impact_class"])
    df = df.rename(columns=lambda col: camel_to_snake(col))
    df["date"] = pd.to_datetime(
        df["date"], format="%b %d, %Y", errors="coerce"
    ).dt.tz_localize("UTC")

    return df


@handle_empty
def clean_news(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={"html": "text"})
    df["text"] = df["text"].apply(clean_html)

    return df
