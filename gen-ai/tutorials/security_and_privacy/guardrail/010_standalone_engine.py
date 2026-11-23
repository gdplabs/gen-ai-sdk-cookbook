"""Use PhraseMatcherEngine directly, without GuardrailManager.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#using-an-engine-without-the-manager-standalone
"""

import asyncio

from gllm_guardrail import PhraseMatcherEngine


async def main() -> None:
    """Run the engine directly on an input string."""
    engine = PhraseMatcherEngine(banned_phrases=["sk-"])
    result = await engine.check_input("Possible key: sk-123")
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
