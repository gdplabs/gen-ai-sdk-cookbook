"""Demonstrates best-effort (default) schema inference for a Pipeline.

When `state_type` and `input_type` are omitted, gllm-pipeline infers key-only
(`Any`-valued) schemas from the keys each step declares it reads and writes,
without executing the step code. An explicit schema always takes precedence.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#example-best-effort-inference
"""

import asyncio
from typing import Any

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


def answer(data: dict[str, Any]) -> str:
    return f"processed {data['query']}"


def main() -> None:
    pipe = Pipeline(
        steps=[
            transform(
                answer,
                input_map={"query": "query"},
                output_state="answer",
                name="answer",
            )
        ],
        # state_type and input_type omitted -> inferred from step keys
    )

    tool = pipe.as_tool()
    print(tool.input_schema["properties"].keys())  # dict_keys(['query'])
    print(tool.input_schema["required"])  # ['query']

    result = asyncio.run(tool.invoke(query="hello"))
    print(result["answer"])  # processed hello


if __name__ == "__main__":
    main()
