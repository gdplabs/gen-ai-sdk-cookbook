"""Demonstrate metadata_keys filtering and the None return for empty selection.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/context-config#metadata_keys-filtering
"""

from gllm_core.schema import ContextConfig


def main() -> None:
    """Show metadata_keys = None/listed/explicit and the None return when no fields."""

    # None (default) and an empty list both mean: keep all metadata keys.
    data = {
        "content": "receipt",
        "metadata": {"source": "docs", "page": 2, "internal": True},
    }

    # None (default) -> all metadata keys are included.
    all_metadata = ContextConfig(fields=["content", "metadata"])
    print(all_metadata.render(data))

    # Empty list -> treated the same as None: all metadata keys are included.
    empty_filter = ContextConfig(fields=["content", "metadata"], metadata_keys=[])
    print(empty_filter.render(data))

    # Explicit list -> only the listed keys that exist are kept; the rest are skipped.
    only_source = ContextConfig(
        fields=["content", "metadata"],
        metadata_keys=["source", "missing"],
    )
    print(only_source.render(data))

    # No fields selected -> render() returns None.
    none_selected = ContextConfig(fields=[], template="static context")
    print(none_selected.render({"content": "text"}))  # None


if __name__ == "__main__":
    main()
