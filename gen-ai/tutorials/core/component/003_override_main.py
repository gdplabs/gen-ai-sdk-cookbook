"""Overriding @main in subclasses and adjusting component log level.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component#example-overriding-main-in-subclasses
"""

import asyncio
import logging
from abc import ABC, abstractmethod

from gllm_core.schema import Component, main


class BaseProcessor(Component, ABC):
    """Abstract processor with a defined entrypoint."""

    @main
    @abstractmethod
    async def process(self, data: str) -> str:
        """Process data - must be implemented by subclasses."""
        pass


class AdvancedProcessor(BaseProcessor):
    """Processor with additional parameters."""

    async def process(self, data: str) -> str:
        # Implements the abstract method
        return self._transform(data)

    @main
    async def transform(self, data: str, mode: str = "upper") -> str:
        """Transform with configurable mode."""
        if mode == "upper":
            return data.upper()
        elif mode == "lower":
            return data.lower()
        else:
            return data

    def _transform(self, data: str) -> str:
        return data.upper()


async def main():
    # The subclass uses its own @main method (transform), not process
    processor = AdvancedProcessor()
    result = await processor.run(data="hello", mode="lower")
    assert result == "hello"
    print(result)

    # input_params reflects the new signature
    ParamsModel = processor.input_params
    assert "mode" in ParamsModel.model_fields
    print(f"input_params fields: {list(ParamsModel.model_fields.keys())}")

    # Adjust log level for lower-overhead runs
    formatter = AdvancedProcessor()
    formatter.log_level = logging.INFO
    print(f"Log level set to: {logging.getLevelName(formatter.log_level)}")


if __name__ == "__main__":
    asyncio.run(main())
