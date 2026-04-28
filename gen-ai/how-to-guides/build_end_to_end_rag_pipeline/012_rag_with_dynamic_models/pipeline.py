"""Runnable example for a RAG pipeline with dynamic models."""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps.pipeline_step import BasePipelineStep


class DynamicRAGState(TypedDict, total=False):
    user_query: str
    model_id: str
    chunks: list[str]
    response: str


class RetrieverStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        return {
            "chunks": [
                "Luminafox is a nocturnal forest creature with reflective silver fur.",
                "Dusk Panther prowls twilight woods and hunts after sunset.",
                "Bramble Owl roosts high in the canopy and navigates in low light.",
            ]
        }


class DynamicResponseStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        model_id = state["model_id"]
        chunks = state["chunks"]
        if model_id == "openai/gpt-4.1-nano":
            response = "OpenAI style response: " + "; ".join(chunks[:2])
        elif model_id == "anthropic/claude-3-5-haiku":
            response = "Anthropic style response: " + " | ".join(chunks[1:])
        else:
            response = f"Fallback response for {model_id}: " + chunks[0]
        return {"response": response}


def build_pipeline(model_id: str) -> Pipeline:
    return Pipeline(
        [
            RetrieverStep(name="retrieve_chunks"),
            DynamicResponseStep(name="dynamic_response"),
        ],
        state_type=DynamicRAGState,
        name=f"dynamic_rag_{model_id.replace('/', '_').replace('-', '_')}",
    )


async def run_model(model_id: str) -> None:
    pipeline = build_pipeline(model_id)
    result = await pipeline.invoke(
        {
            "user_query": "Give me nocturnal forest animals from the dataset",
            "model_id": model_id,
        }
    )
    print(f"Model: {model_id}")
    print(f"Response: {result['response']}")


async def main() -> None:
    await run_model("openai/gpt-4.1-nano")
    await run_model("anthropic/claude-3-5-haiku")


if __name__ == "__main__":
    asyncio.run(main())
