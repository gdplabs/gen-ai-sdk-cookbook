"""Shared Echo component used across step tutorial scripts.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps
"""

from typing import Any

from gllm_core.schema import main
from gllm_core.schema.component import Component


class Echo(Component):
    """A component that returns the value of 'x' unchanged."""

    @main
    async def echo_main(self, x: Any, **kwargs: Any) -> Any:
        """Return the input 'x' unchanged.

        Args:
            x (Any): Any input to be passed into the function.
            **kwargs (Any): Additional keyword arguments are accepted but
                ignored, so Echo can be used as a bare Component expression
                in ``if_else`` / ``guard`` conditions instead of only steps.

        Returns:
            Any: The same value provided via 'x'.
        """
        return x
