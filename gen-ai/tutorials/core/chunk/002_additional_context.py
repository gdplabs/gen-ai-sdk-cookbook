"""additional_context: __repr__ preview and per-item validation.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/chunk#the-additional_context-field
"""

from pydantic import ValidationError

from gllm_core.schema import Chunk


def main() -> None:
    """Show the __repr__ previewing additional_context and the validation error."""
    chunk = Chunk(
        content="Capital: Paris",
        additional_context=["Country: France", b"region: EU"],
        metadata={"src": "wiki"},
        score=0.9,
    )

    # __repr__ now previews additional_context alongside content and metadata.
    # Binary items render as '(Binary content)' and long strings are truncated.
    print(repr(chunk))

    # Each item must be non-empty (str or bytes). An empty string raises a
    # ValidationError with min_length=1 per item, just like content.
    try:
        Chunk(content="text", additional_context=[""])  # empty string -> error
    except ValidationError as exc:
        print(exc)


if __name__ == "__main__":
    main()
