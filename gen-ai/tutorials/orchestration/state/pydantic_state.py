"""Use a Pydantic BaseModel as Pipeline state.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/state#using-a-pydantic-basemodel-as-a-state
"""

import asyncio
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class MyCustomStateModel(BaseModel):
    user_query: str = Field(..., description="The original query from the user")
    chunks: list = Field(default_factory=list, description="Retrieved chunks")
    context: str = Field(default="", description="Context information")
    response: str = Field(default="", description="Generated response")
    document_scores: list[float] = Field(
        default_factory=list, description="Document relevance scores"
    )
    debug_info: dict[str, Any] = Field(
        default_factory=dict, description="Debug information"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


def retriever(data: dict) -> list:
    return [f"chunk-{data['user_query']}"]


async def main() -> None:
    """Apply a Pydantic BaseModel as the Pipeline state_type."""
    pipe = Pipeline(
        steps=[
            transform(retriever, input_map=["user_query"], output_state="chunks")
        ],
        state_type=MyCustomStateModel,
    )

    state = MyCustomStateModel(user_query="hello")
    result = await pipe.invoke(state.model_dump())
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
