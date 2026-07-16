"""
Hybrid search example using Elasticsearch data store.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store#using-hybrid-search
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.capabilities.hybrid_capability import (
    HybridSearchType,
    SearchConfig,
)
from gllm_datastore.core.filters import QueryOptions
from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Use hybrid search combining fulltext and vector retrieval."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

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

    store = ElasticsearchDataStore(
        index_name="my_index",
        url="http://localhost:9200",
    ).with_hybrid(config=hybrid_config)

    chunks = [
        Chunk(id="doc:1", content="Machine learning is fascinating"),
        Chunk(id="doc:2", content="Deep learning drives AI progress"),
    ]
    await store.hybrid.create(chunks)

    results = await store.hybrid.retrieve(
        "machine learning",
        options=QueryOptions(limit=10),
    )
    for chunk in results:
        print(f"  - {chunk.content}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
