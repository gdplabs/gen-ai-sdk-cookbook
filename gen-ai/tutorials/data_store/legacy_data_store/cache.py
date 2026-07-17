"""
Legacy Vector Data Store as a cache with matching strategies.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/legacy/vector-data-store#use-as-a-cache
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Use legacy ChromaVectorDataStore as a cache with different strategies."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    vector_store = ChromaVectorDataStore(
        collection_name="my_cache",
        embedding=em_invoker,
    )

    # Exact matching (default)
    cache = vector_store.as_cache()
    await cache.store("user_query_123", "API response data")
    result = await cache.retrieve("user_query_123", "exact")
    print(f"Exact match: {result}")

    # Fuzzy matching
    cache_fuzzy = vector_store.as_cache(
        matching_strategy="fuzzy",
        matching_config={"max_distance": 2},
    )
    await cache_fuzzy.store(
        "What is artificial intelligence?", "AI explanation..."
    )
    result = await cache_fuzzy.retrieve(
        "What is artifical intelligence?", "fuzzy"
    )
    print(f"Fuzzy match: {result}")

    # Semantic matching
    cache_semantic = vector_store.as_cache(
        matching_strategy="semantic",
        matching_config={"min_similarity": 0.8},
    )
    await cache_semantic.store(
        "What is the weather like today?", "Weather forecast data..."
    )
    result = await cache_semantic.retrieve("Is it sunny today?", "semantic")
    print(f"Semantic match: {result}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
