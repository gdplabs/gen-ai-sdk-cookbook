"""Configure portable and provider-specific thinking options.

GitBook: tutorials/inference/lm-invoker/thinking.md#portable-effort
"""

import asyncio

from gllm_inference.schema import ThinkingConfig


async def main() -> None:
    """Construct a thinking configuration with portable effort and provider options."""
    # Portable effort plus an OpenAI-specific thinking summary option
    thinking = ThinkingConfig(effort="high", kwargs={"summary": "auto"})
    print(thinking)


if __name__ == "__main__":
    asyncio.run(main())
