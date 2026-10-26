"""Relevance Filter: filtering chunks with a language model (LM).

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/relevance-filter#filtering-with-an-lm
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_generation.relevance_filter import LMRelevanceFilter
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

candidate_chunks = [
    Chunk(
        content="Indonesia is a country in Southeast Asia.",
        metadata={"file_name": "indonesia.txt"},
    ),
    Chunk(
        content="Malaysia is a country in Southeast Asia.",
        metadata={"file_name": "malaysia.txt"},
    ),
]
query = "In what part of Asia is Indonesia located?"


async def main() -> None:
    """Filter chunks with an LM filter built from a preset and from an invoker."""
    relevance_filter = LMRelevanceFilter.from_preset("openai/gpt-5-nano")
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query=query
        )
        print([chunk.content for chunk in filtered_chunks])
    finally:
        await relevance_filter.lm_invoker.release_resources()

    lm_invoker = build_lm_invoker(model_id="openai/gpt-5-nano")
    relevance_filter = LMRelevanceFilter(
        lm_invoker=lm_invoker, batch_size=5, on_failure_keep_all=True
    )
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query=query
        )
        print([chunk.content for chunk in filtered_chunks])
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
