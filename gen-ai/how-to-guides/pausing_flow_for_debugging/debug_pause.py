"""Runnable example for pausing pipeline execution for debugging."""

import asyncio
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import pause, step
from langgraph.checkpoint.memory import MemorySaver


class PipelineState(TypedDict, total=False):
    topic: str
    raw_data: str
    result: str


class FetchDataComponent(Component):
    @main
    async def run(self, topic: str) -> str:
        return f"Fetched data for topic: {topic}"


class ProcessDataComponent(Component):
    @main
    async def run(self, raw_data: str) -> str:
        return f"Processed: {raw_data}"


def build_pipeline() -> Pipeline:
    fetch_data = step(
        FetchDataComponent(),
        output_state="raw_data",
        input_map={"topic": "topic"},
        name="fetch_data",
    )
    process = step(
        ProcessDataComponent(),
        output_state="result",
        input_map={"raw_data": "raw_data"},
        name="process",
    )
    return Pipeline(
        steps=[
            fetch_data,
            pause(name="before_processing"),
            process,
        ],
        state_type=PipelineState,
        checkpointer=MemorySaver(),
        name="debug_pause_demo",
    )


async def main() -> None:
    pipeline = build_pipeline()
    config = {"thread_id": "debug-session-1"}

    paused_state = await pipeline.invoke(
        {"topic": "AI Testing"},
        config=config,
        interrupt_before=["before_processing"],
    )
    print(f"Paused state: {paused_state}")

    final_state = await pipeline.invoke(None, config=config)
    print(f"Final state: {final_state}")


if __name__ == "__main__":
    asyncio.run(main())
