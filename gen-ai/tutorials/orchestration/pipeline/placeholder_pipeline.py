"""Use a placeholder (empty) Pipeline with the | operator.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#placeholder-pipelines
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class TextState(TypedDict):
    text: str
    text_upper: str
    text_len: int


def to_upper(data: dict) -> str:
    return data["text"].upper()


def count_len(data: dict) -> int:
    return len(data["text_upper"])


async def main() -> None:
    """Initialize a Pipeline with empty steps as a placeholder,
    then compose with the | operator.
    """
    identity = Pipeline([], state_type=TextState)
    p = Pipeline(
        steps=[transform(to_upper, input_map=["text"], output_state="text_upper")],
        state_type=TextState,
    )

    a = p | identity
    b = identity | p

    # Verify both compositions work identically
    result_a = await a.invoke({"text": "hello", "text_upper": "", "text_len": 0})
    print("p | identity:", result_a)

    result_b = await b.invoke({"text": "hello", "text_upper": "", "text_len": 0})
    print("identity | p:", result_b)


if __name__ == "__main__":
    asyncio.run(main())
