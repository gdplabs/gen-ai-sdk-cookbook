"""Flow control steps: goto, no_op, terminate, guard, while_do, try_catch,
interrupt, pause.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#flow-control
"""

import asyncio
from pathlib import Path
import sys
from typing import TypedDict

from gllm_core.schema import main
from gllm_core.schema.component import Component
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import (
    goto,
    guard,
    log,
    pause,
    step,
    try_catch,
    while_do,
)

sys.path.insert(0, str(Path(__file__).parent))
from echo import Echo


# -- while_do --

class ProcessingState(TypedDict):
    data: str
    status: str


class Processor(Component):
    """A component that processes data and returns 'success' after one call."""

    @main
    async def process(self, input: str) -> str:
        return "success"


def check_success(data: dict) -> bool:
    """Continue looping if status is not 'success'."""
    return data.get("status") != "success"


async def demo_while_do() -> None:
    """while_do creates a do-while loop: body runs at least once."""
    loop_step = while_do(
        body=step(Processor(), input_map={"input": "data"}, output_state="status"),
        condition=check_success,
    )

    p = Pipeline(steps=[loop_step], state_type=ProcessingState)
    result = await p.invoke({"data": "process me", "status": ""})
    print(f"while_do: status = {result['status']}")


# -- try_catch --

class TryCatchState(TypedDict):
    answer: str


class Fallback(Component):
    """Fallback component that returns a safe answer."""

    @main
    async def safe_answer(self) -> str:
        return "fallback answer"


class RiskyComponent(Component):
    """Component that raises an exception."""

    @main
    async def risky(self, query: str) -> str:
        raise ConnectionError("API unavailable")


async def demo_try_catch() -> None:
    """try_catch executes a body and falls back on exception."""
    safe_step = try_catch(
        body=step(
            RiskyComponent(),
            input_map={"query": "question"},
            output_state="answer",
        ),
        fallback=step(Fallback(), output_state="answer"),
        catch=(ConnectionError, TimeoutError),
        caught_exception_state="last_error",
    )

    class TCState(TypedDict):
        question: str
        answer: str
        last_error: str

    p = Pipeline(steps=[safe_step], state_type=TCState)
    result = await p.invoke(
        {"question": "What is AI?", "answer": "", "last_error": ""}
    )
    answer = result["answer"]
    last_error = result.get("last_error", "")
    print(f"try_catch: answer = {answer}, last_error = {last_error}")


# -- pause --

class PauseState(TypedDict):
    value: str


async def demo_pause() -> None:
    """pause is a marker step (no-op) used as a debugging breakpoint target."""
    bp = pause(name="before_output")

    p = Pipeline(
        steps=[
            step(Echo(), input_map={"x": "value"}, output_state="value"),
            bp,
        ],
        state_type=PauseState,
    )
    result = await p.invoke({"value": "hello"})
    print(f"pause: value = {result['value']} (pause is a no-op marker)")

    # Debug run: interrupt before the named pause step
    result_debug = await p.invoke(
        {"value": "hello"},
        interrupt_before=["before_output"],
    )
    value = result_debug["value"]
    print(f"pause (interrupt_before): value = {value} (halted before pause)")


# -- goto --

class GotoState(TypedDict):
    next_step_name_key: str


async def demo_goto() -> None:
    """goto allows jumping to another step in the pipeline."""
    # Jump based on state: reads target from state["next_step_name_key"]
    goto(name="dynamic_jump", target="next_step_name_key")

    # For a minimal demo, we show the construction of a goto step.
    # Full goto usage requires a multi-step pipeline with named steps.
    print(
        "goto: step constructed (requires multi-step pipeline to demonstrate fully)"
    )


# -- guard (already in branching_steps.py, but shown here for completeness) --


class GuardState(TypedDict):
    is_authenticated: bool
    auth_result: str


async def demo_guard() -> None:
    """guard runs success_branch on success or failure branch on failure."""
    enforce_auth_step = guard(
        condition=lambda s: s.get("is_authenticated", False),
        success_branch=log("Welcome!", is_template=False),
        failure_branch=log("Access denied", is_template=False),
        output_state="auth_result",
    )

    p = Pipeline(steps=[enforce_auth_step], state_type=GuardState)
    result = await p.invoke({"is_authenticated": True, "auth_result": ""})
    print(f"guard: auth_result = {result['auth_result']}")


async def main() -> None:
    await demo_while_do()
    await demo_try_catch()
    await demo_pause()
    await demo_goto()
    await demo_guard()


if __name__ == "__main__":
    asyncio.run(main())
