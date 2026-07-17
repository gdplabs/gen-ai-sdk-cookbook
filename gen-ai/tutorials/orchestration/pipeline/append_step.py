"""Append a step to an existing Pipeline using the | operator.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#appending-a-step
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
    """Append a step to a Pipeline using the pipe | operator."""
    p1 = Pipeline(
        steps=[transform(to_upper, input_map=["text"], output_state="text_upper")],
        state_type=TextState,
    )

    # Append step at the end
    p1_plus = p1 | transform(
        count_len, input_map=["text_upper"], output_state="text_len"
    )

    final = await p1_plus.invoke({"text": "hello", "text_upper": "", "text_len": 0})
    print(final)  # {'text': 'hello', 'text_upper': 'HELLO', 'text_len': 5}


if __name__ == "__main__":
    asyncio.run(main())
