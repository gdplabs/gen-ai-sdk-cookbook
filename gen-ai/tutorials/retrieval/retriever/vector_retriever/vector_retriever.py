"""Example of using VectorRetriever for similarity search with ChromaDataStore.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/vector-retriever
"""

import asyncio

from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import VectorRetriever


async def main() -> None:
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    data_store = ChromaDataStore(
        collection_name="documents",
        client_type=ChromaClientType.MEMORY,
    ).with_vector(em_invoker=em_invoker)

    retriever = VectorRetriever(data_store=data_store)

    query = "What is machine learning?"
    results = await retriever.retrieve(query, top_k=10)

    results = await retriever.retrieve(
        "What is machine learning?",
        query_filter=F.eq("metadata.category", "AI"),
        top_k=10,
        threshold=0.8
    )

    batch_results = await retriever.retrieve(["query 1", "query 2"], top_k=10)


if __name__ == "__main__":
    asyncio.run(main())
