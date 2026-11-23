"""An example of indexing data into a vector store.

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/index-your-data-with-vector-data-store
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store.chroma import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main():
    """Index data into a vector store and query it using semantic search."""
    # Initialize vector store with embedding model
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    store = ChromaDataStore(collection_name="documents").with_vector(em_invoker=em_invoker)

    # Add chunks to the store
    await store.vector.create(
        data=[Chunk(content="AI is the future."), Chunk(content="Parrot is a bird.")]
    )

    # Query data using semantic search
    results: list[Chunk] = await store.vector.retrieve(query="Is AI the future?")
    for chunk in results:
        print(f"Chunk content: {chunk.content}")
        print(f"Chunk similarity score: {chunk.score}")
        print("---")


if __name__ == "__main__":
    asyncio.run(main())
