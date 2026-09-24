"""Ask Noul, Choice, and Score questions in one DM invocation.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#question-types-and-answers
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import OpenRouterDMInvoker
from gllm_inference.schema import DMQuestion


async def main() -> None:
    """Print typed answers for several questions about the same state."""
    load_dotenv()
    invoker = OpenRouterDMInvoker(model_name="typesafe/jev-1.13")
    try:
        result = await invoker.invoke(
            state={"customer_message": "I need my order refunded as soon as possible."},
            questions={
                "refund_requested": DMQuestion.noul(
                    instructions="Is the customer requesting a refund?",
                ),
                "request_type": DMQuestion.choice(
                    instructions="Classify the customer's request.",
                    criteria={
                        "refund": "The customer wants their money returned.",
                        "exchange": "The customer wants a replacement item.",
                        "other": "The request is neither a refund nor an exchange.",
                    },
                ),
                "urgency": DMQuestion.score(
                    instructions=(
                        "Score how urgently the customer needs help, from 0 to 2."
                    ),
                    criteria=[
                        "0: Low urgency; no time-sensitive need.",
                        "1: Medium urgency; the customer would prefer a "
                        "prompt response.",
                        "2: High urgency; the customer needs immediate assistance.",
                    ],
                ),
            },
        )
        print(result.answers)
    finally:
        await invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
