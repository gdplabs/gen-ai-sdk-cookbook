"""Demonstrate Component.set_global_log_level for app-wide IO-event suppression.

This example follows the *Set a Global Log Level for All Components* section of
the GitBook tutorial: one classmethod call sets the default log level for every
existing and future Component, while a per-instance `log_level` assignment still
wins for the single component it is applied to.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component#set-a-global-log-level-for-all-components
"""

import asyncio
import logging

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
    """Show global log level precedence over per-instance overrides."""
    # An instance constructed before any global call uses the default DEBUG.
    existing = TextFormatter()

    # One call sets the default for ALL existing and future components.
    Component.set_global_log_level(logging.WARNING)
    # Newly constructed components inherit the global setting.
    new = TextFormatter()

    print(f"Global level set to WARNING ({logging.WARNING})")
    print(f"  pre-existing instance log_level: {existing.log_level} (inherits global)")
    print(f"  new instance log_level:          {new.log_level} (inherits global)")

    # A per-instance override still wins for that one component.
    existing.log_level = logging.DEBUG
    print("After per-instance override on pre-existing instance:")
    print(f"  pre-existing instance log_level: {existing.log_level} (override wins)")
    print(f"  new instance log_level:          {new.log_level} (still global)")

    # A new global call resets prior per-instance overrides back to the new level.
    Component.set_global_log_level(logging.ERROR)
    print(f"After a new global call to ERROR ({logging.ERROR}):")
    print(f"  pre-existing instance log_level: {existing.log_level} (reset to global)")
    print(f"  new instance log_level:          {new.log_level} (reset to global)")

    # Invalid levels are rejected with ValueError.
    try:
        Component.set_global_log_level("WARNING")  # type: ignore[arg-type]
        raise AssertionError("expected ValueError for invalid level")
    except ValueError as exc:
        print(f"Invalid level raised ValueError: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
