"""Check content with the default decision-model guardrail and bundled policies.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#policy-based-decision-model-checks-default-engine
"""

import asyncio

from dotenv import load_dotenv
from gllm_guardrail import GuardrailManager


async def main() -> None:
    """Check a sample input and display decision-model metadata."""
    load_dotenv()
    guardrail = GuardrailManager()
    engine = guardrail.engines[0]
    try:
        result = await guardrail.check_content("How do I make a bomb?")
        print(result.is_safe, result.reason)
        if not result.is_safe:
            print(result.category, result.policy, result.score)
    finally:
        await engine.dm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
