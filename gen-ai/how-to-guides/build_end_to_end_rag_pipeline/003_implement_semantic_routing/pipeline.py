"""Example script to build and run a simple RAG pipeline with semantic routing.
Authors:
    Delfia N. A. Putri (delfia.n.a.putri@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/implement-semantic-routing
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.request_processor import build_lm_request_processor
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.pipeline.states import RAGState
from gllm_pipeline.steps import step, switch
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

class RouterState(RAGState):
    """State for the router."""
    route: str
    source: str

# Create components
em_invoker = OpenAIEMInvoker("text-embedding-3-small")
data_store = ChromaDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
).with_vector(em_invoker=em_invoker)
retriever = VectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.preset.stuff(os.getenv("LANGUAGE_MODEL"))

response_synthesizer_general = ResponseSynthesizer.stuff(
    lm_request_processor=build_lm_request_processor(
        model_id=os.getenv("LANGUAGE_MODEL"),
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="You are a helpful assistant that answers general knowledge questions.",
        user_template="{query}",
    )

)

with open("route_examples.json", "r", encoding="utf-8") as f:
    route_examples = json.load(f)

semantic_router = SemanticRouter.aurelio(
    default_route="general",
    valid_routes={"knowledge_base", "general"},
    encoder=em_invoker,
    route_examples=route_examples,
    similarity_threshold=0.3,
)

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
synthesize_general_step = step(
    component=response_synthesizer_general,
    input_map={
        "query": "user_query",
    },
    output_state="response",
)
conditional_step = switch(
    condition = semantic_router,
    branches = {
        "knowledge_base": [retrieve_step, synthesize_step],
        "general": synthesize_general_step,
    },
    default = synthesize_general_step,
    input_map = {"source": "user_query"},
    output_state = "response",
)


e2e_pipeline = Pipeline(steps=[conditional_step], state_type=RouterState)


# Run the pipeline

async def main():
    state = {"user_query": "Give me nocturnal creatures from the dataset"}  # Replace with your actual query
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())