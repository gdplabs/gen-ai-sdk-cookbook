import asyncio
from gllm_core.retry import retry, RetryConfig


async def slow_operation() -> str:
    await asyncio.sleep(10)
    return "done"


config = RetryConfig(max_retries=2, timeout=5.0)

try:
    result = await retry(slow_operation, retry_config=config)
except asyncio.TimeoutError:
    print("Operation timed out after 5 seconds")
