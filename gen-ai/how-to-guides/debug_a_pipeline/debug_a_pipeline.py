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
