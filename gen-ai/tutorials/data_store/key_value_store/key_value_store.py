"""Example of using OpenBaoKeyValueStore for secure secret management.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/key-value-store
"""

import sys

from gllm_datastore.key_value_store.openbao_key_value_store import OpenBaoKeyValueStore

try:
    kv_store = OpenBaoKeyValueStore(
        base_url="https://openbao.example.com",
        token="your-auth-token",
        mount_point="secret",
    )

    kv_store.write(
        path="myapp/database",
        data={
            "username": "admin",
            "password": "secure_password",
            "host": "db.example.com",
        },
    )

    secret = kv_store.read("myapp/database")
    print(secret.data)
    print(secret.metadata.version)
except ValueError as e:
    print(f"Cannot connect to OpenBao (expected — this is a placeholder URL): {e}", file=sys.stderr)
    sys.exit(0)
