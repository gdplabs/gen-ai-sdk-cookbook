"""Example of using PIIAwareRetriever for privacy-preserving search with automatic anonymization.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/pii-aware-retriever
"""

import asyncio

from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import PIIAwareRetriever
from gllm_retrieval.retriever.pii_resolver import MetadataPIIResolver


async def main() -> None:
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    try:
        data_store = ElasticsearchDataStore(
            index_name="documents"
        ).with_vector(em_invoker=em_invoker)

        pii_resolver = MetadataPIIResolver()

        retriever = PIIAwareRetriever(
            data_store=data_store,
            pii_resolver=pii_resolver,
            weights=[0.5, 0.5]
        )

        results = await retriever.retrieve(
            "What are the medical records for John Doe?",
            top_k=10
        )
    finally:
        await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
