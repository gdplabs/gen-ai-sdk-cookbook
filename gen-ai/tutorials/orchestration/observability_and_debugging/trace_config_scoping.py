"""Scope content capture to a single pipeline invocation with trace_config.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/observability-and-debugging#scoped-content-capture-per-invocation
"""

import asyncio
from typing import TypedDict

from gllm_core.observability import ComponentIOCaptureConfig, get_component_io_capture_config
from langgraph.checkpoint.memory import InMemorySaver

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import transform


class DummyState(TypedDict):
    text: str
    captured_during_run: bool


def read_capture_flag(data: dict) -> bool:
    return get_component_io_capture_config().capture_input


async def main() -> None:
    pipeline = Pipeline(
        steps=[
            transform(
                read_capture_flag,
                input_map=["text"],
                output_state="captured_during_run",
                name="read_capture_flag",
            )
        ],
        state_type=DummyState,
        checkpointer=InMemorySaver(),
    )

    # trace_config scopes the capture policy to this invocation only; the process-wide policy is untouched.
    result = await pipeline.invoke(
        {"text": "hello", "captured_during_run": False},
        thread_id="t3",
        trace_config={
            "component_io_capture": ComponentIOCaptureConfig(capture_input=True, capture_output=True)
        },
    )

    print("during invocation, capture_input:", result["captured_during_run"])
    print("after invocation, capture_input:", get_component_io_capture_config().capture_input)


if __name__ == "__main__":
    asyncio.run(main())
