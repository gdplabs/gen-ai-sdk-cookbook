"""Pipeline used by the FastAPI server example."""

from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps.pipeline_step import BasePipelineStep


class ServerState(TypedDict, total=False):
    user_query: str
    top_k: int
    response: str


class RetrieveStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        top_k = runtime.context.get("top_k", 3) if runtime and runtime.context else 3
        return {"top_k": top_k}


class RespondStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        query = state["user_query"]
        top_k = state["top_k"]
        return {
            "response": f"Top {top_k} simulated matches for '{query}': Reef Ray, Moonfin, Crystal Jellyfish."
        }


e2e_pipeline = Pipeline(
    [
        RetrieveStep(name="retrieve"),
        RespondStep(name="respond"),
    ],
    state_type=ServerState,
    name="server_pipeline_demo",
)
