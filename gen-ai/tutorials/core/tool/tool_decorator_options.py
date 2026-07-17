"""The @tool decorator: name, title, and description resolution.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/tool#the-tool-decorator
"""

import asyncio

from gllm_core.schema import tool


@tool(name="weather", title="Weather Tool")
async def fetch_weather(location: str, units: str = "metric") -> dict:
    """Get weather information for a location.

    Arguments:
        location: City name or query string (e.g. `"Jakarta"`).
        units: Unit system, such as `"metric"` or `"imperial"`.
    """
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
    # Name resolution: explicitly passed name is used
    print(f"Tool name: {fetch_weather.name}")
    print(f"Tool title: {fetch_weather.title}")

    # Without explicit name, the function __name__ is used
    print(f"Tool name: {add.name}")

    # input_schema derived from type hints + docstring
    print(f"input_schema: {add.input_schema}")
    print(f"output_schema: {add.output_schema}")


if __name__ == "__main__":
    asyncio.run(main())
