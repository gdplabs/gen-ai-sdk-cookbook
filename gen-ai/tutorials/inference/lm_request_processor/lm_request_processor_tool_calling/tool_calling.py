import asyncio

from dotenv import load_dotenv
from gllm_core.schema import tool
from gllm_inference.builder import build_lm_request_processor


load_dotenv()


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


lmrp = build_lm_request_processor(
    model_id="openai/gpt-4.1-mini",
    system_template="You are a helpful assistant. Use tools for performing math operations.",
    user_template="{question}",
    config={"tools": [add, subtract, multiply]},
)


async def main():
    response = await lmrp.process(question="What is 10 + 20 * 0 - 4?") 
    print(f"Response:\n{response}")


if __name__ == "__main__":
    asyncio.run(main())
