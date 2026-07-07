import asyncio
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_retrieval.reranker import SimilarityBasedReranker

em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)

# Create the reranker
reranker = SimilarityBasedReranker(embeddings=em_invoker)

# Sample chunks to rerank
chunks = [
    Chunk(id="1", content="Python is a programming language"),
    Chunk(id="2", content="Machine learning uses algorithms to learn from data"),
    Chunk(id="3", content="Deep learning is a subset of machine learning"),
]

# Rerank based on query relevance
query = "What is machine learning?"
reranked = asyncio.run(reranker.rerank(chunks, query))

for i, chunk in enumerate(reranked, 1):
    print(f"{i}. {chunk.content}")
