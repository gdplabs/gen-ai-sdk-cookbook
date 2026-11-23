"""Quickstart: retry decorator and direct execution.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/retry#quickstart
"""

import asyncio

from gllm_core.retry import RetryConfig, retry


@retry()
async def fetch_data(url: str) -> dict:
    """Simulate an unreliable API call that may raise transient errors."""
    # In a real application, this would be an HTTP request
    return {"url": url, "data": "response"}


async def unreliable_call(user_id: str) -> dict:
    """Another function that may raise transient errors."""
    return {"user_id": user_id, "name": "John Doe"}


async def main():
    # Decorator usage: retry is applied automatically
    result = await fetch_data("https://api.example.com/data")
    print(f"Decorator result: {result}")

    # Direct execution: pass function and arguments to retry()
    config = RetryConfig(max_retries=2, base_delay=0.5)
    result2 = await retry(unreliable_call, "user_123", retry_config=config)
    print(f"Direct result: {result2}")


if __name__ == "__main__":
    asyncio.run(main())
