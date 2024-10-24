from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ScrapeOptions:
    max_parallel_tasks: int = 5

    def __post_init__(self):
        if self.max_parallel_tasks < 1:
            raise ValueError("max_parallel_tasks must be at least 1")


@dataclass
class ScrapeResult:
    base: pd.DataFrame
    specs: pd.DataFrame
    history: pd.DataFrame
    news: pd.DataFrame
