"""Use a Pipeline as a Subgraph within another Pipeline.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-a-pipeline-as-a-subgraph
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import log, subgraph, transform


class ChildState(TypedDict):
    text: str
    text_upper: str


def to_upper_child(data: dict) -> str:
    return data["text"].upper()


class ParentState(TypedDict):
    input_text: str
    result_upper: str
    text_len: int


def count_len_parent(data: dict) -> int:
    return len(data["result_upper"])


async def main() -> None:
    """Embed a child Pipeline inside a parent Pipeline via subgraph()."""
    child = Pipeline(
        steps=[
            transform(
                to_upper_child, input_map=["text"], output_state="text_upper"
            )
        ],
        state_type=ChildState,
        name="child_pipeline",
    )

    parent = Pipeline(
        steps=[
            subgraph(
                child,
                input_map={"text": "input_text"},
                output_state_map={"result_upper": "text_upper"},
            ),
            transform(
                count_len_parent,
                input_map=["result_upper"],
                output_state="text_len",
            ),
            log("Parent upper='{result_upper}' (len={text_len})"),
        ],
        state_type=ParentState,
    )

    initial_parent: ParentState = {
        "input_text": "SubGraph Rocks!",
        "result_upper": "",
        "text_len": 0,
    }
    final_parent = await parent.invoke(initial_parent)
    print(final_parent)


if __name__ == "__main__":
    asyncio.run(main())
