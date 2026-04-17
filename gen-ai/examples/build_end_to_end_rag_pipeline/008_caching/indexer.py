"""Example script to index a CSV file into a vector store.

Authors:
    Kadek Denaya (kadek.d.r.diana@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/index-your-data-with-vector-data-store
"""

import asyncio
import csv
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()

# Initialize vector store with persistent storage
vector_store = ChromaVectorDataStore(
    collection_name="documents",
    client_type="persistent",  # use a Persistent Chroma DB
    persist_directory="data",  # 👈 where the data is located
    embedding=OpenAIEMInvoker(model_name=os.getenv("EMBEDDING_MODEL")),
)


# Load documents from CSV file
async def load_csv_data():
    with open("data/imaginary_animals.csv", "r") as f:
        reader = csv.DictReader(f)
        chunks = [
            Chunk(content=row["description"], metadata={"name": row["name"]})
            for row in reader
        ]

    await vector_store.add_chunks(chunks)
    print(f"Successfully indexed {len(chunks)} documents from CSV file")


if __name__ == "__main__":
    asyncio.run(load_csv_data())
