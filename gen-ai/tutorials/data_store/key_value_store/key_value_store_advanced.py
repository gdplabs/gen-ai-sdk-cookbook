"""
Key-Value Store advanced: partial updates, version management, and error handling.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/key-value-store#advanced-patterns
"""

import requests

from dotenv import load_dotenv
from gllm_datastore.key_value_store.key_value_store import WriteOption
from gllm_datastore.key_value_store.openbao_key_value_store import OpenBaoKeyValueStore

load_dotenv()


def main() -> None:
    """Demonstrate advanced key-value store patterns."""
    kv_store = OpenBaoKeyValueStore(
        base_url="https://openbao.example.com",
        token="your-auth-token",
        mount_point="secret",
    )

    # Partial update via patch
    kv_store.patch(
        path="myapp/database",
        data={"password": "new_pass"},
    )

    # Soft-delete versions
    kv_store.delete("myapp/config", versions=[1, 2])

    # Restore deleted versions
    kv_store.undelete("myapp/config", versions=[1, 2])

    # Permanently destroy versions (irreversible)
    kv_store.destroy("myapp/config", versions=[1, 2])

    # Namespace organization
    kv_store.write("myapp/prod/database", {"key": "prod_value"})
    kv_store.write("myapp/staging/database", {"key": "staging_value"})
    kv_store.write("myapp/services/auth/jwt-secret", {"secret": "jwt_value"})

    # Error handling
    try:
        kv_store.write("myapp/config", {"key": "value"}, options=WriteOption(cas=5))
    except requests.RequestException as e:
        if hasattr(e.response, "status_code"):
            if e.response.status_code == 400:
                print("Invalid request or CAS mismatch")
            elif e.response.status_code == 404:
                print("Secret not found")
            elif e.response.status_code == 409:
                print("Version conflict - secret was modified")
        else:
            print(f"Network or connection error: {e}")


if __name__ == "__main__":
    main()
