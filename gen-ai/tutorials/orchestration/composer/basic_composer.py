"""Basic Composer methods: step, transform, bundle, log, no_op, terminate.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#basic-composer-methods
"""

import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline import Pipeline

from .echo import Echo


class ComposerBasicState(TypedDict):
    value: str
    answer: str
    text: str
    upper_text: str
    user: str
    query: str
    payload: dict
    user_id: str


def uppercase(data: dict) -> str:
    """Make a string uppercase."""
    return data["text"].upper()


async def main() -> None:
    """Demonstrate basic Composer fluent API methods."""

    # --- step ---
    p_step = (
        Pipeline()
        .composer
        .step(
            component=Echo(),
            input_map={"x": "value"},
            output_state="answer",
        )
        .done()
    )
    p_step.state_type = ComposerBasicState
    result = await p_step.invoke(
        {"value": "hello", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "", "payload": {}, "user_id": ""}
    )
    print(f"composer.step: answer = {result['answer']}")

    # --- transform ---
    p_transform = (
        Pipeline()
        .composer
        .transform(
            operation=uppercase,
            input_map=["text"],
            output_state="upper_text",
        )
        .done()
    )
    p_transform.state_type = ComposerBasicState
    result = await p_transform.invoke(
        {"value": "", "answer": "", "text": "hello world", "upper_text": "",
         "user": "", "query": "", "payload": {}, "user_id": ""}
    )
    print(f"composer.transform: upper_text = {result['upper_text']}")

    # --- bundle ---
    p_bundle = (
        Pipeline()
        .composer
        .bundle(
            input_states=["user", "query"],
            output_state="payload",
        )
        .done()
    )
    p_bundle.state_type = ComposerBasicState
    result = await p_bundle.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "alice", "query": "search", "payload": {}, "user_id": ""}
    )
    print(f"composer.bundle: payload = {result['payload']}")

    # --- log ---
    p_log = (
        Pipeline()
        .composer
        .log("Processing...", is_template=False)
        .log("User: {user_id}, Query: {query}")
        .done()
    )
    p_log.state_type = ComposerBasicState
    result = await p_log.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "hello", "payload": {}, "user_id": "alice"}
    )
    print("composer.log: messages emitted")

    # --- no_op ---
    p_noop = (
        Pipeline()
        .composer
        .no_op()
        .done()
    )
    p_noop.state_type = ComposerBasicState
    result = await p_noop.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "", "payload": {}, "user_id": ""}
    )
    print("composer.no_op: state unchanged")

    # --- terminate ---
    p_terminate = (
        Pipeline()
        .composer
        .terminate()
        .done()
    )
    p_terminate.state_type = ComposerBasicState
    result = await p_terminate.invoke(
        {"value": "", "answer": "", "text": "", "upper_text": "",
         "user": "", "query": "", "payload": {}, "user_id": ""}
    )
    print("composer.terminate: pipeline stopped")


if __name__ == "__main__":
    asyncio.run(main())
