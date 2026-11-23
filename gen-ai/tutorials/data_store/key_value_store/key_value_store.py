"""
Key-Value Store: versioned secret management with OpenBao.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/key-value-store
"""

from dotenv import load_dotenv
from gllm_datastore.key_value_store.key_value_store import ReadOption, WriteOption
from gllm_datastore.key_value_store.openbao_key_value_store import OpenBaoKeyValueStore

load_dotenv()


def main() -> None:
    """Use OpenBaoKeyValueStore for versioned secret storage."""
    kv_store = OpenBaoKeyValueStore(
        base_url="https://openbao.example.com",
        token="your-auth-token",
        mount_point="secret",
    )

    # Write a secret (creates version 1)
    kv_store.write(
        path="myapp/database",
        data={
            "username": "admin",
            "password": "secure_password",
            "host": "db.example.com",
        },
    )

    # Read the secret
    secret = kv_store.read("myapp/database")
    print(secret.data)
    print(secret.metadata.version)

    # Read a specific version
    secret_v3 = kv_store.read(
        "myapp/config",
        options=ReadOption(version=3),
    )
    print(secret_v3.data)

    # Write with Check-and-Set
    kv_store.write(
        path="myapp/config",
        data={"key": "new_value"},
        options=WriteOption(cas=5),
    )

    # List keys
    keys = kv_store.list("myapp")
    print(keys)


if __name__ == "__main__":
    main()
