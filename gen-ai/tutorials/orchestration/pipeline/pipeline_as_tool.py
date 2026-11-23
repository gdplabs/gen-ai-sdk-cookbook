"""Convert a Pipeline to a Tool using input/output schemas.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#converting-to-a-tool
"""

import asyncio
from typing import TypedDict

from pydantic import BaseModel, Field

from gllm_pipeline.pipeline.pipeline import Pipeline


class QueryInput(BaseModel):
    question: str = Field(..., description="The user's question")


class QueryOutput(BaseModel):
    answer: str = Field(..., description="The generated answer")


class QueryState(TypedDict):
    question: str
    answer: str


async def main() -> None:
    """Convert a Pipeline to a tool for AI Agent integration."""
    pipeline = Pipeline(
        steps=[],  # your steps here
        state_type=QueryState,
        input_type=QueryInput,
        output_type=QueryOutput,
        name="answer_question",
    )

    tool = pipeline.as_tool(description="Answers user questions using RAG")

    # Now the tool has proper input/output schemas
    print(tool.input_schema)   # Shows Pydantic schema
    print(tool.output_schema)  # Shows Pydantic schema


if __name__ == "__main__":
    asyncio.run(main())
