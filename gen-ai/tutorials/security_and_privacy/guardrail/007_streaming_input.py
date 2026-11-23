"""Stream input chunks through GuardrailManager.check_input_stream.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#checkinputstream-checkoutputstream
"""

import asyncio

from gllm_guardrail import GuardrailManager, PhraseMatcherEngine


async def source_chunks():
    """Yield sample input chunks."""
    for part in ["Hello, ", "this is ", "a safe message."]:
        yield part


async def main() -> None:
    """Run an input stream check and echo safe chunks."""
    engine = PhraseMatcherEngine(banned_phrases=["build a bomb"])
    guardrail = GuardrailManager(engine=engine)

    async for chunk in guardrail.check_input_stream(source_chunks()):
        if chunk.is_safe:
            print(chunk.chunk, end="")
        else:
            print(f"\nBlocked: {chunk.reason}")


if __name__ == "__main__":
    asyncio.run(main())
