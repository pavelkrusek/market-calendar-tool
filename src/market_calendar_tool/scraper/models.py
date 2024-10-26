from dataclasses import dataclass, field
from enum import Enum

import pandas as pd


class Site(Enum):
    FOREXFACTORY = "https://www.forexfactory.com/calendar"
    METALSMINE = "https://www.metalsmine.com/calendar"
    ENERGYEXCH = "https://www.energyexch.com/calendar"
    CRYPTOCRAFT = "https://www.cryptocraft.com/calendar"


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
class ScrapeResult:
    site: Site
    base: pd.DataFrame
    specs: pd.DataFrame = field(default_factory=pd.DataFrame)
    history: pd.DataFrame = field(default_factory=pd.DataFrame)
    news: pd.DataFrame = field(default_factory=pd.DataFrame)
