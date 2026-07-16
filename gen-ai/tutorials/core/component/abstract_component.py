"""Using @main with abstract base classes.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component#using-main-with-abstract-classes
"""

import asyncio
from abc import ABC, abstractmethod

from gllm_core.schema import Component, main


class BaseProcessor(Component, ABC):
    """Abstract processor with a defined entrypoint."""

    @main
    @abstractmethod
    async def process(self, data: str) -> str:
        """Process data - must be implemented by subclasses."""
        pass


class UpperCaseProcessor(BaseProcessor):
    """Converts text to uppercase."""

    async def process(self, data: str) -> str:
        return data.upper()


class LowerCaseProcessor(BaseProcessor):
    """Converts text to lowercase."""

    async def process(self, data: str) -> str:
        return data.lower()


async def main():
    upper = UpperCaseProcessor()
    lower = LowerCaseProcessor()

    # Both inherit @main from BaseProcessor.process
    result1 = await upper.run(data="hello")
    assert result1 == "HELLO"
    print(result1)

    result2 = await lower.run(data="WORLD")
    assert result2 == "world"
    print(result2)

    # Shared input schema — both have the same parameter structure
    assert (
        upper.input_params.model_fields.keys()
        == lower.input_params.model_fields.keys()
    )
    print("Shared input schema confirmed")


if __name__ == "__main__":
    asyncio.run(main())
