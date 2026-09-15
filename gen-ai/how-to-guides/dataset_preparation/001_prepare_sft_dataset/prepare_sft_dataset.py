"""Prepare a local CSV dataset for supervised fine-tuning.

Authors:
    Muhamad Hasbullah Faris (hasbullah4869@gmail.com)

References:
    NONE
"""

import os
from pathlib import Path

os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

from gllm_finetuning.config import CsvPromptCatalogConfig, FileDataSourceConfig, PreprocessConfig
from gllm_finetuning.ingestion import registry
from gllm_finetuning.preprocessing import preprocess
from gllm_finetuning.schema import TrainingParadigm

RECIPE_DIR = Path(__file__).parent


def prepare_sft_dataset():
    """Load and format the bundled SFT CSV dataset.

    Returns:
        The formatted dataset with a `messages` column.
    """

    paradigm = TrainingParadigm.SFT
    dataset = registry.get("file").load(
        FileDataSourceConfig(
            source_type="file",
            path=str(RECIPE_DIR / "data" / "sft_examples.csv"),
            paradigm=paradigm,
        )
    )
    config = PreprocessConfig(
        min_chars={"other_columns": 1},
        prompt_catalog=CsvPromptCatalogConfig(
            source_type="csv",
            path=str(RECIPE_DIR / "data" / "prompt_catalog.csv"),
            prompt_name="support-answer",
        ),
    )
    return preprocess(dataset, config, paradigm)


def main() -> None:
    """Print the first formatted SFT example."""

    dataset = prepare_sft_dataset()
    print(f"Prepared {dataset.num_rows} SFT examples.")
    print(dataset[0])


if __name__ == "__main__":
    main()
