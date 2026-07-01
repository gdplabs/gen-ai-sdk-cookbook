"""Example of querying data stores with metadata filters.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/query-filter
"""

import asyncio

from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_datastore.core.filters import filter as F
from gllm_inference.em_invoker import OpenAIEMInvoker


async def main() -> None:
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
        Chunk(id="book:1", content="AI is useful for programming", metadata={"topic": "AI", "category": "published"}),
        Chunk(id="book:2", content="Cheesecake is delicious", metadata={"topic": "food", "category": "published"}),
        Chunk(id="book:3", content="Sushi is delicious", metadata={"topic": "food", "category": "unpublished"}),
    ]
    await store.fulltext.create(chunks)

    results = await store.fulltext.retrieve(filters=F.eq("metadata.topic", "food"))


if __name__ == "__main__":
    asyncio.run(main())
