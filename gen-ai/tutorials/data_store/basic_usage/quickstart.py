"""Data Store quick start: create a store, write chunks, and query them.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store#quick-start
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Quick start: create a Chroma data store and run basic queries."""
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

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
