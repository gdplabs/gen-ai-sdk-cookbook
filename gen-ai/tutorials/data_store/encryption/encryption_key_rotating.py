"""
Key Rotating Encryptor: encryption with key rotation support.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/encryption#key-rotating-encryptor
"""

import os

from dotenv import load_dotenv
from gllm_datastore.encryptor.aes_gcm_encryptor import AESGCMEncryptor
from gllm_datastore.encryptor.key_ring.in_memory_key_ring import InMemoryKeyRing
from gllm_datastore.encryptor.key_rotating_encryptor import KeyRotatingEncryptor

load_dotenv()


def main() -> None:
    """Create a key rotating encryptor with multiple keys."""
    key_ring = InMemoryKeyRing()
    key_ring.add("key_v1", AESGCMEncryptor(key=os.urandom(32)))
    key_ring.add("key_v2", AESGCMEncryptor(key=os.urandom(32)))

    encryptor = KeyRotatingEncryptor(
        key_ring=key_ring,
        active_key_id="key_v1",
    )
    print(f"Active key: {encryptor.active_key_id}")


if __name__ == "__main__":
    main()
