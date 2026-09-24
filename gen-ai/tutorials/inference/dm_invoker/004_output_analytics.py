"""004: Read token usage and duration from DM output analytics.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#output-analytics
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import OpenRouterDMInvoker
from gllm_inference.schema import DMQuestion


async def main() -> None:
    """Print analytics only when the provider reports them."""
    load_dotenv()
    invoker = OpenRouterDMInvoker(model_name="typesafe/jev-1.13")
    try:
        result = await invoker.invoke(
            state="A customer asks to return an order.",
            questions={
                "refund": DMQuestion.noul(instructions="Is a refund requested?")
            },
        )
        if result.token_usage is not None:
            print("Input tokens:", result.token_usage.input_tokens)
            print("Output tokens:", result.token_usage.output_tokens)

        if result.duration is not None:
            print("Duration (seconds):", result.duration)
    finally:
        await invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
