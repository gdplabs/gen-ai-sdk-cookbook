"""Quickstart: define and execute a Component using @main.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component#quickstart
"""

import asyncio

from gllm_core.schema import Component, main


class TextFormatter(Component):
    @main
    async def format(self, text: str, uppercase: bool = False, repeat: int = 1) -> str:
        """Format text with options."""
        result = text.upper() if uppercase else text
        return result * repeat


async def main():
    formatter = TextFormatter()

    # Execute the component uniformly via run(**kwargs)
    result = await formatter.run(text="hello", uppercase=True, repeat=2)
    assert result == "HELLOHELLO"
    print(result)

    # Use the generated input schema (Pydantic model)
    ParamsModel = formatter.input_params  # type: ignore[attr-defined]
    params = ParamsModel(text="world", repeat=2)
    result2 = await formatter.run(**params.model_dump())
    print(result2)


if __name__ == "__main__":
    asyncio.run(main())
