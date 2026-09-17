"""Stream output chunks through GuardrailManager.check_output_stream.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#checkinputstream-checkoutputstream
"""

import asyncio

from gllm_guardrail import (
    BaseGuardrailEngineConfig,
    GuardrailManager,
    GuardrailMode,
    PhraseMatcherEngine,
)


async def response_chunks():
    """Yield sample response chunks."""
    for part in ["Here is ", "your answer."]:
        yield part


async def main() -> None:
    """Run an output stream check with an OUTPUT_ONLY engine."""
    config = BaseGuardrailEngineConfig(guardrail_mode=GuardrailMode.OUTPUT_ONLY)
    engine = PhraseMatcherEngine(config=config, banned_phrases=["sk-"])
    guardrail = GuardrailManager(engine=engine)

    async for chunk in guardrail.check_output_stream(response_chunks()):
        if chunk.is_safe:
            print(chunk.chunk, end="")
        else:
            print(f"\nBlocked: {chunk.reason}")


if __name__ == "__main__":
    asyncio.run(main())
