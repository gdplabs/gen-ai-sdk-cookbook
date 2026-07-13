"""Example of using EnsembleRetriever to combine multiple retrieval strategies with weighted fusion.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/ensemble-retriever
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import VectorRetriever, FulltextRetriever, EnsembleRetriever


async def main() -> None:
    load_dotenv()

    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    vector_datastore = ChromaDataStore(
        collection_name="documents",
        client_type=ChromaClientType.MEMORY,
    ).with_vector(em_invoker=em_invoker)
    fulltext_datastore = ChromaDataStore(
        collection_name="documents",
        client_type=ChromaClientType.MEMORY,
    ).with_fulltext()

    vector_retriever = VectorRetriever(data_store=vector_datastore)
    fulltext_retriever = FulltextRetriever(data_store=fulltext_datastore)

    ensemble_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, fulltext_retriever],
        weights=[0.7, 0.3]
    )

    results = await ensemble_retriever.retrieve(
        "What is machine learning?",
        top_k=10
    )

    batch_results = await ensemble_retriever.retrieve(
        ["query 1", "query 2"],
        top_k=10
    )


if __name__ == "__main__":
    asyncio.run(main())
