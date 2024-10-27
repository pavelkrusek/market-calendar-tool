import os
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
        save_format: SaveFormat = SaveFormat.PARQUET,
        output_dir: Optional[str] = None,
        file_prefix: str = "data",
    ):
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
