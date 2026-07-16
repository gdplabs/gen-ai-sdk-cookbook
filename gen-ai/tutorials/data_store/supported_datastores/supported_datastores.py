"""
Supported Datastores: initialize a Chroma data store with persistent client.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/supported-datastores
"""

import asyncio

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Initialize a Chroma data store with persistent client type."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

    store = (
        ChromaDataStore(
            collection_name="my_collection",
            client_type=ChromaClientType.PERSISTENT,
            persist_directory="./chroma-data",
        )
        .with_fulltext()
        .with_vector(em_invoker=em_invoker)
    )

    # The rest of your code stays the same regardless of backend
    results = await store.fulltext.retrieve()
    print(f"Retrieved {len(results)} chunks")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
