from itertools import chain
from typing import List, Optional

import pandas as pd


class DataProcessingError(Exception):
    """Custom exception for data processing errors."""


class DataProcessor:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def to_df(self) -> pd.DataFrame:
        """
        Convert raw data to a cleaned pandas DataFrame.

        Returns:
            pd.DataFrame: The processed DataFrame.
        """
        try:
            events = list(
                chain.from_iterable(
                    day.get("events", []) for day in self.raw_data.get("days", [])
                )
            )
            df = pd.DataFrame(events)
            # self._clean_data(df)
            return df
        except Exception as e:
            raise DataProcessingError(f"Failed to convert base data to DataFrame: {e}")

    def _to_df(
        self,
        record_path: List[str],
        meta: Optional[List[List[str]]] = None,
        rename_cols: Optional[dict] = None,
    ) -> pd.DataFrame:
        try:
            df = pd.json_normalize(
                self.raw_data, record_path=record_path, meta=meta, errors="ignore"
            )

            if rename_cols:
                df.rename(columns=rename_cols, inplace=True)

            return df

        except Exception as e:
            raise DataProcessingError(f"Failed to convert data to DataFrame: {e}")

    def to_specs_df(self) -> pd.DataFrame:
        return self._to_df(
            record_path=["data", "specs"],
            meta=[["data", "event_id"]],
            rename_cols={"data.event_id": "id"},
        )

    def to_news_df(self) -> pd.DataFrame:
        return self._to_df(
            record_path=["data", "linked_threads", "news"],
            meta=[["data", "event_id"]],
            rename_cols={"data.event_id": "id"},
        )

    def to_history_df(self) -> pd.DataFrame:
        return self._to_df(
            record_path=["data", "history", "events"],
            meta=[["data", "event_id"]],
            rename_cols={"data.event_id": "id"},
        )
