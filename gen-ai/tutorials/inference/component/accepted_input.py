"""LM Component: declaring accepted input.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/component#declaring-accepted-input
"""

import asyncio
from typing import Any

from dotenv import load_dotenv
from gllm_core.schema import main as component_main
from gllm_inference.component import LMComponent


class DescriberComponent(LMComponent):
    """Describe text or attachments."""

    prompt_vars = {"context"}
    default_user_template = "Describe the following: {context}"

    @component_main
    async def describe(self, content: Any) -> str:
        """Check the content, convert it, and ask the model to describe it."""
        self._check_accepted_input(content)
        lm_input = self._to_lm_input(content)
        output = await self._invoke_lm(
            context=lm_input.context, extra_contents=lm_input.extra_contents
        )
        return output.text


async def main() -> None:
    """Describe a short text with a custom component."""
    load_dotenv()
    component = DescriberComponent.from_config(model_id="openai/gpt-5-nano")
    try:
        print(await component.describe("A tiger resting in the grass."))
    finally:
        await component.lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
