"""
Legacy Vector Data Store quickstart: save and retrieve data with ChromaVectorDataStore.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/legacy/vector-data-store/quickstart-with-vector-data-store
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Use legacy ChromaVectorDataStore to add chunks and query by similarity."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    vector_store = ChromaVectorDataStore(
        collection_name="documents",
        embedding=em_invoker,
    )

    chunks = [
        Chunk(content="AI is the future."),
        Chunk(content="Parrot is a bird."),
    ]
    await vector_store.add_chunks(chunks)

    results = await vector_store.query(query="artificial intelligence")
    for chunk in results:
        print(f"  - {chunk.content}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
