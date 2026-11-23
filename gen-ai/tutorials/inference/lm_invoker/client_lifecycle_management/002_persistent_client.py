"""Persistent client lifecycle: a client is reused across calls, closed explicitly.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/client-lifecycle-management#persistent-client
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/client-lifecycle-management#release-resources-from-the-invoker-directly
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import ClientConfig, ClientLifecycle

load_dotenv()


async def main() -> None:
    """Invoke with a persistent client, then release it explicitly."""
    lm_invoker = OpenAILMInvoker(
        OpenAILM.GPT_5_NANO,
        client_config=ClientConfig(lifecycle=ClientLifecycle.PERSISTENT),
    )

    try:
        response = await lm_invoker.invoke("What is the capital of France?")
        print(response.content)
    finally:
        # e.g. in a FastAPI lifespan handler's `finally` block.
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
