"""Example script to build and run a simple RAG pipeline.

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from gl_observability.logs import LoggingConfig, setup_logging
from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_pipeline.steps import step
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

setup_logging(LoggingConfig(level=logging.DEBUG))

for noisy_logger in ("asyncio", "chromadb", "httpcore", "httpx", "httpx2", "openai", "urllib3"):
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

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
    state = {"user_query": "Give me nocturnal creatures from the dataset"}  # Replace with your actual query
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
