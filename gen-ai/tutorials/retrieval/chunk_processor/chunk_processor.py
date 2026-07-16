"""Example of using DedupeChunkProcessor to remove duplicate chunks by id and content.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/chunk-processor
"""

import asyncio

from gllm_core.schema import Chunk
from gllm_retrieval.chunk_processor import DedupeChunkProcessor


async def main() -> None:
    chunks = [
        Chunk(id="chunk-1", content="Jakarta, Indonesia", metadata={"source": "source-1"}),
        Chunk(id="chunk-2", content="Kuala Lumpur, Malaysia", metadata={"source": "source-2"}),
        Chunk(id="chunk-3", content="Bangkok, Thailand", metadata={"source": "source-3"}),
        Chunk(id="chunk-1", content="Jakarta, Indonesia", metadata={"source": "source-1"}),  # Duplicate id with chunk-1
        Chunk(id="chunk-4", content="Kuala Lumpur, Malaysia", metadata={"source": "source-2"}),  # Duplicate content with chunk-2
    ]

    processor = DedupeChunkProcessor()
    result = await processor.process_chunks(chunks)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
