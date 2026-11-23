"""
Cache decorator usage: memoize expensive functions with @cache.cache().

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/cache#decorator-usage
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.cache import MatchingStrategy
from gllm_datastore.data_store import ChromaDataStore

load_dotenv()

call_count = 0


async def user_service_fetch_profile(user_id: str) -> dict:
    """Simulate an expensive profile fetch."""
    await asyncio.sleep(0.1)
    return {"user_id": user_id, "name": "Alice", "email": "alice@example.com"}


async def support_agent_answer(question: str) -> str:
    """Simulate an expensive LLM call."""
    await asyncio.sleep(0.1)
    return f"Answer to: {question}"


async def main() -> None:
    """Use @cache.cache() decorator for memoization."""
    store = ChromaDataStore(collection_name="decorator-cache").with_fulltext()
    cache = store.as_cache(matching_strategy=MatchingStrategy.EXACT)

    @cache.cache()
    async def get_user_profile(user_id: str) -> dict:
        return await user_service_fetch_profile(user_id)

    first = await get_user_profile("user-123")
    print(f"First call: {first}")

    second = await get_user_profile("user-123")
    print(f"Second call (cached): {second}")

    # Custom cache key
    def user_profile_key(user_id: str) -> str:
        return f"user-profile:{user_id}"

    @cache.cache(key_func=user_profile_key)
    async def get_user_profile_custom_key(user_id: str) -> dict:
        return await user_service_fetch_profile(user_id)

    result = await get_user_profile_custom_key("user-456")
    print(f"Custom key result: {result}")

    # Named cache key prefix
    @cache.cache(name="pricing-quote")
    async def calculate_quote(customer_id: str, product_id: str) -> dict:
        return {"quote": f"Quote for {customer_id}/{product_id}"}

    quote = await calculate_quote("cust-1", "prod-2")
    print(f"Quote: {quote}")

    # Per-function matching and eviction settings
    @cache.cache(
        matching_strategy=MatchingStrategy.FUZZY,
        eviction_config={"ttl": "10m"},
    )
    async def answer_support_question(question: str) -> str:
        return await support_agent_answer(question)

    answer = await answer_support_question("How do I reset my password?")
    print(f"Support answer: {answer}")

    await cache.clear()


if __name__ == "__main__":
    asyncio.run(main())
