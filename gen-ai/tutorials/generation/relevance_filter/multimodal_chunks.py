"""Relevance Filter: multimodal chunks.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/relevance-filter#multimodal-chunks
"""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_generation.relevance_filter import LMRelevanceFilter


async def main() -> None:
    """Judge an image chunk and a text chunk together."""
    load_dotenv()
    image = Path(__file__).parent / "data" / "dog.png"
    candidate_chunks = [
        Chunk(content=image.read_bytes(), metadata={"file_name": "dog.png"}),
        Chunk(
            content="Jakarta is the capital of Indonesia.",
            metadata={"file_name": "indonesia.txt"},
        ),
    ]

    relevance_filter = LMRelevanceFilter.from_preset("openai/gpt-5-nano")
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query="Which animal is shown?"
        )
        print(filtered_chunks)
    finally:
        await relevance_filter.lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
