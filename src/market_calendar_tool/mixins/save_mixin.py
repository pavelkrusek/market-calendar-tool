import os
import pickle
from enum import Enum
from typing import Optional

import pandas as pd
from loguru import logger


class SaveFormat(Enum):
    PARQUET = "parquet"
    CSV = "csv"


class SaveMixin:
    def save(
        self,
        output_dir: Optional[str] = None,
        file_name: Optional[str] = None,
    ):
        output_dir = self._ensure_output_dir(output_dir)

        if file_name is None:
            file_name = "data.pickle"
            logger.warning("No file_name provided. Using default 'data.pickle'.")

        file_path = os.path.join(output_dir, file_name)

        try:
            with open(file_path, "wb") as f:
                pickle.dump(self, f)
            logger.info(f"Serialized ScrapeResult object to '{file_path}'.")
        except Exception as e:
            logger.error(
                f"Failed to serialize ScrapeResult object to '{file_path}': {e}"
            )
            raise e

    def save_to_dataframes(
        self,
        save_format: SaveFormat = SaveFormat.PARQUET,
        output_dir: Optional[str] = None,
        file_prefix: str = "data",
    ):
        output_dir = self._ensure_output_dir(output_dir)

        for attribute_name, attribute_value in self.__dict__.items():
            if isinstance(attribute_value, pd.DataFrame):
                if attribute_value.empty:
                    logger.info(f"Skipping empty DataFrame '{attribute_name}'.")
                    continue
                file_name = f"{file_prefix}_{attribute_name}.{save_format.value}"
                file_path = os.path.join(output_dir, file_name)
                try:
                    if save_format == SaveFormat.PARQUET:
                        attribute_value.to_parquet(file_path, index=False)
                    elif save_format == SaveFormat.CSV:
                        attribute_value.to_csv(file_path, index=False)
                    logger.info(f"Saved '{attribute_name}' DataFrame to '{file_path}'.")
                except Exception as e:
                    logger.error(
                        f"Failed to save '{attribute_name}' DataFrame to '{file_path}': {e}"
                    )
                    raise e

    @staticmethod
    def load_object(file_path: str):
        try:
            with open(file_path, "rb") as f:
                obj = pickle.load(f)
            logger.info(f"Deserialized object from '{file_path}'.")
            return obj
        except Exception as e:
            logger.error(f"Failed to deserialize object from '{file_path}': {e}")
            raise e

    def _ensure_output_dir(self, output_dir: Optional[str]) -> str:
        if output_dir is None:
            output_dir = os.getcwd()
            logger.info(
                f"No output_dir provided. Using current working directory: {output_dir}"
            )
        else:
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                    logger.info(f"Created output directory: {output_dir}")
                except OSError as e:
                    logger.error(
                        f"Failed to create output directory '{output_dir}': {e}"
                    )
                    raise OSError(
                        f"Failed to create output directory '{output_dir}': {e}"
                    )
            else:
                logger.info(f"Using existing output directory: {output_dir}")
        return output_dir
