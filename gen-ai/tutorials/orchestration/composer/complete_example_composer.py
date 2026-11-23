"""Composer complete example: a small RAG pipeline built with the fluent API.

Note: In gllm-pipeline 0.5.18, .when()/.then()/.otherwise() branches must be
step objects (not Pipeline objects) to avoid 'Pipeline' object has no attribute
'is_excluded' during graph compilation. The GitBook example nests a full
Pipeline as the .then() branch; this cookbook uses steps instead.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#complete-example
"""

import asyncio
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import guard, log, step


class Retriever(Component):
    """Simulates document retrieval."""

    @main
    async def retrieve(self, query: str) -> dict:
        return {"documents": ["doc1", "doc2"]}


class Generator(Component):
    """Simulates response generation."""

    @main
    async def generate(self, input: dict) -> str:
        return "Generated response"


class Validator(Component):
    """Simulates response validation."""

    @main
    async def validate(self, response: str) -> bool:
        return response.startswith("Generated")


def format_context(data: dict) -> str:
    """Join retrieved documents into a single context string."""
    return " ".join(data["retrieval_result"]["documents"])


class RagState(TypedDict):
    query: str
    validate_response: bool
    retrieval_result: dict
    context: str
    generation_input: dict
    response: str
    is_valid: bool
    auth_result: str


async def main() -> None:
    """Build and run a RAG pipeline with retrieval, generation, and validation.

    The validation stage is a step object (not a nested Pipeline) so it is
    safe to use as a .then() branch under the current library constraint.
    """
    validation_step = step(
        component=Validator(),
        input_map={"response": "response"},
        output_state="is_valid",
    )
    validation_branch = guard(
        condition=lambda s: s["is_valid"],
        success_branch=log("Response validated successfully", is_template=False),
        failure_branch=log("Response validation failed", is_template=False),
        output_state="auth_result",
    )

    pipeline = (
        Pipeline()
        .composer
        .log("Starting RAG pipeline for query: {query}")
        .step(
            component=Retriever(),
            input_map={"query": "query"},
            output_state="retrieval_result",
        )
        .transform(
            operation=format_context,
            input_map=["retrieval_result"],
            output_state="context",
        )
        .bundle(input_states=["query", "context"], output_state="generation_input")
        .step(
            component=Generator(),
            input_map={"input": "generation_input"},
            output_state="response",
        )
        .when(lambda s: s.get("validate_response", True))
        .then([validation_step, validation_branch])
        .otherwise(log("Validation skipped", is_template=False))
        .end()
        .log("RAG pipeline completed. Response: {response}")
        .done()
    )
    pipeline.state_type = RagState

    result = await pipeline.invoke(
        {
            "query": "What is machine learning?",
            "validate_response": True,
            "retrieval_result": {},
            "context": "",
            "generation_input": {},
            "response": "",
            "is_valid": False,
            "auth_result": "",
        }
    )
    print(result["response"])


if __name__ == "__main__":
    asyncio.run(main())
