import asyncio

from gllm_core.schema import Chunk
from gllm_generation.context_enricher import MetadataContextEnricher
from gllm_generation.context_enricher.metadata_context_enricher import (
    MetadataPosition,
)


def main() -> None:
    # Prepare retrieved chunks (each is a gllm_core.schema.Chunk)
    chunks = [
        Chunk(
            content="Neural networks learn by gradient descent.",
            metadata={"title": "Intro to DL", "source": "docs://ml101", "page": 3, "tags": ["ml", "basics"]},
        ),
        Chunk(
            content="Transformers use self-attention.",
            metadata={"title": "Transformers", "source": "docs://nlp", "page": 10},
        ),
    ]

    # Configure the enricher
    enricher = MetadataContextEnricher(
        metadata_fields=["title", "source", "page", "tags"],
        position=MetadataPosition.PREFIX,       # or MetadataPosition.SUFFIX
        separator="\n---\n",
        field_template="- {field}: {value}",
    )

    # Enrich in place; returns the same list for convenience
    enriched = asyncio.run(enricher.enrich(chunks))

    # Use enriched chunks downstream (e.g., to prompt an LLM)
    print(enriched[0].content)

if __name__ == "__main__":
    main()
