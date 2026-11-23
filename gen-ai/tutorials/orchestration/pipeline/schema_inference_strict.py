"""Demonstrates strict schema inference (infer_schema=True) raising on unsafe steps.

`infer_schema=True` makes inference strict: when a step's keys cannot be proven
(e.g. a control-flow step such as `if_else` whose branch outputs are not
guaranteed on every path), gllm-pipeline raises `PipelineSchemaError` instead of
silently falling back to the prior default behavior.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#example-strict-inference-with-an-unsafe-step
"""

import asyncio

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import if_else, transform
from gllm_pipeline.utils.schema_inference import PipelineSchemaError

true_branch = transform(
    lambda data: data["query"],
    input_map={"query": "query"},
    output_state="true_answer",
    name="true_branch",
)
false_branch = transform(
    lambda data: data["query"],
    input_map={"query": "query"},
    output_state="false_answer",
    name="false_branch",
)


def main() -> None:
    pipe = Pipeline(
        steps=[
            if_else(
                lambda state: bool(state["flag"]),
                true_branch,
                false_branch,
                input_map={"flag": "flag"},
                name="route",
            )
        ],
        infer_schema=True,  # strict: raise instead of falling back
    )

    try:
        asyncio.run(pipe.as_tool().invoke(flag=True))
    except PipelineSchemaError as e:
        print(
            e
        )  # Cannot infer pipeline schemas because step 'route' has conditional output keys.


if __name__ == "__main__":
    main()
