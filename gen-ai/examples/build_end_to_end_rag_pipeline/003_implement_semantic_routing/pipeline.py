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
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.builder import build_lm_request_processor
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_misc.router import AurelioSemanticRouter
from gllm_misc.router.aurelio_semantic_router.encoders import EMInvokerEncoder
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.pipeline.states import RAGState
from gllm_pipeline.steps import step, switch
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever

load_dotenv()

class RouterState(RAGState):
    """State for the router."""
    route: str
    source: str

# Create components
em_invoker = OpenAIEMInvoker("text-embedding-3-small")
data_store = ChromaVectorDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
    embedding=em_invoker,
)
retriever = BasicVectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.stuff_preset(os.getenv("LANGUAGE_MODEL"))

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

semantic_router = AurelioSemanticRouter(
    default_route = "general",
    valid_routes = set({"knowledge_base", "general"}),
    encoder = EMInvokerEncoder(
        em_invoker = em_invoker,
        score_threshold = 0.3,
    ),
    routes = route_examples,
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