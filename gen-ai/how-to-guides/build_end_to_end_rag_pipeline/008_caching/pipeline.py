"""Example script to build a pipeline with caching enabled.

Authors:
    Kadek Denaya (kadek.d.r.diana@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/caching
"""

import asyncio
import os
from time import time

from dotenv import load_dotenv
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever

load_dotenv()


def build_pipeline() -> Pipeline:
    """Build a pipeline with caching enabled.

    Returns:
        Pipeline: A pipeline with caching enabled.
    """
    em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
    data_store = ChromaVectorDataStore(
        collection_name="documents",
        client_type="persistent",
        persist_directory="data",
        embedding=em_invoker,
    )
    cache_store = data_store.as_cache()

    e2e_pipeline_with_cache = Pipeline(
        [
            step(
                component=BasicVectorRetriever(data_store),
                input_map={"query": "user_query", "top_k": "top_k"},
                output_state="chunks",
                cache_store=cache_store,  # Enable step-level caching
            ),
            step(
                component=ResponseSynthesizer.stuff_preset(os.getenv("LANGUAGE_MODEL")),
                input_map={"query": "user_query", "chunks": "chunks"},
                output_state="response",
            ),
        ],
        cache_store=cache_store,  # Enable pipeline-level caching
    )
    return e2e_pipeline_with_cache


async def main():
    """Main function to run the pipeline."""

    for _ in range(2):
        start_time = time()
        state = {"user_query": "Give me nocturnal creatures from the dataset"}
        config = {"top_k": 5}
        pipeline = build_pipeline()
        result = await pipeline.invoke(state, config)
        print(f"Pipeline result: {result['response']}")
        end_time = time()
        print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(main())
