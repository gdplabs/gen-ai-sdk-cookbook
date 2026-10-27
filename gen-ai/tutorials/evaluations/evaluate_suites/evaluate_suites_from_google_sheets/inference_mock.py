from typing import Any

# Mock outputs for the rows of the tutorial Google Sheet (exact query strings from the sheet).
_DATASET: dict[str, dict[str, Any]] = {
    "What is the Capital of France?": {
        "actual output": "New York",
        "retrieved_context": "Paris is the capital of France.",
    },
    "What is the sky color?": {
        "actual output": "Blue",
        "retrieved_context": "Sky can be blue in the morning or orange-ish in the evening.",
    },
}


def your_ai_func_result(query: str) -> dict[str, Any]:
    """Return mock LLM output for a given query.

    Args:
        query: The input question / prompt. Must match a query value from the
            tutorial Google Sheet.

    Returns:
        Dictionary with keys ``actual output`` and ``retrieved_context``.

    Raises:
        ValueError: If *query* is not found in the dataset.
    """
    if query not in _DATASET:
        raise ValueError(f"Query not found in mock dataset: {query!r}")
    return _DATASET[query]
