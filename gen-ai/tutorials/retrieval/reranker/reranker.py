import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_retrieval.reranker import SimilarityBasedReranker

load_dotenv()


async def main() -> None:
    em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)
    reranker = SimilarityBasedReranker(embeddings=em_invoker)

    chunks = [
        Chunk(id="1", content="Python is a programming language"),
        Chunk(id="2", content="Machine learning uses algorithms to learn from data"),
        Chunk(id="3", content="Deep learning is a subset of machine learning"),
    ]

    query = "What is machine learning?"
    reranked = await reranker.rerank(chunks, query)

    for i, chunk in enumerate(reranked, 1):
        print(f"{i}. {chunk.content}")


if __name__ == "__main__":
    asyncio.run(main())
