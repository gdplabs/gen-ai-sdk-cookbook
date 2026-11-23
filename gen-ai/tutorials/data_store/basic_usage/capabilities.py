"""
Using the store end to end: fulltext, vector, hybrid, and query filter capabilities.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store#using-the-store-end-to-end
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.capabilities.hybrid_capability import (
    HybridSearchType,
    SearchConfig,
)
from gllm_datastore.core.filters import QueryOptions, filter as F
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Exercise fulltext, vector, and hybrid capability methods."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    store = (
        ChromaDataStore(
            collection_name="customer-notes",
            client_type=ChromaClientType.MEMORY,
        )
        .with_fulltext()
        .with_vector(em_invoker=em_invoker)
    )

    # 1. Prepare chunks
    chunk = Chunk(
        id="note-1",
        content="Order 938 is ready for pickup",
        metadata={"store": "jakarta", "status": "ready"},
    )

    # 2. Fulltext methods
    await store.fulltext.create(chunk)

    results = await store.fulltext.retrieve(
        filters=F.eq("metadata.status", "ready"),
        options=QueryOptions(limit=10),
    )
    print("Fulltext retrieve:")
    for c in results:
        print(f"  - {c.content}")

    await store.fulltext.update(
        update_values={
            "metadata": {"store": "jakarta", "status": "picked_up"}
        },
        filters=F.eq("id", "note-1"),
    )

    await store.fulltext.delete(filters=F.eq("id", "note-1"))
    print("Fulltext create/update/delete done")

    # 3. Vector methods
    await store.vector.create(chunk)

    semantic_hits = await store.vector.retrieve(
        query="orders ready for pickup",
        filters=F.eq("metadata.store", "jakarta"),
        options=QueryOptions(limit=5),
    )
    print("\nVector retrieve:")
    for c in semantic_hits:
        print(f"  - {c.content}")

    # 4. Query filters and options
    filters = F.and_(
        F.eq("metadata.store", "jakarta"),
        F.eq("metadata.status", "ready"),
    )
    options = QueryOptions(
        limit=20, order_by="metadata.updated_at", order_desc=True
    )
    results = await store.fulltext.retrieve(filters=filters, options=options)
    print(f"\nFiltered results: {len(results)}")

    # 5. Hybrid methods (requires backend that supports hybrid,
    #    e.g. ElasticsearchDataStore)
    hybrid_config = [
        SearchConfig(
            search_type=HybridSearchType.FULLTEXT,
            field="text",
            weight=0.3,
        ),
        SearchConfig(
            search_type=HybridSearchType.VECTOR,
            field="embedding",
            weight=0.7,
            em_invoker=em_invoker,
        ),
    ]
    # store = ElasticsearchDataStore(
    #     index_name="my_index", url="http://localhost:9200"
    # ).with_hybrid(config=hybrid_config)
    # await store.hybrid.create(chunks)
    # hits = await store.hybrid.retrieve(
    #     query="pickup orders",
    #     filters=F.eq("metadata.status", "ready"),
    #     options=QueryOptions(limit=10),
    # )
    print(f"\nHybrid config prepared: {len(hybrid_config)} search configs")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
