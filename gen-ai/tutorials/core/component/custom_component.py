"""A quickstart example for defining and executing a custom Component.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component
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

    result = await formatter.run(text="hello", uppercase=True, repeat=2)
    assert result == "HELLOHELLO"
    print(result)


if __name__ == "__main__":
    asyncio.run(main())