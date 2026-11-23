"""Exception handling: controlling which exceptions trigger retries.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/retry#exception-handling
"""

import asyncio

from gllm_core.retry import RetryConfig, retry


# Only retry on ValueError and RuntimeError
config_selective = RetryConfig(
    max_retries=2,
    retry_on_exceptions=(ValueError, RuntimeError),
)


# Never retry OSError; let it propagate immediately
config_non_retryable = RetryConfig(
    max_retries=3,
    retry_on_exceptions=(Exception,),
    non_retryable_exceptions=(ValueError, OSError),
)


async def flaky_task() -> str:
    """A task that may raise transient errors."""
    return "success"


async def main():
    # Using selective retry config
    result = await retry(flaky_task, retry_config=config_selective)
    print(f"Selective retry result: {result}")

    # Using non-retryable config
    result2 = await retry(flaky_task, retry_config=config_non_retryable)
    print(f"Non-retryable config result: {result2}")


if __name__ == "__main__":
    asyncio.run(main())
