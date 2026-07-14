"""Example of using HierarchicalRetriever for progressive multi-level document retrieval.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/hierarchical-retriever
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import VectorRetriever
from gllm_retrieval.retriever.hierarchical_retriever import (
    HierarchicalRetriever,
    HierarchicalRetrieverConfig,
    LevelConfig,
    ConstraintMode
)


async def main() -> None:
    load_dotenv()

    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    try:
        document_store = ChromaDataStore(
            collection_name="documents",
            client_type=ChromaClientType.MEMORY,
        ).with_vector(em_invoker=em_invoker)
        chunk_store = ChromaDataStore(
            collection_name="chunks",
            client_type=ChromaClientType.MEMORY,
        ).with_vector(em_invoker=em_invoker)

        document_retriever = VectorRetriever(data_store=document_store)
        chunk_retriever = VectorRetriever(data_store=chunk_store)

        config = HierarchicalRetrieverConfig(
            levels=[
                LevelConfig(
                    name="document",
                    retriever=document_retriever,
                    top_k=5,
                    filter_key="document_id",
                    constrain_by=None
                ),
                LevelConfig(
                    name="chunk",
                    retriever=chunk_retriever,
                    top_k=10,
                    filter_key="document_id",
                    constrain_by=ConstraintMode.PREVIOUS
                )
            ],
            output_level="chunk"
        )

        retriever = HierarchicalRetriever(config=config)

        results = await retriever.retrieve("What is machine learning?")
    finally:
        await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
