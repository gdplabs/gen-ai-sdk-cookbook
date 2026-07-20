"""Basic steps: step, transform, bundle, copy, log, no_op, terminate.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#basic-steps
"""

import asyncio
from pathlib import Path
import sys
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import bundle, copy, log, no_op, step, transform
from gllm_pipeline.steps._func import terminate

sys.path.insert(0, str(Path(__file__).parent))
from echo import Echo


class BasicStepState(TypedDict):
    value: str
    answer: str
    text: str
    upper_text: str
    user: str
    query: str
    payload: dict
    input_data: str
    output_data: str


def to_uppercase(data: dict) -> str:
    """Make a string uppercase."""
    return data["text"].upper()


async def main() -> None:
    """Demonstrate basic pipeline steps."""

    # --- step ---
    echo_step = step(
        component=Echo(),
        input_map={"x": "value"},
        output_state="answer",
    )
    p_step = Pipeline(steps=[echo_step], state_type=BasicStepState)
    result = await p_step.invoke(
        {"value": "hello", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "", "payload": {}, "input_data": "", "output_data": ""}
    )
    print(f"step: answer = {result['answer']}")

    # --- transform ---
    transform_step = transform(
        operation=to_uppercase,
        input_map=["text"],
        output_state="upper_text",
    )
    p_transform = Pipeline(steps=[transform_step], state_type=BasicStepState)
    result = await p_transform.invoke(
        {"value": "", "answer": "", "text": "hello world", "upper_text": "",
         "user": "", "query": "", "payload": {}, "input_data": "", "output_data": ""}
    )
    print(f"transform: upper_text = {result['upper_text']}")

    # --- bundle ---
    bundle_step = bundle(
        input_states=["user", "query"],
        output_state="payload",
    )
    p_bundle = Pipeline(steps=[bundle_step], state_type=BasicStepState)
    result = await p_bundle.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "alice", "query": "search", "payload": {},
         "input_data": "", "output_data": ""}
    )
    print(f"bundle: payload = {result['payload']}")

    # --- copy ---
    copy_step = copy("input_data", "output_data")
    p_copy = Pipeline(steps=[copy_step], state_type=BasicStepState)
    result = await p_copy.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "", "payload": {},
         "input_data": "duplicated", "output_data": ""}
    )
    print(f"copy: output_data = {result['output_data']}")

    # --- log ---
    log_step1 = log("Processing...", is_template=False)
    log_step2 = log("User: {user}, Query: {query}")
    p_log = Pipeline(steps=[log_step1, log_step2], state_type=BasicStepState)
    result = await p_log.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "alice", "query": "hello", "payload": {},
         "input_data": "", "output_data": ""}
    )
    print("log: messages emitted")

    # --- no_op ---
    no_op_step = no_op()
    p_noop = Pipeline(steps=[no_op_step], state_type=BasicStepState)
    result = await p_noop.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "", "payload": {}, "input_data": "", "output_data": ""}
    )
    print(f"no_op: state unchanged = {result['value']}")

    # --- terminate ---
    terminate_step = terminate()
    p_terminate = Pipeline(steps=[terminate_step], state_type=BasicStepState)
    result = await p_terminate.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "", "payload": {}, "input_data": "", "output_data": ""}
    )
    print("terminate: pipeline stopped")


if __name__ == "__main__":
    asyncio.run(main())
