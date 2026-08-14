"""Runnable example for the pipeline error fallback mechanism.

References:
   [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/pipeline-error-fallback
"""

import argparse
import asyncio
from typing import TypedDict

from gllm_core.logging import LoggerManager
from gllm_inference.component import GenericLMComponent
from gllm_inference.exceptions import BaseInvokerError, ProviderRateLimitError
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import log, step


class MessageState(TypedDict, total=False):
    user_query: str
    response: str
    fallback_response: str


# Nonexistent model: guarantees a real BaseInvokerError at call time so the
# fallback path is exercised without depending on transient provider outages.
primary_component = GenericLMComponent.from_config(
    model_id="openai/gpt-5.4-nano-nonexistent"
)
backup_component = GenericLMComponent.from_config(model_id="openai/gpt-5.4-mini")


def build_basic_fallback_pipeline() -> Pipeline:
    """Single-step fallback: the backup model runs when the primary call fails."""
    return Pipeline(
        steps=[
            step(
                primary_component,
                input_map={"query": "user_query"},
                output_state="response",
                name="primary_lm",
            )
        ],
        fallback=step(
            backup_component,
            input_map={"query": "user_query"},
            output_state="fallback_response",
            name="backup_lm",
        ),
        catch=(BaseInvokerError,),
        state_type=MessageState,
    )


def build_subgraph_fallback_pipeline() -> Pipeline:
    """List fallback: compiled into a backup subgraph that logs then responds."""
    return Pipeline(
        steps=[
            step(
                primary_component,
                input_map={"query": "user_query"},
                output_state="response",
                name="primary_lm",
            )
        ],
        fallback=[
            log("Primary LM call failed — using backup model"),
            step(
                backup_component,
                input_map={"query": "user_query"},
                output_state="fallback_response",
                name="backup_lm",
            ),
        ],
        catch=(BaseInvokerError,),
        state_type=MessageState,
    )


def build_specific_catch_pipeline() -> Pipeline:
    """Only BaseInvokerError (and subclasses) triggers the fallback; other errors propagate."""
    return Pipeline(
        steps=[
            step(
                primary_component,
                input_map={"query": "user_query"},
                output_state="response",
                name="primary_lm",
            )
        ],
        fallback=step(
            backup_component,
            input_map={"query": "user_query"},
            output_state="fallback_response",
            name="backup_lm",
        ),
        catch=(ProviderRateLimitError, BaseInvokerError),
        state_type=MessageState,
    )


def demonstrate_construction_time_validation() -> None:
    """`catch` is validated only when `fallback` is provided; invalid values raise TypeError."""
    for invalid_catch in ((), (int,), (ValueError, "x")):
        try:
            Pipeline(
                [],
                fallback=step(backup_component, name="backup_lm"),
                catch=invalid_catch,
            )
        except TypeError as exc:
            print(f"catch={invalid_catch!r} -> TypeError: {exc}")


def quiet_gllm_logging() -> None:
    """Disable noisy SDK component/error logs so the fallback output is readable."""
    logger_manager = LoggerManager()
    for name in [
        "primary_lm",
        "backup_lm",
        "MainMethodResolver.GenericLMComponent",
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

    pipeline = build_basic_fallback_pipeline()
    state = await pipeline.invoke({"user_query": "Hello!"})
    print(state.get("fallback_response") or state["response"])

    subgraph_pipeline = build_subgraph_fallback_pipeline()
    state = await subgraph_pipeline.invoke({"user_query": "Hello!"})
    print(state.get("fallback_response") or state["response"])

    specific_pipeline = build_specific_catch_pipeline()
    state = await specific_pipeline.invoke({"user_query": "Hello!"})
    print("recovered:", "fallback_response" in state)

    demonstrate_construction_time_validation()


if __name__ == "__main__":
    asyncio.run(main())
