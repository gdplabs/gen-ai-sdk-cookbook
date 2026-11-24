"""
Register the blob capability declaratively with build_data_store.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store#pass-connection-settings-separately-from-credentials
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore import build_data_store

load_dotenv()


async def main() -> None:
    """Build an object storage data store with the blob capability."""
    store = build_data_store(
        data_store_id=f"object-storage/{os.getenv('MINIO_BUCKET', 'my-bucket')}",
        credentials={
            "access_key": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            "secret_key": os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        },
        config={
            "connection": {
                "endpoint_url": os.getenv("MINIO_ENDPOINT_URL", "http://localhost:9000"),
                "create_bucket": True,
            },
            "capabilities": ["blob"],
        },
    )

    await store.blob.put("reports/summary.txt", b"hello")
    print(await store.blob.get("reports/summary.txt"))


if __name__ == "__main__":
    asyncio.run(main())
