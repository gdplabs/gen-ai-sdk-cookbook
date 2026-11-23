"""A quickstart example for defining and calling Tools with @tool.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/tool
"""

import asyncio

from gllm_core.schema import Tool, tool


@tool(description="Get weather information")
async def fetch_weather(location: str, units: str = "metric") -> dict:
    """Get weather information for a location.

    Arguments:
        location: City name or query string (e.g. `"Jakarta"`).
        units: Unit system, such as `"metric"` or `"imperial"`.
    """
    # Implementation goes here
    return {"temperature": 22.5, "conditions": "sunny"}


@tool
async def add(a: int, b: int) -> int:
    """Add two integers.

    Arguments:
        a: First addend.
        b: Second addend.
    """
    return a + b


async def main():
    assert isinstance(fetch_weather, Tool)

    result = await fetch_weather("New York", "imperial")
    print(f"Weather result: {result}")

    result2 = await fetch_weather.invoke(location="Tokyo", units="metric")
    print(f"Weather via invoke: {result2}")

    sum_result = await add.invoke(a=1, b=2)
    print(f"1 + 2 = {sum_result}")

    print(f"Tool input schema: {add.input_schema}")


if __name__ == "__main__":
    asyncio.run(main())
