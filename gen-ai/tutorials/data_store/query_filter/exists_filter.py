"""
Existence filter: match records where a metadata field is present or absent.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/query-filter#existence-filter
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store import InMemoryDataStore

load_dotenv()


async def main() -> None:
    """Use F.exists(...) and F.not_(F.exists(...)) to filter on field presence."""
    # In-memory store needs no Docker/API key and supports the EXISTS operator.
    store = InMemoryDataStore().with_fulltext()

    chunks = [
        Chunk(
            id="doc:1",
            content="AI is useful for programming",
            metadata={"source": "gl-sdk-docs", "topic": "AI"},
        ),
        # No "source" field on purpose.
        Chunk(
            id="doc:2",
            content="Cheesecake is delicious",
            metadata={"topic": "food"},
        ),
        Chunk(
            id="doc:3",
            content="Sushi is delicious",
            metadata={"source": "internal-blog", "topic": "food"},
        ),
    ]
    await store.fulltext.create(chunks)

    # Existence filter: records where metadata.source is present.
    exists_filter = F.exists("metadata.source")
    present = await store.fulltext.retrieve(filters=exists_filter)
    print("Chunks with metadata.source present:")
    for chunk in present:
        print(f"  - {chunk.content} (source={chunk.metadata['source']})")

    # Negative existence: records where metadata.source is missing or null.
    missing_filter = F.not_(F.exists("metadata.source"))
    absent = await store.fulltext.retrieve(filters=missing_filter)
    print("\nChunks with metadata.source absent:")
    for chunk in absent:
        print(f"  - {chunk.content} (keys={list(chunk.metadata)})")


if __name__ == "__main__":
    asyncio.run(main())
