"""Composer concurrency: parallel, map_reduce.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#concurrency
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.types import Group

from .echo import Echo


# -- parallel (direct-style) --

class ParallelState(TypedDict):
    value_a: str
    value_b: str
    result_a: str
    result_b: str


async def demo_parallel() -> None:
    """Composer parallel: runs multiple branches concurrently and merges results.

    Note: branches that produce state output (via output_state) merge correctly.
    Log-only branches (no output_state) can trigger 'NoneType' object is not iterable
    in gllm-pipeline 0.5.18; use steps with output_state for reliable results.
    """
    from gllm_pipeline.steps._func import step as make_step

    step_a = make_step(Echo(), input_map={"x": "value_a"}, output_state="result_a")
    step_b = make_step(Echo(), input_map={"x": "value_b"}, output_state="result_b")

    p = (
        Pipeline()
        .composer
        .parallel(branches=[step_a, step_b])
        .done()
    )
    p.state_type = ParallelState

    result = await p.invoke(
        {"value_a": "A", "value_b": "B", "result_a": "", "result_b": ""}
    )
    print(f"parallel: result_a = {result['result_a']}, result_b = {result['result_b']}")


# -- map_reduce --

class MapReduceState(TypedDict):
    numbers: list
    total: int


async def demo_map_reduce() -> None:
    """Composer map_reduce: maps a function over items, then reduces."""
    p = (
        Pipeline()
        .composer
        .map_reduce(
            input_map={"n": "numbers"},
            output_state="total",
            map_func=lambda item: item["n"],
            reduce_func=sum,
        )
        .done()
    )
    p.state_type = MapReduceState

    result = await p.invoke({"numbers": [1, 2, 3, 4, 5], "total": 0})
    print(f"map_reduce: total = {result['total']}")


# -- map_reduce with Group --

class MapReduceGroupState(TypedDict):
    queries: list
    candidate_groups: list
    ranked: list


async def demo_map_reduce_group() -> None:
    """Composer map_reduce with Group: preserve a full iterable per mapped item."""
    p = (
        Pipeline()
        .composer
        .map_reduce(
            input_map={
                "query": "queries",
                "candidate_pool": Group("candidate_groups"),
            },
            output_state="ranked",
            map_func=lambda item: {
                "query": item["query"],
                "best": item["candidate_pool"][0],
            },
        )
        .done()
    )
    p.state_type = MapReduceGroupState

    result = await p.invoke({
        "queries": ["what is python?", "how to bake bread?"],
        "candidate_groups": ["python-docs", "baking-blog"],
        "ranked": [],
    })
    print(f"map_reduce (Group): ranked = {result['ranked']}")


async def main() -> None:
    await demo_parallel()
    await demo_map_reduce()
    await demo_map_reduce_group()


if __name__ == "__main__":
    asyncio.run(main())
