"""Runnable example for a RAG pipeline with dynamic models."""

import asyncio
import os
from typing import TypedDict

from dotenv import load_dotenv
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever


load_dotenv()


class DynamicRAGState(TypedDict, total=False):
    user_query: str
    top_k: int
    chunks: list[str]
    response: str


def build_response_synthesizer(model_id: str) -> ResponseSynthesizer:
    return ResponseSynthesizer.preset.stuff(model_id)


em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaVectorDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
    embedding=em_invoker,
)
retriever = BasicVectorRetriever(data_store)


def build_pipeline(model_id: str) -> Pipeline:
    response_synthesizer = build_response_synthesizer(model_id)

    retriever_step = step(
        retriever,
        input_map={"query": "user_query", "top_k": "top_k"},
        output_state="chunks",
        name="retriever_step",
    )

    response_synthesizer_step = step(
        component=response_synthesizer,
        input_map={
            "query": "user_query",
            "chunks": "chunks",
        },
        output_state="response",
        name="response_synthesizer_step",
    )

    return Pipeline(
        [retriever_step, response_synthesizer_step],
        state_type=DynamicRAGState,
        name=f"dynamic_rag_{model_id.replace('/', '_').replace('-', '_')}",
    )


async def run_model(model_id: str) -> None:
    pipeline = build_pipeline(model_id)
    result = await pipeline.invoke(
        {
            "user_query": "Give me nocturnal creatures from the dataset",
            "top_k": 3,
        }
    )
    print(f"Model: {model_id}")
    print(f"Response: {result['response']}")


async def main() -> None:
    await run_model(os.getenv("LANGUAGE_MODEL", "openai/gpt-4.1-nano"))


if __name__ == "__main__":
    asyncio.run(main())