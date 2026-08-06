from gllm_retrieval.reranker import FlagEmbeddingReranker

reranker = FlagEmbeddingReranker(
    model_path="BAAI/bge-reranker-base",
    use_fp16=True,
)

reranked = await reranker.rerank(chunks, query)
