"""Runnable example for streaming LM output."""

import asyncio
import logging

from dotenv import load_dotenv

from gllm_core.event.handler import StreamEventHandler, PrintEventHandler

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor


load_dotenv()


async def main() -> None:
    logging.disable(logging.CRITICAL)

    stream_handler = StreamEventHandler()
    print_handler = PrintEventHandler()

    lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini")

    prompt_builder = PromptBuilder(
        system_template="You are a helpful assistant.",
        user_template="{query}",
    )

    processor = LMRequestProcessor(prompt_builder, lm_invoker)

    result = await processor.process(
        query="What is the capital of France?",
        event_emitter=stream_handler,
    )

    print("Final text:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())