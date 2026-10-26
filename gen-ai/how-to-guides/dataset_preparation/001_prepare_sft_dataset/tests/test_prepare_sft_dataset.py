"""Smoke tests for the local SFT preparation recipe.

Authors:
    Muhamad Hasbullah Faris (hasbullah4869@gmail.com)

References:
    NONE
"""

from prepare_sft_dataset import prepare_sft_dataset


def test_prepare_sft_dataset_returns_messages() -> None:
    """Condition: bundled CSV input; Expected: formatted SFT messages."""

    dataset = prepare_sft_dataset()

    assert dataset.column_names == ["messages"]
    assert dataset.num_rows == 2
    assert [message["role"] for message in dataset[0]["messages"]] == ["system", "user", "assistant"]
