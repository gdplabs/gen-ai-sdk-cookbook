"""Example of using SimilarityReranker to reorder chunks by query relevance.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/reranker
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_retrieval.reranker import SimilarityReranker


async def main() -> None:
    """Rerank chunks by embedding similarity to a query."""
    load_dotenv()

    em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)
    try:
        reranker = SimilarityReranker(em_invoker=em_invoker)

        chunks = [
            Chunk(id="1", content="Python is a programming language"),
            Chunk(
                id="2", content="Machine learning uses algorithms to learn from data"
            ),
            Chunk(id="3", content="Deep learning is a subset of machine learning"),
        ]

        query = "What is machine learning?"
        reranked = await reranker.rerank(chunks, query)

        for i, chunk in enumerate(reranked, 1):
            print(f"{i}. {chunk.content}")
    finally:
        await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
