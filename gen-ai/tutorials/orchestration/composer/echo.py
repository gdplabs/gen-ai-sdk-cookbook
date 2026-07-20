"""Shared Echo component used across composer tutorial scripts.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer
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
            x (Any): Any input to be passed to the function.
            **kwargs (Any): Additional keyword arguments (e.g. event_emitter).

        Returns:
            Any: The same value provided via 'x'.
        """
        return x
