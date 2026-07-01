"""Example of using a data store as a cache.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/cache
"""

from gllm_datastore.data_store import ChromaDataStore

store = ChromaDataStore(collection_name="cache-store").with_fulltext()
cache = store.as_cache()
