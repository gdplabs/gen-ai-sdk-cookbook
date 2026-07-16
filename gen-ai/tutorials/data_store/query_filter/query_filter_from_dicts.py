"""
Building query filters from dictionaries using QueryFilter.from_dicts().

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/query-filter#building-filters-from-dictionaries
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import FilterCondition, QueryFilter
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Build filters from dictionary definitions."""
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
            metadata={"topic": "AI", "status": "published"},
        ),
        Chunk(
            id="book:2",
            content="Cheesecake is delicious",
            metadata={"topic": "food", "status": "published"},
        ),
    ]
    await store.fulltext.create(chunks)

    filters = QueryFilter.from_dicts(
        [
            {"key": "metadata.topic", "value": "AI", "operator": "=="},
            {"key": "metadata.status", "value": "published", "operator": "=="},
        ],
        condition=FilterCondition.AND,
    )

    results = await store.fulltext.retrieve(filters=filters)
    print("Dict-built filter results:")
    for chunk in results:
        print(f"  - {chunk.content}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
