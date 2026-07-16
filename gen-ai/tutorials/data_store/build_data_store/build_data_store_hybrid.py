"""
Build a data store with hybrid search from declarative configuration.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/build-data-store#configure-hybrid-search
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore import build_data_store

load_dotenv()


async def main() -> None:
    """Configure hybrid search via build_data_store."""
    store = build_data_store(
        data_store_id="elasticsearch/customer-notes",
        credentials=os.environ.get("ELASTICSEARCH_API_KEY"),
        config={
            "connection": {"url": "http://localhost:9200"},
            "capabilities": ["hybrid"],
            "vector": {
                "em_invoker_config": {
                    "model_id": "openai/text-embedding-3-small",
                    "credentials": os.environ["OPENAI_API_KEY"],
                }
            },
            "hybrid": {
                "config": [
                    {"search_type": "fulltext", "field": "content", "weight": 0.3},
                    {"search_type": "vector", "field": "embedding", "weight": 0.7},
                ]
            },
        },
    )

    results = await store.hybrid.retrieve("orders ready for pickup")
    for chunk in results:
        print(f"  - {chunk.content}")


if __name__ == "__main__":
    asyncio.run(main())
