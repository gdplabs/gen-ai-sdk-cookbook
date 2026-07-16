"""
QueryOptions: limit, pagination, and sorting for data store queries.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/query-filter#query-options
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
    """Use QueryOptions for pagination, sorting, and field projection."""
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
            id=f"book:{i}",
            content=f"Content {i}",
            metadata={"status": "published", "created_at": f"2025-01-{i:02d}"},
        )
        for i in range(1, 6)
    ]
    await store.fulltext.create(chunks)

    # Limit results
    latest_published = await store.fulltext.retrieve(
        filters=F.eq("metadata.status", "published"),
        options=QueryOptions(limit=5),
    )
    print(f"Limited results: {len(latest_published)}")

    # Pagination
    page_size = 2
    page = 2
    results = await store.fulltext.retrieve(
        filters=F.eq("metadata.status", "published"),
        options=QueryOptions(
            limit=page_size,
            offset=(page - 1) * page_size,
        ),
    )
    print(f"Page {page} results: {len(results)}")

    # Sorting
    recent_results = await store.fulltext.retrieve(
        filters=F.eq("metadata.status", "published"),
        options=QueryOptions(
            order_by="metadata.created_at",
            order_desc=True,
            limit=10,
        ),
    )
    print(f"Sorted results: {[c.id for c in recent_results]}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
