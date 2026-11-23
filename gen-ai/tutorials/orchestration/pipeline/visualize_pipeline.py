"""Visualize the Pipeline using get_mermaid_diagram().

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#visualizing-the-pipeline
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import bundle, log, transform


class MiniState(TypedDict):
    text: str
    text_upper: str
    text_len: int
    summary: dict


def to_upper(data: dict) -> str:
    return data["text"].upper()


def count_chars(data: dict) -> int:
    return len(data["text_upper"])


async def main() -> None:
    """Build a Pipeline and print its Mermaid diagram."""
    pipe = Pipeline(
        steps=[
            transform(to_upper, input_map=["text"], output_state="text_upper"),
            transform(count_chars, input_map=["text_upper"], output_state="text_len"),
            bundle(["text", "text_upper", "text_len"], output_state="summary"),
            log("Done: {text} -> {text_upper} ({text_len})"),
        ],
        state_type=MiniState,
    )

    diagram = pipe.get_mermaid_diagram()
    print(diagram)


if __name__ == "__main__":
    asyncio.run(main())
