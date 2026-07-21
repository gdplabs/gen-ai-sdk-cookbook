"""Composer composition: subgraph.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#composition
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline

from .echo import Echo


class SubgraphInnerState(TypedDict):
    query: str
    result: str


class SubgraphParentState(TypedDict):
    user_query: str
    subgraph_result: str


async def main() -> None:
    """Composer subgraph: executes another Pipeline as a step.

    Note: output_state_map maps {parent_state_key: subgraph_state_key} —
    parent key first. The GitBook docs show the reversed order in some examples.
    """
    sub_pipeline = (
        Pipeline()
        .composer
        .step(Echo(), input_map={"x": "query"}, output_state="result")
        .done()
    )
    sub_pipeline.state_type = SubgraphInnerState

    p = (
        Pipeline()
        .composer
        .subgraph(
            subgraph=sub_pipeline,
            input_map={"query": "user_query"},
            output_state_map={"subgraph_result": "result"},
        )
        .done()
    )
    p.state_type = SubgraphParentState

    result = await p.invoke({"user_query": "test", "subgraph_result": ""})
    print(f"subgraph: subgraph_result = {result['subgraph_result']}")


if __name__ == "__main__":
    asyncio.run(main())
