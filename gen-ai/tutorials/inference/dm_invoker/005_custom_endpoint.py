"""005: Target a custom OpenRouter-compatible endpoint for DM invocations.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#custom-endpoint
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import OpenRouterDMInvoker


async def main() -> None:
    """Initialize an OpenRouterDMInvoker pointed at a custom base URL."""
    load_dotenv()
    invoker = OpenRouterDMInvoker(
        model_name="typesafe/jev-1.13",
        model_kwargs={"base_url": "https://gateway.example.com/api"},
    )
    try:
        print(invoker.client_kwargs["base_url"])
    finally:
        await invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
