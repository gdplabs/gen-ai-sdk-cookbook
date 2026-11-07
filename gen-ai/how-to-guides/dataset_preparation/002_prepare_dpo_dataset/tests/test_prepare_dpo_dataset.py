"""Smoke tests for the local DPO preparation recipe.

Authors:
    Muhamad Hasbullah Faris (hasbullah4869@gmail.com)

References:
    NONE
"""

from prepare_dpo_dataset import prepare_dpo_dataset


def test_prepare_dpo_dataset_returns_preferences() -> None:
    """Condition: bundled CSV input; Expected: formatted DPO preferences."""

    dataset = prepare_dpo_dataset()

    assert dataset.column_names == ["messages", "chosen", "rejected"]
    assert dataset.num_rows == 2
    assert [message["role"] for message in dataset[0]["messages"]] == ["system", "user"]
    assert dataset[0]["chosen"]["role"] == "assistant"
    assert dataset[0]["rejected"]["role"] == "assistant"
