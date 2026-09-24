"""Configure retry behavior and timeout for DM invocations.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#retry-and-timeout
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.retry import RetryConfig
from gllm_inference.dm_invoker import OpenRouterDMInvoker
from gllm_inference.schema import DMQuestion


async def main() -> None:
    """Invoke a DM with an explicit retry policy and request timeout."""
    load_dotenv()
    invoker = OpenRouterDMInvoker(
        model_name="typesafe/jev-1.13",
        retry_config=RetryConfig(max_retries=3, timeout=60.0),
    )
    try:
        result = await invoker.invoke(
            state="A customer asks to return an order.",
            questions={
                "refund": DMQuestion.noul(instructions="Is a refund requested?")
            },
        )
        print(result.answers["refund"].noul)
    finally:
        await invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
