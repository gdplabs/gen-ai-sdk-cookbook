from gllm_retrieval.reranker import CohereBedrockReranker

reranker = CohereBedrockReranker(
    model_name="cohere.rerank-v3-5:0",
    region_name="us-east-1",
    fallback_to_original=True,
)

reranked = await reranker.rerank(chunks, query)
