"""Quickstart: output-only moderation with PhraseMatcherEngine.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#2-output-only-moderation
"""

import asyncio

from gllm_guardrail import (
    BaseGuardrailEngineConfig,
    GuardrailInput,
    GuardrailManager,
    GuardrailMode,
    PhraseMatcherEngine,
)


async def main() -> None:
    """Run output-only moderation against a sample response."""
    config = BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.OUTPUT_ONLY)
    engine = PhraseMatcherEngine(config=config, banned_phrases=["sk-"])
    guardrail = GuardrailManager(engine=engine)

    content = GuardrailInput(output="Leaked key: sk-1234567890", input=None)
    result = await guardrail.check_content(content)
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
