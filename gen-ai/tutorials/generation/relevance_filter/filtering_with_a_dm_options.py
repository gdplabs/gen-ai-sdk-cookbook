"""Relevance Filter: customizing DMRelevanceFilter.

Start with filtering_with_a_dm.py for the basic example. This script shows the
options you can add on top of it. Each function below is independent, so you can
copy just the one you need.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/relevance-filter#filtering-with-a-dm
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk, ContextConfig
from gllm_generation.relevance_filter import DMRelevanceFilter
from gllm_inference.dm_invoker import build_dm_invoker
from gllm_inference.schema import DMQuestion

load_dotenv()

MODEL_ID = "openrouter/typesafe/jev-1.13"

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


async def with_existing_dm_invoker() -> None:
    """Option 1: pass a DM invoker you already built instead of a model ID."""
    dm_invoker = build_dm_invoker(model_id=MODEL_ID)
    relevance_filter = DMRelevanceFilter(dm_invoker=dm_invoker, threshold=0.5)
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query=query
        )
        print("\n[1. existing DM invoker]")
        print([chunk.content for chunk in filtered_chunks])
    finally:
        await dm_invoker.release_resources()


async def with_custom_question() -> None:
    """Option 2: replace the default yes/no question with your own."""
    question = DMQuestion.noul(
        instructions="Does this chunk mention a country's capital city?",
        criteria={
            "true": "The chunk names the capital city of a country.",
            "false": "The chunk does not name a capital city.",
        },
    )
    relevance_filter = DMRelevanceFilter.from_config(
        model_id=MODEL_ID, relevance_question=question
    )
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query=query
        )
        print("\n[2. custom relevance_question]")
        print([chunk.content for chunk in filtered_chunks])
    finally:
        await relevance_filter.dm_invoker.release_resources()


async def with_batching() -> None:
    """Option 3: set how many chunks go in each call and how many calls run at once."""
    relevance_filter = DMRelevanceFilter.from_config(
        model_id=MODEL_ID, batch_size=10, max_concurrency=3
    )
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query=query
        )
        print("\n[3. batch_size and max_concurrency]")
        print([chunk.content for chunk in filtered_chunks])
    finally:
        await relevance_filter.dm_invoker.release_resources()


async def with_context_config() -> None:
    """Option 4: show the model the file name together with the chunk content."""
    relevance_filter = DMRelevanceFilter.from_config(
        model_id=MODEL_ID,
        context_config=ContextConfig(
            fields=["content", "metadata"], metadata_keys=["file_name"]
        ),
    )
    try:
        filtered_chunks = await relevance_filter.filter(
            chunks=candidate_chunks, query=query
        )
        print("\n[4. context_config]")
        print([chunk.content for chunk in filtered_chunks])
    finally:
        await relevance_filter.dm_invoker.release_resources()


async def main() -> None:
    """Run every option one after another."""
    await with_existing_dm_invoker()
    await with_custom_question()
    await with_batching()
    await with_context_config()


if __name__ == "__main__":
    asyncio.run(main())
