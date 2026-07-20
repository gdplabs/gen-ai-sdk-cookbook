"""Concurrency steps: parallel, map_reduce.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#concurrency
"""

import asyncio
from pathlib import Path
import sys
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import map_reduce, parallel, step
from gllm_pipeline.types import Group, Val

sys.path.insert(0, str(Path(__file__).parent))
from echo import Echo


# -- parallel --

class ParallelState(TypedDict):
    value_a: str
    value_b: str
    result_a: str
    result_b: str


async def demo_parallel() -> None:
    """parallel runs multiple branches concurrently and merges results.

    Note: branches that produce state output (via output_state) merge correctly.
    Log-only branches (no output_state) can trigger 'NoneType' object is not iterable
    in gllm-pipeline 0.5.18; use steps with output_state for reliable results.
    """
    parallel_step = parallel(
        branches=[
            step(Echo(), input_map={"x": "value_a"}, output_state="result_a"),
            step(Echo(), input_map={"x": "value_b"}, output_state="result_b"),
        ],
    )

    p = Pipeline(steps=[parallel_step], state_type=ParallelState)
    result = await p.invoke(
        {"value_a": "A", "value_b": "B", "result_a": "", "result_b": ""}
    )
    print(f"parallel: result_a = {result['result_a']}, result_b = {result['result_b']}")


# -- map_reduce (simple) --

class MapReduceState(TypedDict):
    numbers: list
    total: int


async def demo_map_reduce_simple() -> None:
    """map_reduce maps a function over items, then reduces results."""
    sum_step = map_reduce(
        input_map={"n": "numbers"},
        output_state="total",
        map_func=lambda item: item["n"],
        reduce_func=sum,
    )

    p = Pipeline(steps=[sum_step], state_type=MapReduceState)
    result = await p.invoke({"numbers": [1, 2, 3, 4, 5], "total": 0})
    print(f"map_reduce: total = {result['total']}")


# -- map_reduce with Group --

class MapReduceGroupState(TypedDict):
    queries: list
    candidate_groups: list
    ranked_results: list


async def demo_map_reduce_group() -> None:
    """map_reduce with Group: preserve a full iterable per mapped item."""

    rank_step = map_reduce(
        input_map={
            "query": "queries",
            "candidates": Group("candidate_groups"),
        },
        output_state="ranked_results",
        map_func=lambda item: {
            "query": item["query"],
            "top_candidate": item["candidates"][0],
        },
    )

    p = Pipeline(steps=[rank_step], state_type=MapReduceGroupState)
    result = await p.invoke({
        "queries": ["what is python?", "how to bake bread?"],
        "candidate_groups": ["python-docs", "baking-blog"],
        "ranked_results": [],
    })
    print(f"map_reduce (Group): ranked_results = {result['ranked_results']}")


# -- map_reduce with Val + Group --

class MapReduceValGroupState(TypedDict):
    queries: list
    candidate_groups: list
    ranked_results: list


async def demo_map_reduce_val_group() -> None:
    """map_reduce with Group(Val(...)): grouped literal iterable."""

    rank_step = map_reduce(
        input_map={
            "query": "queries",
            "candidates": Group("candidate_groups"),
            "labels": Group(Val(["relevant", "neutral"])),
        },
        output_state="ranked_results",
        map_func=lambda item: {
            "query": item["query"],
            "top_candidate": item["candidates"][0],
            "labels": item["labels"],
        },
    )

    p = Pipeline(steps=[rank_step], state_type=MapReduceValGroupState)
    result = await p.invoke({
        "queries": ["q1", "q2"],
        "candidate_groups": ["c1", "c2"],
        "ranked_results": [],
    })
    print(f"map_reduce (Val+Group): ranked_results = {result['ranked_results']}")


async def main() -> None:
    await demo_parallel()
    await demo_map_reduce_simple()
    await demo_map_reduce_group()
    await demo_map_reduce_val_group()


if __name__ == "__main__":
    asyncio.run(main())
