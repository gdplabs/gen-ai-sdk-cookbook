"""Quickstart for the Decisions Model (DM) Invoker.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#quickstart
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import OpenRouterDMInvoker
from gllm_inference.schema import DMQuestion


async def main() -> None:
    """Ask a Noul question about customer state."""
    load_dotenv()
    invoker = OpenRouterDMInvoker(model_name="typesafe/jev-1.13")
    try:
        result = await invoker.invoke(
            state={"customer_message": "I would like to return my order."},
            questions={
                "refund_requested": DMQuestion.noul(
                    instructions="Is the customer requesting a refund?",
                ),
            },
        )
        print(result.answers["refund_requested"].noul)
    finally:
        await invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
