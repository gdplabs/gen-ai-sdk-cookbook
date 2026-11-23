"""Decorator usage: @retry() on async, sync, and class methods.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/retry#decorator-usage
"""

import asyncio

from gllm_core.retry import RetryConfig, retry


# Parameterless — uses default config (no retries unless overridden)
@retry()
async def get_data(id: str) -> dict:
    return {"id": id, "data": "value"}


# With custom config
@retry(RetryConfig(max_retries=3, timeout=120))
async def fetch_with_timeout(query: str) -> list:
    return [f"result for {query}"]


# Works on sync functions too
@retry()
def calculate(x: int) -> int:
    return x * 2


# Works on class methods
class DataService:
    @retry(RetryConfig(max_retries=2))
    async def get_data(self, id: str) -> dict:
        return {"id": id, "data": "test"}


async def main():
    # Async decorated function
    result = await get_data("abc")
    print(f"get_data: {result}")

    # With custom config
    results = await fetch_with_timeout("hello")
    print(f"fetch_with_timeout: {results}")

    # Sync function
    print(f"calculate: {calculate(5)}")

    # Class method
    service = DataService()
    data = await service.get_data("xyz")
    print(f"DataService.get_data: {data}")


if __name__ == "__main__":
    asyncio.run(main())
