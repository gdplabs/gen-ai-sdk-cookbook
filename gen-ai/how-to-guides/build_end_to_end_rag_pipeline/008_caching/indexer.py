"""Example script to index a CSV file into a vector store.

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/index-your-data-with-vector-data-store
"""

import asyncio
import csv
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()

# Initialize vector store with persistent storage
em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
vector_store = ChromaDataStore(
    collection_name="documents",
    client_type="persistent",  # use a Persistent Chroma DB
    persist_directory="data",  # 👈 where the data is located
).with_vector(em_invoker=em_invoker)


# Load documents from CSV file
async def load_csv_data():
    with open("data/imaginary_animals.csv", "r") as f:
        reader = csv.DictReader(f)
        chunks = [
            Chunk(content=row["description"], metadata={"name": row["name"]})
            for row in reader
        ]

    try:
        await vector_store.vector.create(chunks)
        print(f"Successfully indexed {len(chunks)} documents from CSV file")
    finally:
        await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(load_csv_data())
