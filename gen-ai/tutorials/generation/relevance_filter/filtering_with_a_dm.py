"""Relevance Filter: filtering chunks with a decision model (DM).

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/relevance-filter#filtering-with-a-dm
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_generation.relevance_filter import DMRelevanceFilter

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
    Chunk(
        content="The capital of Indonesia is Jakarta.",
        metadata={"file_name": "indonesia.txt"},
    ),
]
query = "In what part of Asia is Indonesia located? And what's its capital city?"


async def main() -> None:
    """Keep only the chunks a DM judges relevant to the query."""
    relevance_filter = DMRelevanceFilter.from_config(
        model_id="openrouter/typesafe/jev-1.13", threshold=0.6
    )
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query=query
        )
        print([chunk.content for chunk in filtered_chunks])
    finally:
        await relevance_filter.dm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
