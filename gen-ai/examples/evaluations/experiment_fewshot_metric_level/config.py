"""Experiment configurations.

This module contains all experiment configurations including dataset paths
and model information.
"""

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
FEWSHOT_JSON = DATA_DIR / "fewshot_examples.json"

# Experiment configurations
EXPERIMENTS = [
    {
        "index": 0,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 1,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 2,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 3,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 4,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 5,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 6,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 7,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 8,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 9,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 10,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 11,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 12,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 13,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
    {
        "index": 14,
        "model_provider": "your_model_provider",
        "provider_model_id": "your_provider_model_id",
        "data_path": DATA_DIR / "your_experiment_file.csv",
    },
]


def get_experiment_config(index):
    """Get experiment configuration by index (int or string name).

    Args:
        index: Experiment index (int) or name (string).

    Returns:
        dict: Experiment configuration.

    Raises:
        ValueError: If experiment not found.
    """
    # If index is a string that looks like an integer, convert to int first
    if isinstance(index, str) and index.isdigit():
        index = int(index)
    
    # Try to find matching experiment by index field
    for exp in EXPERIMENTS:
        if exp["index"] == index:
            return exp

    raise ValueError(f"Experiment '{index}' not found. Available: {[e['index'] for e in EXPERIMENTS]}")



def get_fewshot_json_path(use_small_data: bool = False) -> Path:
    """Get path to few-shot examples JSON.

    Args:
        use_small_data (bool, optional): Whether to use small dataset. Defaults to False.

    Returns:
        Path: Path to few-shot JSON file.
    """
    if use_small_data:
        small_path = DATA_DIR / "fewshot_examples_small.json"
        if small_path.exists():
            return small_path

    return FEWSHOT_JSON
