from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

# Initialize data store with vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
data_store = ChromaDataStore(
    collection_name="documents",
).with_vector(em_invoker=em_invoker)

# Add chunks to the store
chunks = [
    Chunk(content="AI is the future."),
    Chunk(content="Parrot is a bird."),
]
await data_store.add_chunks(chunks)
