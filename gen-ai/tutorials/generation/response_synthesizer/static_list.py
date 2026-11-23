"""Response Synthesizer: Static List Strategy.

Demonstrates the Static List strategy for formatting context items without
using a language model. Includes both default and custom format_response_func.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#id-3.-static-list
"""

import asyncio

from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_generation.response_synthesizer.strategy import StaticListSynthesisStrategy


async def main() -> None:
    chunks = [
        Chunk(content="Python is a high-level programming language."),
        Chunk(content="Python was created by Guido van Rossum."),
        Chunk(content="Python is known for its readability."),
    ]

    # --- Default formatter ---
    strategy = StaticListSynthesisStrategy()
    synthesizer = ResponseSynthesizer(strategy=strategy)
    response = await synthesizer.synthesize(chunks=chunks)
    print("=== Default formatter ===")
    print(response)

    # --- Custom format_response_func, passed at strategy construction ---
    def format_chunks(items: list[str]) -> str:
        if not items:
            return "No content available."
        return "### Retrieved Information:\n" + "\n".join(
            f"- {item}" for item in items
        )

    custom_strategy = StaticListSynthesisStrategy(format_response_func=format_chunks)
    custom_synthesizer = ResponseSynthesizer(strategy=custom_strategy)
    response = await custom_synthesizer.synthesize(chunks=chunks)
    print("\n=== Custom formatter ===")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
