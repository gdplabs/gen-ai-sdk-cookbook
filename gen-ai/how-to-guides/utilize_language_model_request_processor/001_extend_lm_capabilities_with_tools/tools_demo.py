"""Runnable example for extending an LM request processor with tools."""

import asyncio
import logging

from gllm_core.schema import tool

from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import LMOutput, Message, ModelId, ToolCall, ToolResult


CREATURE_DATABASE = {
    "Luminafox": "Luminafox glows in the dark because its silver fur reflects ambient moonlight.",
    "Dusk Panther": "Dusk Panther relies on stealth and low-light vision rather than glowing markings.",
}


@tool
async def creature_profile(name: str) -> str:
    """Return a short profile for a named creature."""
    return CREATURE_DATABASE.get(name, f"No profile found for {name}.")


class ToolCallingDemoInvoker(BaseLMInvoker):
    async def _invoke(self, messages, config, transformer, stream) -> LMOutput:
        del config, transformer, stream
        tool_result = self._find_tool_result(messages)

        output = LMOutput()
        if tool_result is None:
            output.add_text("I need fresh creature data before I answer.")
            output.add_tool_call(
                ToolCall(
                    id="tool-call-1",
                    name="creature_profile",
                    args={"name": "Luminafox"},
                )
            )
            return output

        output.add_text(
            "Final answer: Luminafox is the glowing creature. "
            f"Tool evidence: {tool_result.output}"
        )
        return output

    def _format_messages(self, messages: list[Message]) -> list[Message]:
        return messages

    @staticmethod
    def _find_tool_result(messages: list[Message]) -> ToolResult | None:
        for message in messages:
            for content in message.contents:
                if isinstance(content, ToolResult):
                    return content
        return None


async def main() -> None:
    logging.disable(logging.CRITICAL)

    invoker = ToolCallingDemoInvoker(
        model_id=ModelId.from_string("openai/gpt-5-nano"),
        tools=[creature_profile],
    )
    processor = LMRequestProcessor(
        PromptBuilder(
            system_template="Use tools when they improve factual accuracy.",
            user_template="{query}",
        ),
        invoker,
    )

    raw_result = await processor.process(
        query="Which creature glows in the dark? Use the creature_profile tool before answering.",
        auto_execute_tools=False,
    )
    print("Initial tool request")
    print(f"Assistant text: {raw_result.text}")
    for tool_call in raw_result.tool_calls:
        print(f"Tool call: {tool_call.name}({tool_call.args})")

    final_result = await processor.process(
        query="Which creature glows in the dark? Use the creature_profile tool before answering.",
        auto_execute_tools=True,
    )
    print("Auto-executed answer")
    print(final_result.text)


if __name__ == "__main__":
    asyncio.run(main())
