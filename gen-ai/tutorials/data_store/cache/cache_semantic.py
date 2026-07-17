"""
Semantic cache retrieval using vector capability.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/cache#semantic-retrieval
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.cache import MatchingStrategy
from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Use semantic matching for cache lookups."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    store = (
        ChromaDataStore(collection_name="semantic-cache")
        .with_fulltext()
        .with_vector(em_invoker=em_invoker)
    )
    cache = store.as_cache(matching_strategy=MatchingStrategy.SEMANTIC)

    await cache.store(
        "How do I request a refund?",
        "Open a support ticket with your order ID.",
    )
    result = await cache.retrieve(
        "What is the process for getting my money back?",
        matching_strategy=MatchingStrategy.SEMANTIC,
        min_similarity=0.8,
    )
    print(f"Semantic cache result: {result}")

    await cache.clear()
    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
