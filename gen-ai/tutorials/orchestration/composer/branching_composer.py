"""Composer branching: if_else, switch, toggle, guard (direct-style).

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#branching
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import log, step
from gllm_pipeline.types import Val

from .echo import Echo


# -- if_else (direct-style) --

class IfElseState(TypedDict):
    flag: bool
    feature_status: str


async def demo_if_else() -> None:
    """Composer if_else: direct-style when both branches are ready.

    Note: In gllm-pipeline 0.5.18, branches must use step objects (not Pipeline
    objects) to avoid 'Pipeline' object has no attribute 'is_excluded' during
    graph compilation. The GitBook docs use Pipeline objects as branches.
    """
    feature_on = log("Feature ON", is_template=False)
    feature_off = log("Feature OFF", is_template=False)

    p = (
        Pipeline()
        .composer
        .if_else(
            condition=lambda s: s["flag"],
            if_branch=feature_on,
            else_branch=feature_off,
            output_state="feature_status",
        )
        .done()
    )
    p.state_type = IfElseState

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
    """Composer if_else with a Component condition."""
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

    p = (
        Pipeline()
        .composer
        .if_else(
            condition=Echo(),
            if_branch=grant_access,
            else_branch=deny_access,
            input_map={"x": "is_adult"},
            output_state="condition_result",
        )
        .done()
    )
    p.state_type = IfElseComponentState

    result = await p.invoke(
        {"is_adult": "true", "condition_result": "", "decision": ""}
    )
    print(f"if_else (Component, adult):  decision = {result['decision']}")

    result2 = await p.invoke(
        {"is_adult": "false", "condition_result": "", "decision": ""}
    )
    print(f"if_else (Component, minor):  decision = {result2['decision']}")


# -- switch (direct-style) --

class SwitchState(TypedDict):
    command: str
    command_type: str


async def demo_switch() -> None:
    """Composer switch: direct-style with branches dict."""
    search_step = log("Searching...", is_template=False)
    filter_step = log("Filtering...", is_template=False)
    unknown_step = log("Unknown command", is_template=False)

    p = (
        Pipeline()
        .composer
        .switch(
            condition=lambda s: s["command"],
            branches={"search": search_step, "filter": filter_step},
            default=unknown_step,
            output_state="command_type",
        )
        .done()
    )
    p.state_type = SwitchState

    result = await p.invoke({"command": "search", "command_type": ""})
    print(f"switch (search):  command_type = {result['command_type']}")

    result2 = await p.invoke({"command": "filter", "command_type": ""})
    print(f"switch (filter):  command_type = {result2['command_type']}")


# -- toggle (direct-style) --

class ToggleState(TypedDict):
    feature_enabled: bool
    feature_status: str


async def demo_toggle() -> None:
    """Composer toggle: runs if_branch when condition is truthy."""
    feature_step = log("Feature executed", is_template=False)

    p = (
        Pipeline()
        .composer
        .toggle(
            condition="feature_enabled",
            if_branch=feature_step,
            output_state="feature_status",
        )
        .done()
    )
    p.state_type = ToggleState

    result = await p.invoke({"feature_enabled": True, "feature_status": ""})
    print(f"toggle (enabled):  feature_status = {result['feature_status']}")

    result2 = await p.invoke({"feature_enabled": False, "feature_status": ""})
    print(f"toggle (disabled): feature_status = {result2['feature_status']}")


# -- guard (direct-style) --

class GuardState(TypedDict):
    is_authenticated: bool
    auth_result: str


async def demo_guard() -> None:
    """Composer guard: success_branch on success, failure + terminate on failure."""
    welcome_step = log("Welcome!", is_template=False)

    p = (
        Pipeline()
        .composer
        .guard(
            condition=lambda s: s.get("is_authenticated", False),
            success_branch=welcome_step,
            output_state="auth_result",
        )
        .done()
    )
    p.state_type = GuardState

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
