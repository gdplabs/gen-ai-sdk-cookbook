import asyncio
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import build_em_invoker
from gllm_generation.relevance_filter import SimilarityBasedRelevanceFilter

candidate_chunks = [
    Chunk(content="Indonesia is a country in Southeast Asia.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="Malaysia is a country in Southeast Asia.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="Singapore is a country in Southeast Asia.", metadata={"file_name": "singapore.txt"}),
    Chunk(content="The capital of Indonesia is Jakarta.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="The capital of Malaysia is Kuala Lumpur.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="The capital of Singapore is Singapore.", metadata={"file_name": "singapore.txt"}),
]
query = "In what part of Asia is Indonesia located? And what's its capital city?"

em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
relevance_filter = SimilarityBasedRelevanceFilter(em_invoker, threshold=0.6)
filtered_chunks = asyncio.run(relevance_filter.filter(chunks=candidate_chunks, query=query))
print(filtered_chunks)
