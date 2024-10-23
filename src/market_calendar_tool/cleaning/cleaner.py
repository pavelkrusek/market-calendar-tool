import re
from enum import Enum

import pandas as pd
import pycountry
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


def is_valid_currency(currency: str) -> bool:
    try:
        return pycountry.currencies.get(alpha_3=currency.upper()) is not None
    except Exception as e:
        logger.error(f"Error in is_valid_currency: {e}")
        return False


def camel_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def clean_data(df: pd.DataFrame | ScrapeResult) -> pd.DataFrame:
    if isinstance(df, ScrapeResult):
        df = df.base

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
