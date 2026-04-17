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
        "index": "botanica_test",
        "model_provider": "google",
        "model_id": "gemini-1.5-flash-002",
        "data_path": BASE_DIR / "data" / "botanica_test.csv",
    },
    {
        "index": "botanica",
        "model_provider": "google",
        "model_id": "gemini-1.5-flash-002",
        "data_path": BASE_DIR / "data" / "botanica_experiment.csv",
    },
    {
        "index": 0,
        "model_provider": "novita-ai",
        "provider_model_id": "qwen/qwen2.5-vl-72b-instruct",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - fe0efd62-340a-492d-b83a-e93af8c2d704.csv",
    },
    {
        "index": 1,
        "model_provider": "novita-ai",
        "provider_model_id": "meta-llama/llama-3.3-70b-instruct",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 4a16abdc-eba1-4d6f-96ea-a6b1d2f97ea5.csv",
    },
    {
        "index": 2,
        "model_provider": "novita-ai",
        "provider_model_id": "deepseek/deepseek-chat",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 62f8a4c4-beb1-46e6-b77a-2fd4ffc2f2e4.csv",
    },
    {
        "index": 3,
        "model_provider": "novita-ai",
        "provider_model_id": "qwen/qwen2.5-72b-instruct",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 7dc061ee-bfd7-4d6c-9e41-76f60acfcf3b.csv",
    },
    {
        "index": 4,
        "model_provider": "openai",
        "provider_model_id": "gpt-4o",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 9c6e2b52-2de4-4e1f-92da-7cea5c22a01a.csv",
    },
    {
        "index": 5,
        "model_provider": "openai",
        "provider_model_id": "gpt-4o-mini",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - a64a6e4d-da3c-4bda-b4d1-c3c20513c0ac.csv",
    },
    {
        "index": 6,
        "model_provider": "google",
        "provider_model_id": "gemini-1.5-pro-002",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 0df96eea-b1c9-4a24-83e9-e2df67fbf8c2.csv",
    },
    {
        "index": 7,
        "model_provider": "google",
        "provider_model_id": "gemini-1.5-flash-002",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - c464b80e-5064-40f3-96de-10b050277b30.csv",
    },
    {
        "index": 8,
        "model_provider": "anthropic",
        "provider_model_id": "claude-3.5-sonnet",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 3d3c6d52-8b09-4a9e-9e6c-7ae8fc2a73bc.csv",
    },
    {
        "index": 9,
        "model_provider": "anthropic",
        "provider_model_id": "claude-3.5-haiku",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 77e8e95f-a1fd-4d68-9ca5-87b2f6baec29.csv",
    },
    {
        "index": 10,
        "model_provider": "anthropic",
        "provider_model_id": "claude-3-opus",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 1fa91aeb-0e33-4f5e-bcc3-51cb29cf09dd.csv",
    },
    {
        "index": 11,
        "model_provider": "anthropic",
        "provider_model_id": "claude-3-haiku",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 1cdb9c90-a5ed-439c-a86a-3e3aa8d03e5d.csv",
    },
    {
        "index": 12,
        "model_provider": "anthropic",
        "provider_model_id": "claude-3-sonnet",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - ccb40be3-0d9a-4f48-abd2-a5bb1dd6e6d4.csv",
    },
    {
        "index": 13,
        "model_provider": "amazon-bedrock",
        "provider_model_id": "amazon-titan-text-premier",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 00a6e0e2-a8a4-460e-81f6-afd82b21e45d.csv",
    },
    {
        "index": 14,
        "model_provider": "cohere",
        "provider_model_id": "command-r-plus",
        "path": "/home/daniel-adi/GL-SDK/explore-fewshot/gl-sdk/libs/gllm-evals/gllm_evals/experiment_few_shot_per_questions/data/new_experiments/botanica-5ad4cf0f64c81f5c84c564d2b5b3a084f9a6e8c5da22aaecdf49befba2039672 - 4b29a76e-a3fe-4c87-a4bd-0c7d3dd84e82.csv",
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
