import asyncio

from gllm_core.schema import Chunk
from gllm_generation.context_enricher import MetadataContextEnricher
from gllm_generation.context_enricher.metadata_context_enricher import MetadataPosition


def main() -> None:
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

    enricher = MetadataContextEnricher(
        metadata_fields=["title", "source", "page", "tags"],
        position=MetadataPosition.PREFIX,
        separator="\n---\n",
        field_template="- {field}: {value}",
    )

    enriched = asyncio.run(enricher.enrich(chunks))
    print(enriched[0].content)


if __name__ == "__main__":
    main()
