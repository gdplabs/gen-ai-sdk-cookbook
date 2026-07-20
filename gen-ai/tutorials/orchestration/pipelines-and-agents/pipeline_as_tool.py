"""Pipeline-as-a-Tool: convert a deterministic Pipeline into a callable Tool.

This pattern lets an AI Agent invoke a complex workflow (like a RAG search) as
a single atomic action. Every Component and Pipeline in the SDK has an .as_tool()
method.

Note: This script demonstrates the Pipeline.as_tool() API without requiring
gllm-aip (the Agent package). The resulting Tool object has input/output schemas
that an Agent would use to decide when to call it.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipelines-and-agents#pipeline-as-a-tool
"""

import asyncio
from typing import TypedDict

from pydantic import BaseModel, Field

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class QueryInput(BaseModel):
    """Input schema for the RAG tool."""
    question: str = Field(..., description="The user's question")


class QueryOutput(BaseModel):
    """Output schema for the RAG tool."""
    answer: str = Field(..., description="The generated answer")


class RagState(TypedDict):
    question: str
    answer: str


def generate_answer(data: dict) -> str:
    """Simulate answer generation."""
    return f"Answer to: {data['question']}"


async def main() -> None:
    """Build a deterministic RAG pipeline and convert it to a Tool."""

    # 1. Define a deterministic RAG Pipeline
    rag_pipeline = Pipeline(
        steps=[
            transform(generate_answer, input_map=["question"], output_state="answer"),
        ],
        state_type=RagState,
        input_type=QueryInput,
        output_type=QueryOutput,
        name="rag_pipeline",
    )

    # 2. Convert the Pipeline into a Tool
    rag_tool = rag_pipeline.as_tool(
        description=(
        "Retrieves relevant context and generates answers"
        " for factual queries."
    ),
    )

    # 3. Show the Tool's schemas (an Agent would use these to decide when to call it)
    print(f"Tool name: {rag_tool.name}")
    print(f"Tool description: {rag_tool.description}")
    print(f"Tool input schema: {rag_tool.input_schema}")
    print(f"Tool output schema: {rag_tool.output_schema}")

    # 4. The Pipeline still works as a pipeline
    result = await rag_pipeline.invoke({"question": "What is LangGraph?", "answer": ""})
    print(f"\nPipeline result: {result['answer']}")


if __name__ == "__main__":
    asyncio.run(main())
