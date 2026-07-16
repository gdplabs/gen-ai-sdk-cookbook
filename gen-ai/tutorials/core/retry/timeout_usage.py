"""Timeout: setting an overall timeout for the entire retry operation.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/retry#timeout
"""

import asyncio

from gllm_core.retry import RetryConfig, retry


async def slow_operation() -> str:
    await asyncio.sleep(10)
    return "done"


async def main():
    config = RetryConfig(max_retries=2, timeout=5.0)

    try:
        result = await retry(slow_operation, retry_config=config)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out after 5 seconds")


if __name__ == "__main__":
    asyncio.run(main())
