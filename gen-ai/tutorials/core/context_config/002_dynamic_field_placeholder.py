"""Demonstrate dynamic field placeholders in a ContextConfig template.

A placeholder matching any name in `fields` is resolved from the data payload.
This script also shows that when a selected field resolves to nothing, render()
returns None for this release rather than an empty substitution.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/context-config#template-placeholder-syntax
"""

from gllm_core.schema import ContextConfig


def main() -> None:
    """Render with a dynamic field placeholder and observe the empty-result case."""
    # {content} is a dynamic placeholder because "content" is in fields.
    config = ContextConfig(
        fields=["content", "metadata"],
        template="Content: {content}\nMetadata: {metadata_json}",
    )
    print(config.render({"content": "receipt", "metadata": {"source": "docs"}}))
    # Content: receipt
    # Metadata: {
    #   "source": "docs"
    # }

    # If the only selected field resolves to nothing (absent from data),
    # render() returns None rather than a half-empty string.
    missing = ContextConfig(fields=["content"], template="Got: {content}")
    print(missing.render({"other": "value"}))  # None


if __name__ == "__main__":
    main()
