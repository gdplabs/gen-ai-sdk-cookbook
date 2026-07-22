"""Use the leftshift (<<) operator to embed a Pipeline as a subgraph.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-the-leftshift-operator
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import log, transform


class ChildState(TypedDict):
    text: str
    text_upper: str


def to_upper_child(data: dict) -> str:
    return data["text"].upper()


class Parent2State(TypedDict):
    text: str          # overlaps with ChildState.text
    text_upper: str    # overlaps with ChildState.text_upper
    note: str


async def main() -> None:
    """Embed a child Pipeline in a parent via the << operator.
    Subgraphs created this way auto-map overlapping State keys.
    """
    child = Pipeline(
        steps=[
            transform(
                to_upper_child, input_map=["text"], output_state="text_upper"
            )
        ],
        state_type=ChildState,
        name="child",
    )

    parent2 = Pipeline(
        steps=[log("Before: {text}")],
        state_type=Parent2State,
        name="parent2",
    )

    # Include child as a subgraph within parent2
    combined = parent2 << child   # auto-maps overlapping keys

    initial_p2: Parent2State = {
        "text": "Auto-map!",
        "text_upper": "",
        "note": "",
    }
    final_p2 = await combined.invoke(initial_p2)
    print(final_p2["text"], final_p2["text_upper"])


if __name__ == "__main__":
    asyncio.run(main())
