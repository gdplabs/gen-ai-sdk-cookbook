"""Composition steps: log, subgraph.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#composition
"""

import asyncio
from pathlib import Path
import sys
from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import log, step, subgraph

sys.path.insert(0, str(Path(__file__).parent))
from echo import Echo


# -- log --

class LogState(TypedDict):
    user_id: str
    query: str


async def demo_log() -> None:
    """log emits a message through an event emitter."""
    plain = log("Processing...", is_template=False)
    templated = log("User: {user_id}, Query: {query}")

    p = Pipeline(steps=[plain, templated], state_type=LogState)
    await p.invoke({"user_id": "alice", "query": "hello"})
    print("log: messages emitted")


# -- subgraph --

class SubgraphInnerState(TypedDict):
    query: str
    result: str


class SubgraphParentState(TypedDict):
    user_query: str
    subgraph_result: str


async def demo_subgraph() -> None:
    """subgraph executes another Pipeline as a step.

    Note: output_state_map maps {parent_state_key: subgraph_state_key}.
    The GitBook docs show {result: subgraph_result} but the correct
    direction is {subgraph_result: result} — parent key first.
    """
    sub_pipeline = Pipeline(
        steps=[step(Echo(), input_map={"x": "query"}, output_state="result")],
        state_type=SubgraphInnerState,
    )

    use_subgraph = subgraph(
        subgraph=sub_pipeline,
        input_map={"query": "user_query"},
        output_state_map={"subgraph_result": "result"},
    )

    p = Pipeline(steps=[use_subgraph], state_type=SubgraphParentState)
    result = await p.invoke({"user_query": "test", "subgraph_result": ""})
    print(f"subgraph: subgraph_result = {result['subgraph_result']}")


async def main() -> None:
    await demo_log()
    await demo_subgraph()


if __name__ == "__main__":
    asyncio.run(main())
