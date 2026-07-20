"""Branching steps: if_else, switch, toggle, guard.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#branching
"""

import asyncio
from pathlib import Path
import sys
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import guard, if_else, log, step, switch, toggle
from gllm_pipeline.types import Val

sys.path.insert(0, str(Path(__file__).parent))
from echo import Echo


# -- if_else --

class IfElseState(TypedDict):
    flag: bool
    feature_status: str


async def demo_if_else() -> None:
    """if_else chooses between two branches based on a condition."""
    feature_on = log("Feature ON", is_template=False)
    feature_off = log("Feature OFF", is_template=False)

    p = Pipeline(
        steps=[
            if_else(
                condition=lambda s: s["flag"],
                if_branch=feature_on,
                else_branch=feature_off,
                output_state="feature_status",
            )
        ],
        state_type=IfElseState,
    )

    result_true = await p.invoke({"flag": True, "feature_status": ""})
    print(f"if_else (flag=True):  feature_status = {result_true['feature_status']}")

    result_false = await p.invoke({"flag": False, "feature_status": ""})
    print(f"if_else (flag=False): feature_status = {result_false['feature_status']}")


# -- if_else with Component condition --

class IfElseComponentState(TypedDict):
    is_adult: str
    condition_result: str
    decision: str


async def demo_if_else_component() -> None:
    """if_else with a Component condition (Echo returns 'x' unchanged)."""
    grant_access = step(
        Echo(),
        input_map={"x": Val("Access granted")},
        output_state="decision",
    )
    deny_access = step(
        Echo(),
        input_map={"x": Val("Access denied")},
        output_state="decision",
    )

    auth_gate = if_else(
        condition=Echo(),
        if_branch=grant_access,
        else_branch=deny_access,
        input_map={"x": "is_adult"},
        output_state="condition_result",
    )

    p = Pipeline(steps=[auth_gate], state_type=IfElseComponentState)
    result = await p.invoke(
        {"is_adult": "true", "condition_result": "", "decision": ""}
    )
    print(f"if_else (Component):  decision = {result['decision']}")

    result2 = await p.invoke(
        {"is_adult": "false", "condition_result": "", "decision": ""}
    )
    print(f"if_else (Component):  decision = {result2['decision']}")


# -- switch --

class SwitchState(TypedDict):
    command: str
    command_type: str


async def demo_switch() -> None:
    """switch selects a branch from a dict of options."""
    dispatch_step = switch(
        condition=lambda s: s["command"],
        branches={
            "search": log("Searching...", is_template=False),
            "filter": log("Filtering...", is_template=False),
        },
        default=log("Unknown command", is_template=False),
        output_state="command_type",
    )

    p = Pipeline(steps=[dispatch_step], state_type=SwitchState)

    result = await p.invoke({"command": "search", "command_type": ""})
    print(f"switch (search): command_type = {result['command_type']}")

    result2 = await p.invoke({"command": "filter", "command_type": ""})
    print(f"switch (filter): command_type = {result2['command_type']}")

    result3 = await p.invoke({"command": "unknown", "command_type": ""})
    print(f"switch (unknown): command_type = {result3['command_type']}")


# -- toggle --

class ToggleState(TypedDict):
    feature_enabled: bool
    feature_status: str


async def demo_toggle() -> None:
    """toggle runs if_branch if condition is truthy (otherwise no_op)."""
    feature_flag_step = toggle(
        condition="feature_enabled",
        if_branch=log("Feature executed", is_template=False),
        output_state="feature_status",
    )

    p = Pipeline(steps=[feature_flag_step], state_type=ToggleState)

    result = await p.invoke({"feature_enabled": True, "feature_status": ""})
    print(f"toggle (enabled):  feature_status = {result['feature_status']}")

    result2 = await p.invoke({"feature_enabled": False, "feature_status": ""})
    print(f"toggle (disabled): feature_status = {result2['feature_status']}")


# -- guard --

class GuardState(TypedDict):
    is_authenticated: bool
    auth_result: str


async def demo_guard() -> None:
    """guard runs success_branch on success,
        or failure_branch + terminate on failure."""
    enforce_auth_step = guard(
        condition=lambda s: s.get("is_authenticated", False),
        success_branch=log("Welcome!", is_template=False),
        output_state="auth_result",
    )

    p = Pipeline(steps=[enforce_auth_step], state_type=GuardState)

    result = await p.invoke({"is_authenticated": True, "auth_result": ""})
    print(f"guard (authenticated): auth_result = {result['auth_result']}")


async def main() -> None:
    await demo_if_else()
    await demo_if_else_component()
    await demo_switch()
    await demo_toggle()
    await demo_guard()


if __name__ == "__main__":
    asyncio.run(main())
