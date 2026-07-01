from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

# Create a data store cache with vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
cache_store = ChromaDataStore(
    collection_name="my_cache",
).with_vector(em_invoker=em_invoker).as_cache()
