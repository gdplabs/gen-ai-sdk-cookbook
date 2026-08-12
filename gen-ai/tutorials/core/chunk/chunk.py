"""Chunk basics: construct a Chunk and inspect its primary fields.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/chunk#the-additional_context-field
"""

from gllm_core.schema import Chunk


def main() -> None:
    """Build a Chunk with content + additional_context and print both."""
    chunk = Chunk(
        content="Capital: Paris",
        additional_context=[
            "Country: France",
            b"region: EU",  # binary items are allowed alongside text
        ],
        metadata={"src": "wiki"},
        score=0.9,
    )

    print(chunk.content)  # Capital: Paris
    print(chunk.additional_context)  # ['Country: France', b'region: EU']
    print(chunk.metadata)  # {'src': 'wiki'}
    print(chunk.score)  # 0.9

    # additional_context defaults to an empty list when omitted.
    plain = Chunk(content="Just the main content")
    print(plain.additional_context)  # []


if __name__ == "__main__":
    main()
