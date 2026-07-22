"""Runtime Configuration with config-driven switches via input_map.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#runtime-configuration
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class CfgState(TypedDict):
    text: str
    result: str


def format_text(data: dict) -> str:
    """Operation uses config-driven switches."""
    s = data["text"]
    if data["reverse"]:
        s = s[::-1]
    if data["uppercase"]:
        s = s.upper()
    return s


async def main() -> None:
    """Run a Pipeline with runtime configuration."""
    pipe = Pipeline(
        steps=[
            transform(
                format_text,
                input_map=["text", "reverse", "uppercase"],
                output_state="result",
            )
        ],
        state_type=CfgState,
    )

    # Provide all required config keys listed in input_map
    state: CfgState = {"text": "Hello", "result": ""}
    out = await pipe.invoke(state, config={"reverse": False, "uppercase": True})
    print(out["result"])  # HELLO

    out2 = await pipe.invoke(
        {"text": "Hello", "result": ""}, config={"reverse": True, "uppercase": True}
    )
    print(out2["result"])  # OLLEH


if __name__ == "__main__":
    asyncio.run(main())
