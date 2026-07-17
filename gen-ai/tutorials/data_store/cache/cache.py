"""
Data Store as Cache: basic usage with decorator and direct operations.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/cache
"""

import asyncio
import json

from dotenv import load_dotenv
from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store import ChromaDataStore

load_dotenv()


async def main() -> None:
    """Use a data store as a cache with exact matching."""
    store = ChromaDataStore(collection_name="cache-store").with_fulltext()
    cache = store.as_cache()

    # Direct cache operations
    await cache.store(
        "orders:938",
        json.dumps({"status": "packed", "priority": "high"}),
        metadata={"tenant": "retail"},
    )

    result = await cache.retrieve("orders:938")
    print(f"Retrieved: {result}")

    await cache.delete("orders:938")

    # Filtered retrieval
    await cache.store(
        "faq:refund-policy",
        "Refunds are processed within 7 days.",
        metadata={"tenant": "retail"},
    )

    result = await cache.retrieve(
        "faq:refund-policy",
        filters=F.eq("metadata.tenant", "retail"),
    )
    print(f"Filtered cache result: {result}")

    await cache.clear()


if __name__ == "__main__":
    asyncio.run(main())
