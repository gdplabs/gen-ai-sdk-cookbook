from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_retrieval.reranker import SimilarityBasedReranker

em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)
reranker = SimilarityBasedReranker(embeddings=em_invoker)

reranked = await reranker.rerank(chunks, query)
