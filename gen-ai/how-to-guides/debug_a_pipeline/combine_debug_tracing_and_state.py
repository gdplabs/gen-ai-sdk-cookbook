"""Combine debug tracing with debug_state config flag.

See https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/debug-a-pipeline#combining-with-debug-state
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class DebugState(TypedDict):
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
        state_type=DebugState,
    )


async def main() -> None:
    pipeline = build_pipeline()
    pipeline.enable_debug_tracing()

    result = await pipeline.invoke(
        {"text": "combined debug", "text_upper": "", "text_len": 0},
        config={"debug_state": True},
    )

    # result["__state_logs__"] contains full debug events
    print(result["__state_logs__"])


if __name__ == "__main__":
    asyncio.run(main())
