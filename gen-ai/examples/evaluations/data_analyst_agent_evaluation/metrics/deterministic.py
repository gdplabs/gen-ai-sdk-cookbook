"""Simple deterministic metrics that do not require LLM calls."""

import json


def keyword_match(response: str, keywords: list[str]) -> bool:
    """Return True if ALL keywords appear in response (case-insensitive).

    Args:
        response: The response text to check.
        keywords: List of keywords to match.

    Returns:
        bool: True if all keywords are found (case-insensitive), False otherwise.
    """
    if not response or not keywords:
        return False

    response_lower = response.lower()
    return all(keyword.lower() in response_lower for keyword in keywords)


def answer_not_empty(record: dict) -> bool:
    """Return True if the answer field is not empty."""
    return bool(record.get("answer", "").strip())


def trajectory_has_final_answer(record: dict) -> bool:
    """Return True if the trajectory contains a final answer from the assistant."""
    raw = record.get("generated_agent_trajectory", "")
    if not raw:
        return False
    try:
        messages = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return False
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            return bool(msg.get("content", "").strip())
    return False
