"""Backwards compatibility with legacy _run Components.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component#backwards-compatibility-with-legacy-run-components
"""

import asyncio

from gllm_core.schema import Component


class LegacyComponent(Component):
    async def _run(self, message: str, priority: int = 1) -> str:
        """Legacy component using _run."""
        return f"[P{priority}] {message}"


async def main():
    legacy = LegacyComponent()
    result = await legacy.run(message="hello", priority=2)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
