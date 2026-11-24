"""
Configure the blob capability with a custom HTTP client.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store#custom-http-client-for-blob-storage
"""

import asyncio
import os

import urllib3
from dotenv import load_dotenv
from gllm_datastore.data_store.object_storage.data_store import ObjectStorageDataStore

load_dotenv()


async def main() -> None:
    """Pass a urllib3 pool as http_client and use the blob capability through it."""
    http_client = urllib3.PoolManager(
        timeout=urllib3.Timeout(connect=5.0, read=30.0),
        retries=urllib3.Retry(total=3, backoff_factor=0.5),
    )
    # For a private CA over HTTPS, also pass cert_reqs and ca_certs to the pool.

    store = ObjectStorageDataStore(
        endpoint_url=os.getenv("MINIO_ENDPOINT_URL", "http://localhost:9000"),
        bucket_name=os.getenv("MINIO_BUCKET", "my-bucket"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        create_bucket=True,
        http_client=http_client,
    ).with_blob()

    await store.blob.put("http-client/hello.txt", b"hello")
    print(await store.blob.get("http-client/hello.txt"))


if __name__ == "__main__":
    asyncio.run(main())
