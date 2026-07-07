from typing import TypedDict

from gllm_core.schema import Component, main
from langgraph.checkpoint.memory import MemorySaver

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import pause, step


class PipelineState(TypedDict, total=False):
    topic: str
    raw_data: str
    result: str


# Simple, self-contained Component classes for demonstration
class FetchDataComponent(Component):
    @main
    async def run(self, topic: str) -> str:
        return f"Fetched data for topic: {topic}"


class ProcessDataComponent(Component):
    @main
    async def run(self, raw_data: str) -> str:
        return f"Processed: {raw_data}"


memory = MemorySaver()

fetch_data = step(FetchDataComponent(), output_state="raw_data", input_map={"topic": "topic"}, name="fetch_data")
process = step(ProcessDataComponent(), output_state="result", input_map={"raw_data": "raw_data"}, name="process")

pipeline = Pipeline(
    steps=[
        fetch_data,
        # Named marker — activate it at invocation time via interrupt_before / interrupt_after
        pause(name="before_processing"),
        process,
    ],
    state_type=PipelineState,
    checkpointer=memory,
)
