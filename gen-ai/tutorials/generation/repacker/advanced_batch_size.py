"""Repacker Advanced: batching with batch_size.

Demonstrates using batch_size to split input chunks into multiple batches
before ordering and shaping, instead of treating all chunks as one batch.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/repacker#advanced-batching-with-batch_size
"""

import asyncio

from gllm_core.schema import Chunk
from gllm_generation.repacker.repacker import Repacker


async def main() -> None:
    chunks = [Chunk(content=f"Chunk {i}") for i in range(5)]
    repacker = Repacker(method="forward", mode="chunk", batch_size=2)
    result = await repacker.repack(chunks)  # list[list[Chunk]], one list per batch
    for batch in result:
        print([c.content for c in batch])


if __name__ == "__main__":
    asyncio.run(main())
