"""Example of using ParentDocumentRetriever for retrieving child chunks with parent context.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/parent-document-retriever
"""

import asyncio

from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import ParentDocumentRetriever


async def main() -> None:
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    child_store = ElasticsearchDataStore(
        index_name="child_chunks"
    ).with_vector(em_invoker=em_invoker)

    parent_store = ElasticsearchDataStore(
        index_name="parent_chunks"
    ).with_fulltext()

    retriever = ParentDocumentRetriever(
        child_data_store=child_store,
        parent_data_store=parent_store,
        parent_metadata_field="parent_chunk_id"
    )

    results = await retriever.retrieve(
        "What is machine learning?",
        top_k=5
    )


if __name__ == "__main__":
    asyncio.run(main())
