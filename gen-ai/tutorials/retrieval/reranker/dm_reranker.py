"""Rerank chunks with a decisions-model relevance rubric.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/retrieval/reranker#rubric-based-reranking
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_retrieval.reranker import DMReranker


async def main() -> None:
    """Score and return the most relevant candidate chunk."""
    load_dotenv()
    chunks = [
        Chunk(content="Paris is the capital of France."),
        Chunk(content="Berlin is the capital of Germany."),
    ]
    reranker = DMReranker.from_config(model_id="openrouter/typesafe/jev-1.13", top_n=1)
    try:
        ranked = await reranker.rerank(chunks, "What is the capital of France?")
        for chunk in ranked:
            print(chunk.content, chunk.score)
    finally:
        await reranker.dm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
