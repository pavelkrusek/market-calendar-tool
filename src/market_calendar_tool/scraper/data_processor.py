from itertools import chain

import pandas as pd


class DataProcessingError(Exception):
    """Custom exception for data processing errors."""

    pass


class DataProcessor:
    def __init__(self, raw_data: dict):
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
            raise DataProcessingError(f"Failed to convert data to DataFrame: {e}")
