"""Calling a Tool: direct call vs invoke().

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/tool#calling-a-tool
"""

import asyncio

from gllm_core.schema import tool


@tool
async def add(a: int, b: int) -> int:
    """Add two integers.

    Arguments:
        a: First addend.
        b: Second addend.
    """
    return a + b


async def main():
    # Direct call — if func is async, returns a coroutine
    result = await add(1, 2)
    print(f"Direct call: {result}")

    # Standardized invoke call — always async, works for sync and async
    result2 = await add.invoke(a=1, b=2)
    print(f"invoke() result: {result2}")

    print(f"input_schema: {add.input_schema}")
    print(f"output_schema: {add.output_schema}")


if __name__ == "__main__":
    asyncio.run(main())
