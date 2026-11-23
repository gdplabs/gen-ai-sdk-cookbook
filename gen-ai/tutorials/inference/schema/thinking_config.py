"""Construct a ThinkingConfig schema.

GitBook: tutorials/inference/schema.md#thinkingconfig
"""

import asyncio

from gllm_inference.schema.config import ThinkingConfig


async def main() -> None:
    """Construct a thinking configuration with provider-specific options."""
    config = ThinkingConfig(
        enabled=True,                # bool -- defaults to True
        effort="high",               # str | None -- provider-validated portable effort
        kwargs={"summary": "auto"},  # dict[str, Any] -- provider-specific options
    )
    print(config)


if __name__ == "__main__":
    asyncio.run(main())
