"""Runnable example for executing a pipeline."""

import asyncio
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step


class ExecutionState(TypedDict, total=False):
    user_query: str
    history: str
    context: str
    response: str
    references: list[str]


class RetrieveContext(Component):
    @main
    async def run(self, user_query: str, history: str, top_k: int) -> str:
        return (
            f"Retrieved {top_k} notes for '{user_query}'. "
            f"Conversation history length: {len(history)}."
        )


class GenerateResponse(Component):
    @main
    async def run(self, user_query: str, context: str) -> str:
        return f"Answer to '{user_query}' based on context: {context}"


class CollectReferences(Component):
    @main
    async def run(self, context: str) -> list[str]:
        return [
            "docs/overview.md",
            "docs/faq.md",
            f"context-summary::{context[:32]}",
        ]


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            step(
                RetrieveContext(),
                input_map={
                    "user_query": "user_query",
                    "history": "history",
                    "top_k": "top_k",
                },
                output_state="context",
                name="retrieve_context",
            ),
            step(
                GenerateResponse(),
                input_map={
                    "user_query": "user_query",
                    "context": "context",
                },
                output_state="response",
                name="generate_response",
            ),
            step(
                CollectReferences(),
                input_map={"context": "context"},
                output_state="references",
                name="collect_references",
            ),
        ],
        state_type=ExecutionState,
        name="execute_pipeline_demo",
    )


async def main() -> None:
    pipeline = build_pipeline()
    initial_state: ExecutionState = {
        "user_query": "What is machine learning?",
        "history": "User previously asked about supervised learning.",
    }

    default_result = await pipeline.invoke(initial_state, context={"top_k": 2})
    print("Basic execution")
    print(f"Response: {default_result['response']}")
    print(f"References: {default_result['references']}")

    configured_result = await pipeline.invoke(
        initial_state,
        context={"top_k": 4, "debug": True},
    )
    print("Execution with configuration")
    print(f"Response: {configured_result['response']}")
    print(f"References: {configured_result['references']}")


if __name__ == "__main__":
    asyncio.run(main())
