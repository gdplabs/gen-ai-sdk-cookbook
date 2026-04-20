"""An example of filtering data in a vector store.

Authors:
    - Kadek Denaya (kadek.d.r.diana@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/query-filter
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store.chroma.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main():
    """Filter data in a vector store."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    store = ChromaDataStore(collection_name="articles").with_vector(
        em_invoker=em_invoker
    )

    chunks = [
        Chunk(
            id="book:1",
            content="AI is useful for programming",
            metadata={"topic": "AI", "category": "published"},
        ),
        Chunk(
            id="book:2",
            content="AI is the future",
            metadata={"topic": "AI", "category": "unpublished"},
        ),
        Chunk(
            id="book:3",
            content="Parrot is a bird",
            metadata={"topic": "birds", "category": "published"},
        ),
    ]
    await store.vector.create(chunks)

    results: list[Chunk] = await store.vector.retrieve(
        query="is AI the future?",
        filters=F.and_(
            F.eq("metadata.topic", "AI"), F.eq("metadata.category", "published")
        ),
    )
    for chunk in results:
        print(f"Chunk content: {chunk.content}")
        print(f"Chunk similarity score: {chunk.score}")
        print("---")


if __name__ == "__main__":
    asyncio.run(main())
