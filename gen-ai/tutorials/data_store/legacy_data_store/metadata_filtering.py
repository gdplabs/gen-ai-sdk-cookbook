"""
Legacy Vector Data Store metadata filtering with retrieval_params.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/legacy/vector-data-store/quickstart-with-vector-data-store#metadata-filtering
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Apply metadata filtering on a legacy ChromaVectorDataStore."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    vector_store = ChromaVectorDataStore(
        collection_name="documents",
        embedding=em_invoker,
    )

    chunks = [
        Chunk(content="AI is the future.", metadata={"type": "document"}),
        Chunk(content="Parrot is a bird.", metadata={"type": "document"}),
    ]
    await vector_store.add_chunks(chunks)

    retrieval_params = {
        "filter": {
            "$and": [
                {"type": "document"},
            ]
        },
        "where_document": {"$contains": {"text": "AI"}},
    }

    results = await vector_store.query(
        query="artificial intelligence",
        retrieval_params=retrieval_params,
    )
    for chunk in results:
        print(f"  - {chunk.content}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
