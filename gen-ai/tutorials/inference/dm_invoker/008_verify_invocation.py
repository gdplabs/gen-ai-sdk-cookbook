"""Verify a model invocation.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#verify-invocations
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import TypeSafeDMInvoker


async def main() -> None:
    """Check that the model is reachable with the configured credentials."""
    load_dotenv()
    invoker = TypeSafeDMInvoker(model_name="jev-latest")
    try:
        result = await invoker.verify_invocation()

        if result.success:
            print(f"{result.model_id} is reachable in {result.duration:.2f}s")
        else:
            print(f"{result.model_id} failed: {result.error}")
    finally:
        await invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
