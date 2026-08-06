"""Example script to build and run a simple RAG pipeline.

Authors:
    Henry Wicaksono (henry.wicaksono@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_pipeline.steps import step
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

# Create components
em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
).with_vector(em_invoker=em_invoker)
retriever = VectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.preset.stuff(os.getenv("LANGUAGE_MODEL"))

# Create the pipeline
retrieve_step = step(
    component=retriever,
    input_map={"query": "user_query", "top_k": "top_k"},
    output_state="chunks",
)
synthesize_step = step(
    component=response_synthesizer,
    input_map={"query": "user_query", "chunks": "chunks"},
    output_state="response",
)
e2e_pipeline = retrieve_step | synthesize_step

# Run the pipeline

async def main():
    try:
        state = {"user_query": "Give me nocturnal creatures from the dataset"}  # Replace with your actual query
        config = {"top_k": 5}
        result = await e2e_pipeline.invoke(state, config)
        print(f"Pipeline result: {result['response']}")
    finally:
        await em_invoker.release_resources()
        await response_synthesizer.strategy.lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
