"""Runnable example for the pipeline error fallback mechanism.

Mirrors the GitBook guide:
https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/pipeline-error-fallback

This example demonstrates how to make a pipeline resilient to transient
failures by configuring ``fallback`` and ``catch`` on ``Pipeline``:

* ``fallback`` is a ``BasePipelineStep`` (or a list of them, compiled into a
  backup subgraph) executed when an error escapes the main graph execution.
* ``catch`` is a tuple of exception types that should trigger the fallback.
  Defaults to ``(Exception,)`` (catch everything).
"""

import argparse
import asyncio
from typing import TypedDict

from gllm_core.logging import LoggerManager
from gllm_core.schema import Component
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import log, step


class MessageState(TypedDict, total=False):
    user_query: str
    response: str
    fallback_response: str


class RiskyService(Component):
    """Simulates a call to an external service that can fail."""

    async def _run(self, query: str = "") -> str:
        raise ValueError("External service is temporarily unavailable")
        # In real usage this would return: f"Live answer for: {query}"


class SafeService(Component):
    """A safe fallback that always succeeds."""

    async def _run(self, query: str = "") -> str:
        return f"Fallback answer for: {query}"


def build_basic_fallback_pipeline() -> Pipeline:
    """Single-step fallback: one backup step runs when the main step fails."""
    return Pipeline(
        steps=[
            step(
                RiskyService(),
                input_map={"query": "user_query"},
                output_state="response",
                name="risky_service",
            )
        ],
        fallback=step(
            SafeService(),
            input_map={"query": "user_query"},
            output_state="fallback_response",
            name="safe_service",
        ),
        catch=(ValueError,),
        state_type=MessageState,
    )


def build_subgraph_fallback_pipeline() -> Pipeline:
    """List fallback: compiled into a backup subgraph that logs then responds."""
    return Pipeline(
        steps=[
            step(
                RiskyService(),
                input_map={"query": "user_query"},
                output_state="response",
                name="risky_service",
            )
        ],
        fallback=[
            log("Primary service failed — using fallback"),
            step(
                SafeService(),
                input_map={"query": "user_query"},
                output_state="fallback_response",
                name="safe_service",
            ),
        ],
        catch=(ValueError,),
        state_type=MessageState,
    )


def build_specific_catch_pipeline() -> Pipeline:
    """Only ValueError triggers the fallback; other errors propagate."""
    return Pipeline(
        steps=[
            step(
                RiskyService(),
                input_map={"query": "user_query"},
                output_state="response",
                name="risky_service",
            )
        ],
        fallback=step(
            SafeService(),
            input_map={"query": "user_query"},
            output_state="fallback_response",
            name="safe_service",
        ),
        catch=(ValueError,),
        state_type=MessageState,
    )


def quiet_gllm_logging() -> None:
    """Disable noisy SDK component/error logs so the fallback output is readable."""
    logger_manager = LoggerManager()
    for name in [
        "RiskyService",
        "SafeService",
        "risky_service",
        "safe_service",
        "MainMethodResolver.RiskyService",
        "MainMethodResolver.SafeService",
        "RaiseStepErrorHandler",
    ]:
        logger_manager.get_logger(name).disabled = True


async def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline error fallback example")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable noisy step/error logs to make the fallback output easier to read",
    )
    args = parser.parse_args()

    if args.quiet:
        quiet_gllm_logging()

    # 1. Basic fallback: the risky service fails, the fallback recovers.
    pipeline = build_basic_fallback_pipeline()
    state = await pipeline.invoke({"user_query": "Hello!"})
    print(state["fallback_response"])  # "Fallback answer for: Hello!"

    # 2. Fallback as a backup subgraph (logs the failure, then produces a response).
    subgraph_pipeline = build_subgraph_fallback_pipeline()
    state = await subgraph_pipeline.invoke({"user_query": "Hello!"})
    print(state["fallback_response"])  # "Fallback answer for: Hello!"

    # 3. Catching only specific errors: ValueError is caught and recovered from.
    specific_pipeline = build_specific_catch_pipeline()
    state = await specific_pipeline.invoke({"user_query": "Hello!"})
    print("recovered:", "fallback_response" in state)  # True


if __name__ == "__main__":
    asyncio.run(main())
