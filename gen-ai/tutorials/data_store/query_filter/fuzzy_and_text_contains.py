"""
Fuzzy and text-contains filters with their optional arguments.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/query-filter#fuzzy-metadata-filter
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/query-filter#text-contains-options
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store import InMemoryDataStore

load_dotenv()


async def main() -> None:
    """Use F.fuzzy(prefix_length=...) and F.text_contains(literal_match=..., case_sensitive=...)."""
    # In-memory store needs no Docker/API key and supports every option shown here.
    store = InMemoryDataStore().with_fulltext()

    chunks = [
        Chunk(
            id="doc:1",
            content="Machine learning basics",
            metadata={"title": "machine learning"},
        ),
        Chunk(
            id="doc:2",
            content="Sale: 50%_off everything",
            metadata={"title": "50%_off sale"},
        ),
        Chunk(
            id="doc:3",
            content="Cooking with cheese",
            metadata={"title": "Cheese cookbook"},
        ),
    ]
    await store.fulltext.create(chunks)

    # Fuzzy metadata filter: tolerates the typo in "lerning".
    fuzzy = await store.fulltext.retrieve(filters=F.fuzzy("metadata.title", "machine lerning"))
    print("Fuzzy match:")
    for chunk in fuzzy:
        print(f"  - {chunk.metadata['title']}")

    # prefix_length: the first 3 characters must match exactly.
    fuzzy_prefix = await store.fulltext.retrieve(
        filters=F.fuzzy("metadata.title", "machine lerning", prefix_length=3)
    )
    print("Fuzzy match with prefix_length=3:")
    for chunk in fuzzy_prefix:
        print(f"  - {chunk.metadata['title']}")

    # Text contains options: literal substring ("%" and "_" are not wildcards), case-insensitive.
    contains = await store.fulltext.retrieve(
        filters=F.text_contains("metadata.title", "50%_OFF", literal_match=True, case_sensitive=False)
    )
    print("Text contains (literal_match=True, case_sensitive=False):")
    for chunk in contains:
        print(f"  - {chunk.metadata['title']}")

    # Case-sensitive: "cheese" does not match "Cheese".
    case_sensitive = await store.fulltext.retrieve(
        filters=F.text_contains("metadata.title", "cheese", case_sensitive=True)
    )
    print(f"Text contains (case_sensitive=True) matches: {len(case_sensitive)}")


if __name__ == "__main__":
    asyncio.run(main())
