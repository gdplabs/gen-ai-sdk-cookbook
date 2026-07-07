import asyncio

from gllm_core.schema import tool
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor


@tool
def get_weather(city: str) -> str:
    """Get the weather of a city."""
    return f"The weather of {city} is sunny."


async def main() -> None:
    prompt_builder = PromptBuilder(user_template="What is the weather in Jakarta?")
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[get_weather])
    try:
        lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)

        output = await lm_request_processor.process()
        print(f"Response: {output.text}")

        # Disable automatic tool execution to inspect the raw tool calls instead.
        output = await lm_request_processor.process(auto_execute_tools=False)
        print(f"Response: {output.tool_calls}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
