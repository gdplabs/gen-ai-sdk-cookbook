"""Example script to build and run a RAG pipeline with simple guardrail.

Authors:
    Delfia N. A. Putri (delfia.n.a.putri@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/simple-guardrail
"""

import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from gllm_core.constants import EventLevel
from gllm_core.event import EventEmitter
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_pipeline.pipeline import RAGState
from gllm_pipeline.steps import guard, log, step
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever

load_dotenv()

# Define the state class
class GuardrailState(RAGState):
    """RAG state with guardrail validation parameters.

    Extends the base RAGState to include query length validation settings.
    """
    max_query_length: int
    min_query_length: int

def validate_message_length(inputs: dict[str, Any]) -> bool:
    """Validate the length of the user query.

    Args:
        inputs (dict[str, Any]): The inputs to the function.

    Returns:
        bool: True if the user query is valid, False otherwise.
    """
    user_query = inputs["user_query"]
    max_query_length = inputs["max_query_length"]
    min_query_length = inputs["min_query_length"]
    return len(user_query) <= max_query_length and len(user_query) >= min_query_length

# Create components
em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaVectorDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
    embedding=em_invoker,
)
retriever = BasicVectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.stuff_preset(os.getenv("LANGUAGE_MODEL"))


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

guardrail_step = guard(
    validate_message_length,
    success_branch=retrieve_step,
    failure_branch=log( # for extra logging step
        message="User query length is not valid: '{user_query}'",
        emit_kwargs={"event_level": EventLevel.INFO},
    ),
    input_map={
        "user_query": "user_query",
        "max_query_length": "max_query_length",
        "min_query_length": "min_query_length",
    },
)
e2e_pipeline = guardrail_step | synthesize_step
e2e_pipeline.state_type = GuardrailState

# Run the pipeline

async def main():
    state = {
        "user_query": "Give me nocturnal creatures from the dataset", # Replace with your actual query
        "max_query_length": 100,
        "min_query_length": 1,
    }

    # Test with invalid query length
    invalid_state = {
        "user_query": "this is a very long message that should be rejected by the guardrail, with length over 100 characters, and once again, it should be rejected",
        "max_query_length": 100,
        "min_query_length": 1,
    }

    event_emitter = EventEmitter.with_console_handler() # for extra logging step
    config = {
        "top_k": 5,
        "event_emitter": event_emitter, # for extra logging step
    }
    result = await e2e_pipeline.invoke(
        # state,
        invalid_state, # to test guardrail
        config,
    )
    print(f"Pipeline result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
