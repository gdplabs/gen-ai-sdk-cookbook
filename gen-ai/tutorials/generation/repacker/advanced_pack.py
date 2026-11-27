"""Repacker: handling over-budget chunks with pack.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/repacker#advanced-handling-over-budget-chunks-with-pack
"""

import asyncio

from gllm_core.schema import Chunk
from gllm_generation.repacker.repacker import Repacker


async def main() -> None:
    """Compare the truncate and keep strategies on over-budget chunks."""
    chunks = [
        Chunk(content=text) for text in ("aaaa", "bbbb", "cccc", "dddd")
    ]  # size 4 each

    # truncate, single batch: pops from the tail until the total (16) fits 9
    repacker = Repacker(pack="truncate", size_limit=9)
    result = await repacker.repack(chunks)
    print([c.content for c in result])  # ['aaaa', 'bbbb']

    # truncate, batch_size=2: each batch is trimmed on its own
    repacker = Repacker(pack="truncate", size_limit=5, batch_size=2)
    result = await repacker.repack(chunks)
    print([[c.content for c in batch] for batch in result])  # [['aaaa'], ['cccc']]

    # keep: nothing is dropped; one warning is logged because the batch (16) exceeds 9
    repacker = Repacker(pack="keep", size_limit=9)
    result = await repacker.repack(chunks)
    print([c.content for c in result])  # ['aaaa', 'bbbb', 'cccc', 'dddd']


if __name__ == "__main__":
    asyncio.run(main())
