"""Retry: fallback across attempts.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/retry#fallback-across-attempts
"""

import asyncio

from gllm_core.fallback import execute_fallbacks


async def query_primary() -> str:
    """Simulate a slow primary operation."""
    raise TimeoutError("primary is slow")


async def query_backup() -> str:
    """Simulate a healthy backup operation."""
    return "answer from backup"


async def main() -> None:
    """Fall back to the backup operation when the primary one times out."""
    result = await execute_fallbacks(
        [query_primary, query_backup], fallback_on_exceptions=(TimeoutError,)
    )
    print(result)  # answer from backup


if __name__ == "__main__":
    asyncio.run(main())
