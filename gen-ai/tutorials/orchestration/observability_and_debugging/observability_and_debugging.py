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

pipeline = Pipeline(
    steps=[transform(to_upper, input_map=["text"], output_state="text_upper", name="to_upper")],
    state_type=DummyState,
    checkpointer=InMemorySaver(),
)
