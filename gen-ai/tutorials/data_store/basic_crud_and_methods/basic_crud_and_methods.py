"""
Data Store quick start and basic CRUD operations.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import QueryOptions, filter as F
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Quick start: create a data store, write chunks, and query them."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    store = (
        ChromaDataStore(
            collection_name="customer-notes",
            client_type=ChromaClientType.MEMORY,
        )
        .with_fulltext()
        .with_vector(em_invoker=em_invoker)
    )

    chunks = [
        Chunk(
            id="book:1",
            content="AI is useful for programming",
            metadata={"topic": "AI"},
        ),
        Chunk(
            id="book:2",
            content="Cheesecake is delicious",
            metadata={"topic": "food"},
        ),
        Chunk(
            id="book:3",
            content="Sushi is delicious",
            metadata={"topic": "food"},
        ),
    ]
    await store.fulltext.create(chunks)

    # Query via metadata filter
    results = await store.fulltext.retrieve(
        filters=F.eq("metadata.topic", "food")
    )
    print("Fulltext results:")
    for chunk in results:
        print(f"  - {chunk.content}")

    # Query via semantic similarity
    results = await store.vector.retrieve(query="pickup orders")
    print("\nVector results:")
    for chunk in results:
        print(f"  - {chunk.content}")

    # Query with combined filters and options
    filters = F.and_(
        F.eq("metadata.topic", "food"),
    )
    options = QueryOptions(limit=20, order_desc=True)
    hits = await store.fulltext.retrieve(filters=filters, options=options)
    print("\nFiltered fulltext results:")
    for chunk in hits:
        print(f"  - {chunk.content}")

    semantic_hits = await store.vector.retrieve(
        query="orders ready for pickup",
        filters=filters,
        options=QueryOptions(limit=5),
    )
    print("\nFiltered vector results:")
    for chunk in semantic_hits:
        print(f"  - {chunk.content}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
