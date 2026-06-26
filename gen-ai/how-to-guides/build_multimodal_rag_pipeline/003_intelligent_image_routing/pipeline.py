"""Example script to build and run a smart image routing RAG pipeline.

Authors:
    Nico Samuelson Tjandra (nico.s.tjandra@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/smart-image-routing
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_pipeline.steps import step
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

# Create components
em_invoker = VoyageEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="narp-operational-guide",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=em_invoker)
retriever = VectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.preset.stuff(os.getenv("LANGUAGE_MODEL"))

# Build the pipeline
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
async def main() -> None:
    """Run the smart image routing RAG pipeline against a sample NARP query.

    Invokes the end-to-end pipeline with a hard-coded query and prints the
    synthesized response to stdout.
    """
    state = {
        "user_query": "If a client does not require support with toileting, does not require support with dressing, but does require support with showering/bathing, what team assignment and group classification do they receive?",
    }
    config = {"top_k": 10}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
