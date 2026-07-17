"""
Encryption in Data Store: transparent field-level encryption with AES-GCM.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/encryption
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_datastore.encryptor.aes_gcm_encryptor import AESGCMEncryptor
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Enable encryption on a Chroma data store and store/retrieve encrypted chunks."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

    # Generate a 256-bit key (32 bytes)
    encryption_key = os.urandom(32)
    encryptor = AESGCMEncryptor(key=encryption_key)

    store = (
        ChromaDataStore(
            collection_name="secure-docs",
            client_type=ChromaClientType.MEMORY,
        )
        .with_encryption(
            encryptor=encryptor,
            fields={"content", "metadata.secret_key"},
        )
        .with_fulltext()
        .with_vector(em_invoker=em_invoker)
    )

    # Create chunks with sensitive data
    chunks = [
        Chunk(
            id="doc-1",
            content="Sensitive medical record...",
            metadata={
                "role": "patient",
                "ssn": "000-00-0000",
                "secret_key": "classified",
            },
        )
    ]

    # Store (encryption happens automatically)
    await store.fulltext.create(chunks)

    # Retrieve using a plaintext field
    results = await store.fulltext.retrieve(
        filters=F.eq("metadata.role", "patient")
    )

    # Access data (decryption happens automatically)
    for chunk in results:
        print(f"Content: {chunk.content}")
        print(f"SSN: {chunk.metadata.get('ssn')}")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
