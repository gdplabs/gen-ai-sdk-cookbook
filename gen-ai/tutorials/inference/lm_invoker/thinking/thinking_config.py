"""Configure thinking with boolean, object, and dictionary input forms.

GitBook: tutorials/inference/lm-invoker/thinking.md#configuring-thinking
"""

import asyncio

from gllm_inference.schema import ThinkingConfig


async def main() -> None:
    """Construct the supported thinking configuration forms."""
    # Option 1: as a boolean
    thinking = True

    # Option 2: as a ThinkingConfig object
    thinking = ThinkingConfig(enabled=True, effort="high")

    # Option 3: as a serialized ThinkingConfig dictionary
    thinking = {"enabled": True, "effort": "high"}
    print(thinking)


if __name__ == "__main__":
    asyncio.run(main())
