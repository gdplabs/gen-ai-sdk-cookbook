"""Capture intermediate step outputs using include_outputs_from.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/observability-and-debugging#capturing-step-outputs
"""

import asyncio
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class DummyState(TypedDict):
    text: str
    text_upper: str


def to_upper(data: dict) -> str:
    return data["text"].upper()


async def main() -> None:
    pipeline = Pipeline(
        steps=[
            transform(
                to_upper,
                input_map=["text"],
                output_state="text_upper",
                name="to_upper",
            )
        ],
        state_type=DummyState,
        checkpointer=InMemorySaver(),
    )
    result = await pipeline.invoke(
        {"text": "hello", "text_upper": ""},
        thread_id="t2",
        include_outputs_from={"to_upper"},
    )
    print(result["__step_outputs__"]["to_upper"])


if __name__ == "__main__":
    asyncio.run(main())
