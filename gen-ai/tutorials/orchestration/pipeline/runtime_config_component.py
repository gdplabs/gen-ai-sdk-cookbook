"""Runtime Configuration with Component condition and if_else branching.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#runtime-configuration
"""

import asyncio
from typing import Any, TypedDict

from gllm_core.schema import Component
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import if_else, transform


class GreaterThan(Component):
    """Component that returns 'true' if value > threshold else 'false'."""

    def decide(self, value: int, threshold: int) -> str:
        """Return 'true' if value > threshold else 'false'."""
        return "true" if value > threshold else "false"

    async def _run(self, **kwargs: Any) -> str:
        """Implements the core logic; called by Component.run(...)."""
        value: int = kwargs["value"]
        threshold: int = kwargs["threshold"]
        return self.decide(value, threshold)


class DecisionState(TypedDict):
    value: int
    threshold: int
    decision: str
    msg: str


async def main() -> None:
    """Use if_else with a Component condition and runtime config."""
    higher = transform(
        lambda _data: "value > threshold", input_map=[], output_state="msg"
    )
    lower_eq = transform(
        lambda _data: "value <= threshold", input_map=[], output_state="msg"
    )

    cond_comp = GreaterThan()

    greater_than_step = if_else(
        condition=cond_comp,
        if_branch=higher,
        else_branch=lower_eq,
        input_map={"value": "value", "threshold": "threshold"},
        output_state="decision",
    )

    pipe = Pipeline(
        steps=[greater_than_step],
        state_type=DecisionState,
    )

    # value > threshold → "true" branch
    result1 = await pipe.invoke(
        {"value": 10, "threshold": 5, "decision": "", "msg": ""},
        config={"value": 10, "threshold": 5},
    )
    print(result1)

    # value <= threshold → "false" branch
    result2 = await pipe.invoke(
        {"value": 3, "threshold": 5, "decision": "", "msg": ""},
        config={"value": 3, "threshold": 5},
    )
    print(result2)


if __name__ == "__main__":
    asyncio.run(main())
