"""Example script to build and run a video search RAG pipeline with timestamped retrieval.

Authors:
    Nico Samuelson Tjandra (nico.s.tjandra@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/video-search-pipeline
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_generation.repacker import Repacker
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker import GoogleEMInvoker
from gllm_inference.request_processor import build_lm_request_processor
from gllm_pipeline.steps import step
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

SYSTEM_PROMPT = """
You are a video question answering assistant. 
In the context, there are video segments and a summary of the video.
Use the video segments and the summary to answer the user's query.
When relevant, explain the answer and cite the timestamp so the user knows exactly where to look.
When the information is not available in the context, just say so.

Context:
{context}
"""
USER_PROMPT = "Query: {query}"

# Create components
em_invoker = GoogleEMInvoker(model_name=os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="video-qa",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=em_invoker)
retriever = VectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.stuff(
    lm_request_processor=build_lm_request_processor(
        model_id=os.environ["LANGUAGE_MODEL"],
        credentials=os.environ["GOOGLE_API_KEY"],
        system_template=SYSTEM_PROMPT,
        user_template=USER_PROMPT,
    ),
    chunks_repacker=Repacker(mode="chunk"),
)


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


async def main() -> None:
    """Run the video RAG pipeline against a sample attention-mechanism query.

    Invokes the end-to-end pipeline with a hard-coded query and prints the
    synthesized response (with cited timestamps) to stdout.
    """
    state = {
        "user_query": "What is the attention mechanism?",
        "event_emitter": None,
    }
    config = {"top_k": 10}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
