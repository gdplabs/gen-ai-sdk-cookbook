"""Runnable example for extending LM capabilities with tools."""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import tool
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor


load_dotenv()


@tool
async def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
async def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b


@tool
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


async def main() -> None:
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-4o-mini",
        tools=[add, subtract, multiply],
    )

    prompt_builder = PromptBuilder(
        system_template="You are a helpful assistant.",
        user_template="{query}",
    )

    processor = LMRequestProcessor(prompt_builder, lm_invoker)

    result = await processor.process(
        query="What is 25 multiplied by 4? Use the multiply tool.",
    )

    print(f"Query: What is 25 multiplied by 4?")
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())