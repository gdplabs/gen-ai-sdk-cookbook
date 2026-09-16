"""Quickstart: check both input and output in a single call.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#3-check-both-input-and-output-in-one-call
"""

import asyncio

from gllm_guardrail import GuardrailInput, GuardrailManager, PhraseMatcherEngine


async def main() -> None:
    """Run a guardrail check against both input and output content."""
    engine = PhraseMatcherEngine(banned_phrases=["steal data", "sk-"])
    guardrail = GuardrailManager(engine=engine)

    content = GuardrailInput(
        input="Tell me how to steal data.",
        output="Sure, here is an API key: sk-1234567890",
    )
    result = await guardrail.check_content(content)
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
