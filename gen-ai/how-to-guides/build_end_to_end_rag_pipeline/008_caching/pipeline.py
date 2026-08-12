"""Example script to build a pipeline with caching enabled.

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/caching
"""

import asyncio
import os
from time import time

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_pipeline.types import CacheConfig
from gllm_retrieval.retriever import VectorRetriever  # ty:ignore[unresolved-import]

load_dotenv()


def build_pipeline() -> tuple[Pipeline, OpenAIEMInvoker, ResponseSynthesizer]:
    """Build a pipeline with caching enabled.

    Returns:
        tuple[Pipeline, OpenAIEMInvoker, ResponseSynthesizer]: The pipeline with caching enabled, along with the
            embedding invoker and response synthesizer it holds, so their resources can be released after use.
    """
    em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
    data_store = ChromaDataStore(
        collection_name="documents",
        client_type="persistent",
        persist_directory="data",
    ).with_vector(em_invoker=em_invoker).with_fulltext()
    cache_store = data_store.as_cache()
    response_synthesizer = ResponseSynthesizer.preset.stuff(os.getenv("LANGUAGE_MODEL"))

    e2e_pipeline_with_cache = Pipeline(
        [
            step(
                component=VectorRetriever(data_store),
                input_map={"query": "user_query", "top_k": "top_k"},
                output_state="chunks",
                cache=CacheConfig(store=cache_store),  # Enable step-level caching
            ),
            step(
                component=response_synthesizer,
                input_map={"query": "user_query", "chunks": "chunks"},
                output_state="response",
            ),
        ],
        cache=CacheConfig(store=cache_store),  # Enable pipeline-level caching
    )
    return e2e_pipeline_with_cache, em_invoker, response_synthesizer


async def main():
    """Main function to run the pipeline."""

    for _ in range(2):
        start_time = time()
        state = {"user_query": "Give me nocturnal creatures from the dataset"}
        config = {"top_k": 5}
        pipeline, em_invoker, response_synthesizer = build_pipeline()
        result = await pipeline.invoke(state, config)
        print(f"Pipeline result: {result['response']}")
        end_time = time()
        print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(main())
