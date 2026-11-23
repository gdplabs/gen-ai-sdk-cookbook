"""Merge two Pipelines of the same State schema using the | operator.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#merge-two-pipelines
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import log, transform


class TextState(TypedDict):
    text: str
    text_upper: str
    text_len: int


def to_upper(data: dict) -> str:
    return data["text"].upper()


def count_len(data: dict) -> int:
    return len(data["text_upper"])


async def main() -> None:
    """Merge two Pipelines with the same state type."""
    p_left = Pipeline(
        steps=[transform(to_upper, input_map=["text"], output_state="text_upper")],
        state_type=TextState,
    )
    p_right = Pipeline(
        steps=[
            transform(count_len, input_map=["text_upper"], output_state="text_len"),
            log("len={text_len}"),
        ],
        state_type=TextState,
    )

    combined = p_left | p_right  # OK: same state type

    final = await combined.invoke(
        {"text": "compose", "text_upper": "", "text_len": 0}
    )
    print(final)  # {'text': 'compose', 'text_upper': 'COMPOSE', 'text_len': 7}


if __name__ == "__main__":
    asyncio.run(main())
