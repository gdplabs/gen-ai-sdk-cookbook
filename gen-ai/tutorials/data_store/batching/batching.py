"""Example of using batched operations with MilvusDataStore.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/batching
"""

import asyncio

from gllm_datastore.data_store import MilvusDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker


async def main() -> None:
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

    await store.vector.create(huge_list_of_chunks)


if __name__ == "__main__":
    asyncio.run(main())
