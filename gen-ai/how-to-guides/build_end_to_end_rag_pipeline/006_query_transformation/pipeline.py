"""Example script to build and run a RAG pipeline with query transformation.

Authors:
    Delfia N. A. Putri (delfia.n.a.putri@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/query-transformation
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.builder import build_lm_request_processor
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_pipeline.pipeline import RAGState
from gllm_pipeline.steps import step, transform
from gllm_retrieval.query_transformer.one_to_one_query_transformer import OneToOneQueryTransformer
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever

load_dotenv()

class RAGStateWithQT(RAGState):
    """RAG state with query transformation support.

    Extends the base RAGState to include transformed queries.
    """
    query: str

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
transform_query_step = step(
    component=OneToOneQueryTransformer(
        lm_request_processor=build_lm_request_processor(
            model_id="openai/gpt-4o-mini",
            system_template="You are a helpful assistant that rewrites queries for better retrieval. Rewrite the following query. Only output the transformed query.",
            user_template="Query: {query}",
        )
    ),
    input_map={"query": "user_query"},
    output_state="queries",
)
flatten_query = transform(
    operation=lambda x: "\n".join(x["queries"]),
    input_states=["queries"],
    output_state="query",
)
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

e2e_pipeline = transform_query_step | flatten_query | retrieve_step | synthesize_step
e2e_pipeline.state_type = RAGStateWithQT


# Run the pipeline
async def main():
    state = {"user_query": "Give me nocturnal creatures from the dataset"}  # Replace with your actual query
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
