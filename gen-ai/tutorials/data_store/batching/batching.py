"""
Automated batching: configure default_batch_size during capability registration.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/batching
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store import MilvusDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Configure automated batching with MilvusDataStore."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

    store = (
        MilvusDataStore(
            collection_name="my_collection",
            uri="http://localhost:19530",
        )
        .with_vector(
            em_invoker=em_invoker,
            default_batch_size=100,
        )
    )

    huge_list_of_chunks = [
        Chunk(id=f"chunk-{i}", content=f"Document content {i}")
        for i in range(10)
    ]
    await store.vector.create(huge_list_of_chunks)

    # Per-call batch size override
    await store.vector.create(huge_list_of_chunks, batch_size=50)

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
