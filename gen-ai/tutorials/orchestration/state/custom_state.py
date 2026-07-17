"""Define a custom TypedDict state for a Pipeline.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/state#defining-a-custom-state
"""

import asyncio
from typing import Any, TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class MyCustomState(TypedDict):
    user_query: str
    chunks: list
    context: str
    response: str
    document_scores: list[float]
    debug_info: dict[str, Any]


def retrieve_step(data: dict) -> list:
    return [f"chunk-{data['user_query']}"]


async def main() -> None:
    """Apply a custom TypedDict as the Pipeline state_type."""
    pipe = Pipeline(
        steps=[
            transform(
                retrieve_step,
                input_map=["user_query"],
                output_state="chunks",
            )
        ],
        state_type=MyCustomState,
    )

    initial: MyCustomState = {
        "user_query": "hello",
        "chunks": [],
        "context": "",
        "response": "",
        "document_scores": [],
        "debug_info": {},
    }
    result = await pipe.invoke(initial)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
