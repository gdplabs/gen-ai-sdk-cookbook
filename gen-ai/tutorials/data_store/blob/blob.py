"""
Store and read raw bytes with the blob capability.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store#8-blob-methods
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore.data_store.object_storage.data_store import ObjectStorageDataStore

load_dotenv()


async def main() -> None:
    """Put an object, check it exists, and read it back with its metadata."""
    store = ObjectStorageDataStore(
        endpoint_url=os.getenv("MINIO_ENDPOINT_URL", "http://localhost:9000"),
        bucket_name=os.getenv("MINIO_BUCKET", "my-bucket"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        create_bucket=True,
    ).with_blob()

    pdf_bytes = b"%PDF-1.4 example bytes"
    await store.blob.put(
        "reports/2026/summary.pdf",
        pdf_bytes,
        content_type="application/pdf",
        metadata={"author": "jakarta-team"},
    )

    blob = await store.blob.get_with_metadata("reports/2026/summary.pdf")
    if blob is not None:
        print(blob.content_type, blob.metadata)

    print(await store.blob.exists("reports/2026/summary.pdf"))


if __name__ == "__main__":
    asyncio.run(main())
