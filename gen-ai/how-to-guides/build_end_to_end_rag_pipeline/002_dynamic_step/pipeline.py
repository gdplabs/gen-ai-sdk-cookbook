"""Example script to build and run a simple RAG pipeline with dynamic step.

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/dynamic-step
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from gl_observability.logs import LoggingConfig, setup_logging
from gllm_datastore.data_store import ChromaDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_pipeline.pipeline.states import RAGState
from gllm_pipeline.steps import step, toggle
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

setup_logging(LoggingConfig(level=logging.DEBUG))

for noisy_logger in ("asyncio", "chromadb", "httpcore", "httpx", "httpx2", "openai", "urllib3"):
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

# Define the state class
class ToggleState(RAGState):
    """RAG state with knowledge base toggle functionality.

    Extends the base RAGState to include a flag for enabling/disabling knowledge base usage.
    """
    use_knowledge_base: bool

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

knowledge_base_toggle_step = toggle(
    condition=lambda x: x["use_knowledge_base"],
    if_branch=[retrieve_step],
)

e2e_pipeline = knowledge_base_toggle_step | synthesize_step
e2e_pipeline.state_type = ToggleState

# Run the pipeline
async def main():
    state = {
        "user_query": "Give me nocturnal creatures from the dataset", # Replace with your actual query
        "use_knowledge_base": False, # Set to True to retrieve from knowledge base
        "chunks": [] # Initialize to empty list if knowledge base is disabled
    }
    config = {
        "top_k": 5,
    }
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
