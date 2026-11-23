"""Demonstrate Component IO-event log level tuning and its runtime overhead.

This example follows the *Component lifecycle* section of the GitBook tutorial:
it shows the default DEBUG behavior first, then switches to INFO to skip
IO-event formatting and measures the latency impact on repeated calls.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component#adjust-log-level-for-lower-overhead-runs
"""

import asyncio
import logging
import time

from gllm_core.schema import Component, main


class TextFormatter(Component):
    """Simple component that formats text."""

    @main
    async def format(self, text: str, uppercase: bool = False, repeat: int = 1) -> str:
        """Format text with options."""
        result = text.upper() if uppercase else text
        return result * repeat

    async def _run(self, **kwargs: object) -> str:
        """Delegate run() to the @main entrypoint."""
        return await self.format(**kwargs)  # type: ignore[arg-type]


async def main() -> None:
    """Run the log-level example and print elapsed time for each scenario."""
    component = TextFormatter()

    # Keep default DEBUG — IO events are logged.
    start = time.perf_counter()
    for _ in range(200):
        await component.run(text="hello", uppercase=True, repeat=2)
    debug_elapsed = time.perf_counter() - start
    print(f"DEBUG run() calls completed in {debug_elapsed:.4f}s")

    # Raise to INFO — IO-event formatting is skipped.
    component.log_level = logging.INFO
    start = time.perf_counter()
    for _ in range(200):
        await component.run(text="hello", uppercase=True, repeat=2)
    info_elapsed = time.perf_counter() - start
    print(f"INFO run() calls completed in {info_elapsed:.4f}s")


if __name__ == "__main__":
    asyncio.run(main())
