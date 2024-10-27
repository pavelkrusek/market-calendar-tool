import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

import pandas as pd

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

    def save(
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
        super().save(
            save_format=save_format, output_dir=output_dir, file_prefix=file_prefix
        )
