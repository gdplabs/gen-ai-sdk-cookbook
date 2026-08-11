"""Accessing the underlying HTTP client on a PERSISTENT invoker.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/client-lifecycle-management#accessing-the-underlying-client
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import ClientConfig, ClientLifecycle

load_dotenv()


async def main() -> None:
    """Read the live client instance off a PERSISTENT invoker."""
    lm_invoker = OpenAILMInvoker(
        OpenAILM.GPT_5_NANO,
        client_config=ClientConfig(lifecycle=ClientLifecycle.PERSISTENT),
    )

    try:
        await lm_invoker.invoke("What is the capital of France?")
        client = lm_invoker.client
        print(type(client))
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
