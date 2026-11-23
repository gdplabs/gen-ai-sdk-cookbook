"""Use the pipe (|) operator to compose a Pipeline.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#the-pipe-operator
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.steps._func import log, transform


class MiniState2(TypedDict):
    text: str
    text_upper: str
    text_len: int


def to_upper2(data: dict) -> str:
    return data["text"].upper()


def count_chars2(data: dict) -> int:
    return len(data["text_upper"])


async def main() -> None:
    """Compose a Pipeline using the pipe | operator."""
    pipe2 = (
        transform(to_upper2, input_map=["text"], output_state="text_upper")
        | transform(count_chars2, input_map=["text_upper"], output_state="text_len")
        | log("Upper2: {text_upper} (len={text_len})")
    )
    pipe2.state_type = MiniState2  # important: set your TypedDict state

    initial2: MiniState2 = {"text": "pipeline!", "text_upper": "", "text_len": 0}
    final2 = await pipe2.invoke(initial2)
    print(final2)


if __name__ == "__main__":
    asyncio.run(main())
