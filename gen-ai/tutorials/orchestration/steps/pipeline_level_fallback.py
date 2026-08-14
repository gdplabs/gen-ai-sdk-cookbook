"""Pipeline-level fallback vs step-level FallbackStepErrorHandler.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps/error-handling#pipeline-level-fallback
"""

import asyncio
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_pipeline.steps.step_error_handler import FallbackStepErrorHandler


class DemoState(TypedDict, total=False):
    user_query: str
    response: str


class RiskyComponent(Component):
    @main
    async def run(self, query: str) -> str:
        raise ConnectionError("Upstream service is unreachable")


class SafeComponent(Component):
    @main
    async def run(self, query: str) -> str:
        return f"Backup answer for: {query}"


async def run_with_pipeline_level_fallback() -> None:
    """No step-level handler, so the error escapes to the pipeline-level fallback."""
    pipeline = Pipeline(
        steps=[
            step(
                RiskyComponent(),
                input_map={"query": "user_query"},
                output_state="response",
                name="primary",
            ),
        ],
        fallback=step(
            SafeComponent(),
            input_map={"query": "user_query"},
            output_state="response",
            name="backup",
        ),
        catch=(ConnectionError, TimeoutError),
        state_type=DemoState,
    )

    state = await pipeline.invoke({"user_query": "Hello!"})
    print("Pipeline-level fallback result:", state["response"])


async def run_with_step_level_handler() -> None:
    """A step-level FallbackStepErrorHandler recovers first, so the pipeline
    never sees the error and its own fallback (if any) does not fire.
    """
    pipeline = Pipeline(
        steps=[
            step(
                RiskyComponent(),
                input_map={"query": "user_query"},
                output_state="response",
                name="primary",
                error_handler=FallbackStepErrorHandler(
                    fallback=lambda error, state, runtime, context: {
                        "response": "Recovered inside the step"
                    }
                ),
            ),
        ],
        # This pipeline-level fallback is unreachable: the step above already
        # recovers, so no exception ever escapes to the pipeline.
        fallback=step(
            SafeComponent(),
            input_map={"query": "user_query"},
            output_state="response",
            name="backup",
        ),
        catch=(ConnectionError, TimeoutError),
        state_type=DemoState,
    )

    state = await pipeline.invoke({"user_query": "Hello!"})
    print("Step-level handler result:", state["response"])


async def main() -> None:
    await run_with_pipeline_level_fallback()
    await run_with_step_level_handler()


if __name__ == "__main__":
    asyncio.run(main())
