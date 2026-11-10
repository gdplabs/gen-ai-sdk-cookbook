"""007: Bound the size of DM state and question text with a content policy.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#content-validation-and-transformation
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import TypeSafeDMInvoker
from gllm_inference.schema import ContentPolicy, DMQuestion, OnViolation, TextConstraint

content_policy = ContentPolicy(
    text=[
        # Truncate any text longer than 2000 characters.
        TextConstraint(max_size=2000),
        # Reject text shorter than 3 characters instead of transforming it.
        TextConstraint(min_size=3, on_violation=OnViolation.RAISE),
    ],
)

async def main() -> None:
    """Invoke a DM whose long state is truncated before the request is sent."""
    load_dotenv()
    invoker = TypeSafeDMInvoker(model_name="jev-latest", content_policy=content_policy)
    try:
        result = await invoker.invoke(
            state="A customer asks to return an order. " * 200,
            questions={
                "refund": DMQuestion.noul(instructions="Is a refund requested?")
            },
        )
        print(result.answers["refund"].noul)
    finally:
        await invoker.release_resources()

if __name__ == "__main__":
    asyncio.run(main())
