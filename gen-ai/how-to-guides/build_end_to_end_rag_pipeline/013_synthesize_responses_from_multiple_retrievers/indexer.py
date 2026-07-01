"""Example script to index internal chunks into a vector store.

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/synthesize-responses-from-multiple-retrievers
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()


def create_internal_retriever() -> VectorRetriever:
    embedding_model = OpenAIEMInvoker(
        model_name=os.environ["EMBEDDING_MODEL"],
        api_key=os.environ["OPENAI_API_KEY"],
    )

    data_store = ChromaDataStore(
        collection_name="internal_research_docs",
        client_type=ChromaClientType.PERSISTENT,
        persist_directory="data/chroma",
    ).with_vector(em_invoker=embedding_model)

    return VectorRetriever(data_store)


async def ingest_internal_data(vector_retriever: VectorRetriever) -> None:
    chunks = [
        Chunk(
            id="internal-pipeline-overview",
            content="GL SDK pipelines orchestrate steps, parallel branches, and response synthesis.",
            metadata={"source": "internal-docs"},
        ),
        Chunk(
            id="internal-vector-search",
            content="VectorRetriever searches ChromaDB for internal chunks that match a user query.",
            metadata={"source": "internal-docs"},
        ),
        Chunk(
            id="internal-response-synthesis",
            content="ResponseSynthesizer generates an answer from retrieved context chunks.",
            metadata={"source": "internal-docs"},
        ),
    ]
    await vector_retriever.data_store.vector.create(chunks)
    print(f"Successfully indexed {len(chunks)} internal documents")


if __name__ == "__main__":
    asyncio.run(ingest_internal_data(create_internal_retriever()))
