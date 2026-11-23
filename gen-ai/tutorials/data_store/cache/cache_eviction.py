"""
Cache eviction: TTL, LRU, and LFU strategies with lifecycle management.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/cache#eviction-basics
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.cache.vector_cache.eviction_manager import (
    asyncio_eviction_manager,
)
from gllm_datastore.cache.vector_cache.eviction_strategy import (
    lru_eviction_strategy,
    ttl_eviction_strategy,
)
from gllm_datastore.data_store import ChromaDataStore

AsyncIOEvictionManager = asyncio_eviction_manager.AsyncIOEvictionManager
TTLEvictionStrategy = ttl_eviction_strategy.TTLEvictionStrategy
LRUEvictionStrategy = lru_eviction_strategy.LRUEvictionStrategy

load_dotenv()


async def main() -> None:
    """Demonstrate cache eviction lifecycle with TTL and LRU strategies."""
    # TTL eviction with async context manager
    store = ChromaDataStore(collection_name="eviction-cache").with_fulltext()

    strategy = TTLEvictionStrategy(ttl="10m")
    eviction_manager = AsyncIOEvictionManager(
        vector_store=store,
        eviction_strategy=strategy,
        check_interval=60,
    )
    cache = store.as_cache(eviction_manager=eviction_manager)

    async with cache:
        await cache.store("session:abc", "cached-session", ttl="10m")

    # LRU eviction with manual lifecycle
    strategy_lru = LRUEvictionStrategy(max_entries=1000)
    eviction_manager_lru = AsyncIOEvictionManager(
        vector_store=store,
        eviction_strategy=strategy_lru,
        check_interval=60,
    )
    cache_lru = store.as_cache(eviction_manager=eviction_manager_lru)

    await cache_lru.start()
    try:
        await cache_lru.store("quote:123", "cached quote")
    finally:
        await cache_lru.close()


if __name__ == "__main__":
    asyncio.run(main())
