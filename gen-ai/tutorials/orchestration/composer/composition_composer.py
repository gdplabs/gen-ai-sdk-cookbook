"""Composer composition: fluent chain and subgraph composition.

Covers the corrected GitBook fences:
- whats-a-composer: transform's output_state is keyword-only.
- composition: inner Pipelines are composed with .subgraph(subgraph=...),
  not .step(pipeline).

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#whats-a-composer
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#composition
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline

from .echo import Echo


class SubgraphInnerState(TypedDict):
    query: str
    result: str
    upper_result: str


class SubgraphParentState(TypedDict):
    user_query: str
    subgraph_result: str


async def main() -> None:
    """Composer subgraph: executes another Pipeline as a step.

    Note: output_state_map maps {parent_state_key: subgraph_state_key} —
    parent key first. The GitBook docs show the reversed order in some examples.
    """
    # Fluent chain: output_state on transform is keyword-only.
    sub_pipeline = (
        Pipeline()
        .composer
        .step(Echo(), {"x": "query"}, "result")
        .log("Processing result: {result}")
        .transform(
            lambda data: data["result"].upper(), ["result"], output_state="upper_result"
        )
        .done()
    )
    sub_pipeline.state_type = SubgraphInnerState

    # Compose the inner pipelines as subgraph steps.
    step_a = Pipeline().composer.log("Step A", is_template=False).done()
    step_b = Pipeline().composer.log("Step B", is_template=False).done()
    step_c = Pipeline().composer.log("Step C", is_template=False).done()

    composed_pipeline = (
        Pipeline()
        .composer
        .subgraph(subgraph=step_a)
        .subgraph(subgraph=step_b)
        .subgraph(subgraph=step_c)
        .done()
    )

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
    print(f"transform: upper_result = {result.get('upper_result')}")

    await composed_pipeline.invoke({})
    print("composition: subgraph-composed pipeline ran")


if __name__ == "__main__":
    asyncio.run(main())
