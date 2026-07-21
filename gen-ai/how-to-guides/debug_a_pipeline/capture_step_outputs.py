"""Capture individual step outputs with include_outputs_from.

See https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/debug-a-pipeline#capturing-step-outputs
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import transform


class OutputState(TypedDict):
    text: str
    text_upper: str
    text_len: int


def to_upper(data: dict) -> str:
    return data["text"].upper()


def count_chars(data: dict) -> int:
    return len(data["text_upper"])


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            transform(
                to_upper, input_map=["text"], output_state="text_upper", name="to_upper"
            ),
            transform(
                count_chars,
                input_map=["text_upper"],
                output_state="text_len",
                name="count_chars",
            ),
        ],
        state_type=OutputState,
    )


async def main() -> None:
    pipeline = build_pipeline()

    result = await pipeline.invoke(
        {"text": "hello world", "text_upper": "", "text_len": 0},
        include_outputs_from={"to_upper", "count_chars"},
    )

    print(result["__step_outputs__"]["to_upper"])
    print(result["__step_outputs__"]["count_chars"])


if __name__ == "__main__":
    asyncio.run(main())
