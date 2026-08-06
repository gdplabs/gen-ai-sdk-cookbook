from gllm_retrieval.reranker import TEIReranker

reranker = TEIReranker(
    url="https://your-tei-endpoint.com/rerank",
    timeout=10,
    fallback_to_original=True,
)

reranked = await reranker.rerank(chunks, query)
