"""Example of using AES-GCM encryption for data at rest.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/encryption
"""

import os

from gllm_datastore.encryptor.aes_gcm_encryptor import AESGCMEncryptor

encryption_key = os.urandom(32)
encryptor = AESGCMEncryptor(key=encryption_key)
