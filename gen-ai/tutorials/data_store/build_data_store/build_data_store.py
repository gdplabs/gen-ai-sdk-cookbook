"""Example of building a data store using build_data_store factory.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/build-data-store
"""

from gllm_datastore import build_data_store

store = build_data_store(
    data_store_id="in-memory/default",
)
