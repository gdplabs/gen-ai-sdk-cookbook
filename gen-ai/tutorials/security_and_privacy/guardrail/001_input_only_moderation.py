"""Quickstart: input-only moderation with PhraseMatcherEngine.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#1-input-only-moderation-string
"""

import asyncio

from gllm_guardrail import GuardrailManager, PhraseMatcherEngine


async def main() -> None:
    """Run input-only moderation against a sample phrase."""
    engine = PhraseMatcherEngine(banned_phrases=["secret password", "build a bomb"])
    guardrail = GuardrailManager(engine=engine)

    result = await guardrail.check_content("This contains a secret password.")
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
