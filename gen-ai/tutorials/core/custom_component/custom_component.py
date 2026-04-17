"""An example of making a custom component.

Authors:
    - Kadek Denaya (kadek.d.r.diana@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/add-a-custom-component
"""

import asyncio
from typing import Any

from gllm_core.schema.component import Component


class Echo(Component):
    """A simple component that returns the provided input unchanged."""

    def identity(self, x: Any) -> Any:
        """Return the input unchanged.

        Args:
            x (Any): Input value.

        Returns:
            Any: The same input value.
        """
        return x

    async def _run(self, **kwargs: Any) -> Any:
        """Core logic that reads 'x' from kwargs and echoes it back.

        Notes:
            Accessing with subscript (kwargs["x"]) makes 'x' a required input.
            The Pipeline’s analyzer detects this and will validate it upstream.
        """
        value = kwargs["x"]
        return self.identity(value)


async def main():
    """Main function."""
    echo = Echo()
    result = await echo.run(x="hello")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
