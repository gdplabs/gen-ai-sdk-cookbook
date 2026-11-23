"""Repacker Advanced: size limits and custom size functions.

Demonstrates using size_func and size_limit to trim from the end before
reordering, with a custom token-estimation metric.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/repacker#advanced-size-limits-and-custom-size-functions
"""

import asyncio

from gllm_core.schema import Chunk
from gllm_generation.repacker.repacker import Repacker


def rough_token_count(chunk: Chunk) -> int:
    # Extremely rough token estimate: words * 1.3
    return int(len(str(chunk.content).split()) * 1.3)


async def main() -> None:
    chunks = [
        Chunk(content="Short intro."),
        Chunk(content="Detailed middle section with more words."),
        Chunk(content="Final notes."),
    ]
    repacker = Repacker(
        method="sides",
        mode="context",
        delimiter="\n\n",
        size_func=rough_token_count,
        size_limit=10,
    )
    context = await repacker.repack(chunks)
    print(context)


if __name__ == "__main__":
    asyncio.run(main())
