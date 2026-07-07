import asyncio
from gllm_pipeline.steps import step
from gllm_pipeline.pipeline import Pipeline
from modules.response_synthesizer import build_response_synthesizer
from modules.retriever import retriever

def build_pipeline(model_id: str) -> Pipeline:
    """Build the end-to-end pipeline.

    Args:
        model_id (str): Model identifier used to build the response synthesizer.

    Returns:
        Any: A composed pipeline with .invoke(state, config) coroutine method.
    """
    # The following steps stay the same
    retriever_step = step(
        retriever,
        input_map={"query": "user_query", "top_k": "top_k"},
        output_state="chunks",
    )

    response_synthesizer_step = step(
        component=response_synthesizer,
        input_map={
            "query": "user_query",
            "chunks": "chunks",
        },
        output_state="response",
    )
    return retriever_step | response_synthesizer_step
