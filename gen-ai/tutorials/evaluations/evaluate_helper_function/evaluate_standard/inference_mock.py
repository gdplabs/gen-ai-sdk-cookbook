from typing import Any

from gllm_evals.dataset.dict_dataset import DictDataset

# Load local CSV entries once at import time.
_DATASET: dict[str, dict[str, Any]] = {
    row["query"]: {
        "actual output": row["generated_response"],
        "retrieved_context": row["retrieved_context"],
    }
    for row in DictDataset.from_csv("dataset_examples/simple_qa_data.csv").load()
}

# Add Google Sheets dataset entries (exact query strings from the sheet).
_DATASET["What is the Capital of France?"] = {
    "actual output": "New York",
    "retrieved_context": "Paris is the capital of France.",
}
_DATASET["What is the sky color?"] = {
    "actual output": "Blue",
    "retrieved_context": "Sky can be blue in the morning or orange-ish in the evening.",
}


def your_ai_func_result(query: str) -> dict[str, Any]:
    """Return mock LLM output for a given query.

    Args:
        query: The input question / prompt. Must match a query value from either
            the local CSV or the Google Sheets tutorial dataset.

    Returns:
        Dictionary with keys ``actual output`` and ``retrieved_context``.

    Raises:
        ValueError: If *query* is not found in the dataset.
    """
    if query not in _DATASET:
        raise ValueError(f"Query not found in mock dataset: {query!r}")
    return _DATASET[query]
