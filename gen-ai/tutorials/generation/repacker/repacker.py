"""Repacker quickstart: basic methods and modes.

Demonstrates forward (default), reverse, and sides methods with chunk and
context output modes.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/repacker#quickstart
"""

import asyncio

from gllm_core.schema import Chunk
from gllm_generation.repacker.repacker import Repacker


async def main() -> None:
    chunks = [
        Chunk(content="Intro"),
        Chunk(content="Middle"),
        Chunk(content="Conclusion"),
    ]

    # Forward (default): preserve original order
    repacker = Repacker()
    result = await repacker.repack(chunks)
    print("Forward:", [c.content for c in result])

    # Reverse: flip the order
    repacker = Repacker(method="reverse")
    result = await repacker.repack(chunks)
    print("Reverse:", [c.content for c in result])

    # Sides: alternate from ends to reduce lost-in-the-middle
    repacker = Repacker(method="sides", mode="chunk")
    result = await repacker.repack(chunks)
    print("Sides:", [c.content for c in result])

    # Context mode: return a single string
    repacker = Repacker(method="forward", mode="context", delimiter="\n---\n")
    context = await repacker.repack(chunks)
    print("Context mode:\n" + context)


if __name__ == "__main__":
    asyncio.run(main())
