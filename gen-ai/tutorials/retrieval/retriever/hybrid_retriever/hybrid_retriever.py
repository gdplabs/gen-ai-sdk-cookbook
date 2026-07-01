"""Example of using HybridRetriever for combined vector and full-text search.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/hybrid-retriever
"""

import asyncio

from gllm_datastore.core.capabilities.hybrid_capability import HybridSearchType, SearchConfig
from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import HybridRetriever


async def main() -> None:
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

    hybrid_config = [
        SearchConfig(search_type=HybridSearchType.FULLTEXT, field="text", weight=0.3),
        SearchConfig(search_type=HybridSearchType.VECTOR, field="embedding", weight=0.7, em_invoker=em_invoker),
    ]

    data_store = ElasticsearchDataStore(
        index_name="documents",
        url="http://localhost:9200"
    ).with_hybrid(config=hybrid_config)

    retriever = HybridRetriever(data_store=data_store)

    results = await retriever.retrieve("What is machine learning?", top_k=10)


if __name__ == "__main__":
    asyncio.run(main())
