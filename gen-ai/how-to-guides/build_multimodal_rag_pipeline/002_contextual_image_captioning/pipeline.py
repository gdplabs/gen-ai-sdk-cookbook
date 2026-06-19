"""Example script to build and run an image search RAG pipeline with contextual captions.

Authors:
    Nico Samuelson Tjandra (nico.s.tjandra@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/image-search-pipeline
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
    collection_name="indonesia-tourism-contextual",
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
    """Run the contextual image captioning RAG pipeline against a sample tourism query.

    Invokes the end-to-end pipeline with a hard-coded query against the contextual
    caption collection and prints the synthesized response to stdout.
    """
    state = {
        "user_query": "Deskripsikan seperti apa bentuk rumah Suku Bajo di atas air dan tata letak desa panggung mereka?",
    }
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
