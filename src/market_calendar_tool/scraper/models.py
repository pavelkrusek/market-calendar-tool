import glob
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

import pandas as pd
from loguru import logger

from market_calendar_tool.mixins.save_mixin import SaveFormat, SaveMixin


class Site(Enum):
    FOREXFACTORY = "https://www.forexfactory.com/calendar"
    METALSMINE = "https://www.metalsmine.com/calendar"
    ENERGYEXCH = "https://www.energyexch.com/calendar"
    CRYPTOCRAFT = "https://www.cryptocraft.com/calendar"

    @property
    def prefix(self):
        prefix = self.name.lower()
        return re.sub(r"\W+", "_", prefix)


site_number_mapping = {
    Site.FOREXFACTORY: 1,
    Site.METALSMINE: 2,
    Site.ENERGYEXCH: 3,
    Site.CRYPTOCRAFT: 4,
}


@dataclass(frozen=True)
class ScrapeOptions:
    max_parallel_tasks: int = 5

    def __post_init__(self):
        if self.max_parallel_tasks < 1:
            raise ValueError("max_parallel_tasks must be at least 1")


@dataclass
class ScrapeResult(SaveMixin):
    site: Site
    date_from: str
    date_to: str
    base: pd.DataFrame
    scraped_at: float = field(default_factory=lambda: time.time())
    specs: pd.DataFrame = field(default_factory=pd.DataFrame)
    history: pd.DataFrame = field(default_factory=pd.DataFrame)
    news: pd.DataFrame = field(default_factory=pd.DataFrame)

    def save_to_dataframes(
        self,
        save_format: SaveFormat = SaveFormat.PARQUET,
        output_dir: Optional[str] = None,
    ):
        formatted_time = datetime.fromtimestamp(self.scraped_at).strftime(
            "%Y%m%d%H%M%S"
        )
        file_prefix = (
            f"{self.site.prefix}__{self.date_from}_{self.date_to}_{formatted_time}"
        )
        super().save_to_dataframes(
            save_format=save_format, output_dir=output_dir, file_prefix=file_prefix
        )

    def save(
        self,
        output_dir: Optional[str] = None,
    ):
        formatted_time = datetime.fromtimestamp(self.scraped_at).strftime(
            "%Y%m%d%H%M%S"
        )
        file_name = f"scrape_result_{formatted_time}.pickle"
        super().save(output_dir=output_dir, file_name=file_name)

    @classmethod
    def load(cls, file_path: Optional[str] = None) -> "ScrapeResult":
        if file_path is None:
            pattern = os.path.join(os.getcwd(), "scrape_result_*.pickle")
            files = glob.glob(pattern)

            if not files:
                raise FileNotFoundError(
                    "No 'scrape_result_*.pickle' files found in the current directory."
                )

            def extract_timestamp(f):
                try:
                    timestamp_str = (
                        os.path.basename(f).split("_")[2].split(".pickle")[0]
                    )
                    return datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                except (IndexError, ValueError):
                    return datetime.min

            latest_file = max(files, key=extract_timestamp)
            logger.info(f"No file_path provided. Using the latest file: {latest_file}")
            file_path = latest_file

        return cls.load_object(file_path)
