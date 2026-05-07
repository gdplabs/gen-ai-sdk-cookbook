"""Mock inference function for evaluation tutorials.

This module provides a local replacement for `gllm_evals.utils.demo_utils.your_ai_func_result`
that returns deterministic mock outputs from a small built-in dataset.
"""

from typing import Any

_DATASET: list[dict[str, Any]] = [
    {
        "question_id": 1,
        "input": "What is the Capital of France?",
        "expected_output": "Paris",
        "generated_output": "New York",
        "retrieved_context": "Paris is the capital of France.",
    },
    {
        "question_id": 2,
        "input": "What is the sky color?",
        "expected_output": "Depends on the time and weather",
        "generated_output": "Blue",
        "retrieved_context": "Sky can be blue in the morning or orange-ish in the evening.",
    },
]


def your_ai_func_result(query: str) -> dict[str, Any]:
    """Return mock LLM output for a given query.

    Args:
        query: The input question / prompt.

    Returns:
        A dictionary with keys ``actual output`` and ``retrieved_context``
        matching the provided dataset. Raises ``ValueError`` if the query
        is not found.
    """
    for row in _DATASET:
        if row["input"] == query:
            return {
                "actual output": row["generated_output"],
                "retrieved_context": row["retrieved_context"],
            }
    raise ValueError(f"Query not found in mock dataset: {query!r}")
