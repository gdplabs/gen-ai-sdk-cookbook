"""
KMS Encryptor: envelope encryption using a Key Management Service.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/encryption#kms-encryptor
"""

import base64
import os

from gllm_datastore.encryptor.kms_encryptor import KmsEncryptor
from gllm_datastore.kms.kms import BaseKeyManagementService


class SampleKMSImplementation(BaseKeyManagementService):
    """A sample in-process KMS implementation (for demonstration only)."""

    def get_dek(self) -> tuple[bytes, str]:
        """Generate a data encryption key and its base64-encoded encrypted form."""
        dek = os.urandom(32)
        encrypted_dek = base64.b64encode(dek).decode()
        return dek, encrypted_dek

    def decrypt_dek(self, encrypted_dek: bytes) -> bytes:
        """Decode the base64-encoded encrypted DEK back to raw bytes."""
        return base64.b64decode(encrypted_dek)

    def encrypt(self, plaintext: bytes) -> bytes:
        """Return plaintext unchanged (no server-side KMS to call in this sample)."""
        return plaintext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """Decode the base64-encoded ciphertext back to raw bytes."""
        return base64.b64decode(ciphertext)


def main() -> None:
    """Encrypt and decrypt a value through KmsEncryptor to prove the round-trip."""
    kms = SampleKMSImplementation()
    encryptor = KmsEncryptor(kms=kms)

    ciphertext = encryptor.encrypt("top secret value")
    plaintext = encryptor.decrypt(ciphertext)

    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted:  {plaintext}")
    assert plaintext == "top secret value"


if __name__ == "__main__":
    main()
