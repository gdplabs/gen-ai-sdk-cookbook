"""
Build a data store from declarative configuration using build_data_store.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store#build-a-data-store-from-configuration
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore import (
    DataStoreConfig,
    EMInvokerConfig,
    VectorConfig,
    build_data_store,
)

load_dotenv()


async def main() -> None:
    """Build a data store from configuration and use it."""
    # Simple in-memory store with default fulltext capability
    store = build_data_store(data_store_id="in-memory/default")

    await store.fulltext.create(
        Chunk(
            id="note-1",
            content="Order 938 is ready for pickup",
            metadata={"status": "ready"},
        )
    )

    results = await store.fulltext.retrieve()
    print("Default fulltext results:")
    for chunk in results:
        print(f"  - {chunk.content}")

    # Typed configuration with vector capability
    config = DataStoreConfig(
        capabilities=["fulltext", "vector"],
        vector=VectorConfig(
            em_invoker_config=EMInvokerConfig(
                model_id="openai/text-embedding-3-small",
                credentials=os.environ["OPENAI_API_KEY"],
            ),
        ),
    )

    store_typed = build_data_store(
        data_store_id="in-memory/default",
        config=config,
    )

    await store_typed.fulltext.create(
        Chunk(
            id="note-2",
            content="Order 939 is ready for pickup",
            metadata={"status": "ready"},
        )
    )

    semantic_results = await store_typed.vector.retrieve(
        query="orders ready for pickup"
    )
    print("\nVector results:")
    for chunk in semantic_results:
        print(f"  - {chunk.content}")


if __name__ == "__main__":
    asyncio.run(main())
