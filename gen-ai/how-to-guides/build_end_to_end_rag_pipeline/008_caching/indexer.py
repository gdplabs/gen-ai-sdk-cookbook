from gllm_pipeline.pipeline import Pipeline

from gllm_pipeline.types import CacheConfig

e2e_pipeline_with_cache = Pipeline(
    [
        step(
            component=VectorRetriever(data_store=data_store),
            input_map={"query": "user_query", "top_k": "top_k"},
            output_state="chunks",
            cache=CacheConfig(store=cache_store),  # Enable step-level caching
        ),
        step(
            component=ResponseSynthesizer.stuff_preset(os.getenv("LANGUAGE_MODEL")),
            input_map={"query": "user_query", "chunks": "chunks"},
            output_state="response",
        ),
    ],
    cache=CacheConfig(store=cache_store),  # Enable pipeline-level caching
)
