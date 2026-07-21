"""Composer builder-style branching: when/then/otherwise,
    switch/case/default, toggle/then, guard/on_success/on_failure,
    parallel/fork.

The builder-style API uses fluent chaining (e.g. `.when().then().otherwise().end()`)
as opposed to the direct-style API (e.g. `.if_else(condition, if_branch, else_branch)`).

Note: In gllm-pipeline 0.5.18, builder-style branches must use step
    objects (not Pipeline
objects) as branch arguments. Passing a full Pipeline as a branch triggers an
`AttributeError: 'Pipeline' object has no attribute 'is_excluded'` during graph
compilation. The GitBook examples use Pipeline objects; this cookbook uses steps.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#branching
"""

import asyncio
from typing import Any, TypedDict

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import log, step

from .echo import Echo


# -- when/then/otherwise/end --

class WhenState(TypedDict):
    flag: bool
    feature_status: Any


async def demo_when_then() -> None:
    """Builder-style when().then().otherwise().end()."""
    p = (
        Pipeline()
        .composer
        .when(lambda s: s["flag"])
            .then(step(Echo(), input_map={"x": "flag"}, output_state="feature_status"))
            .otherwise(log("Feature OFF", is_template=False))
            .end()
        .done()
    )
    p.state_type = WhenState

    result_true = await p.invoke({"flag": True, "feature_status": ""})
    print(f"when/then (true):  feature_status = {result_true['feature_status']}")

    result_false = await p.invoke({"flag": False, "feature_status": ""})
    print(f"when/then (false): feature_status = {result_false['feature_status']}")


# -- switch/case/default/end --

class SwitchState(TypedDict):
    command: str
    command_type: str


async def demo_switch_case() -> None:
    """Builder-style switch().case().default().end()."""
    p = (
        Pipeline()
        .composer
        .switch(lambda s: s["command"])
            .case("search", log("Searching...", is_template=False))
            .case("filter", log("Filtering...", is_template=False))
            .default(log("Unknown command", is_template=False))
            .end()
        .done()
    )
    p.state_type = SwitchState

    result = await p.invoke({"command": "search", "command_type": ""})
    print(f"switch/case (search):  command_type = {result['command_type']}")

    result2 = await p.invoke({"command": "filter", "command_type": ""})
    print(f"switch/case (filter):  command_type = {result2['command_type']}")


# -- toggle/then/end --

class ToggleState(TypedDict):
    feature_enabled: bool
    feature_status: str


async def demo_toggle_then() -> None:
    """Builder-style toggle().then().end()."""
    p = (
        Pipeline()
        .composer
        .toggle("feature_enabled")
            .then(log("Feature executed", is_template=False))
            .end()
        .done()
    )
    p.state_type = ToggleState

    result = await p.invoke({"feature_enabled": True, "feature_status": ""})
    print(f"toggle/then (enabled):  feature_status = {result['feature_status']}")

    result2 = await p.invoke({"feature_enabled": False, "feature_status": ""})
    print(f"toggle/then (disabled): feature_status = {result2['feature_status']}")


# -- guard/on_success/on_failure/end --

class GuardState(TypedDict):
    is_authenticated: bool
    auth_result: str


async def demo_guard_builder() -> None:
    """Builder-style guard().on_success().on_failure().end()."""
    p = (
        Pipeline()
        .composer
        .guard(lambda s: s.get("is_authenticated", False))
            .on_success(log("Welcome!", is_template=False))
            .on_failure(log("Access denied!", is_template=False))
            .end()
        .done()
    )
    p.state_type = GuardState

    result = await p.invoke({"is_authenticated": True, "auth_result": ""})
    print(f"guard (auth): auth_result = {result['auth_result']}")


# -- parallel/fork/end --

class ParallelState(TypedDict):
    value_a: str
    value_b: str
    result_a: str
    result_b: str


async def demo_parallel_fork() -> None:
    """Builder-style parallel().fork().end()."""
    p = (
        Pipeline()
        .composer
        .parallel()
            .fork(step(Echo(), input_map={"x": "value_a"}, output_state="result_a"))
            .fork(step(Echo(), input_map={"x": "value_b"}, output_state="result_b"))
            .end()
        .done()
    )
    p.state_type = ParallelState

    result = await p.invoke(
        {"value_a": "A", "value_b": "B", "result_a": "", "result_b": ""}
    )
    print(f"parallel/fork: result_a = {result['result_a']}, "
      f"result_b = {result['result_b']}")


async def main() -> None:
    await demo_when_then()
    await demo_switch_case()
    await demo_toggle_then()
    await demo_guard_builder()
    await demo_parallel_fork()


if __name__ == "__main__":
    asyncio.run(main())
