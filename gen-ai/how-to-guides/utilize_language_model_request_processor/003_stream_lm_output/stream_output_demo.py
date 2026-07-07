import json
import asyncio
from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.request_processor import LMRequestProcessor
from gllm_core.event import EventEmitter
from gllm_core.event.handler import StreamEventHandler
from gllm_inference.prompt_builder import PromptBuilder

load_dotenv()

async def main():
    # Setup event system for streaming
    streamer = StreamEventHandler()
    event_emitter = EventEmitter([streamer])

    # Initialize LM invoker and processor
    lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini")
    prompt_builder = PromptBuilder(
        system_template="You are a helpful assistant who specializes in recommending activities.",
        user_template="{question}"
    )
    lm_request_processor = LMRequestProcessor(
        prompt_builder=prompt_builder,
        lm_invoker=lm_invoker,
    )

    # Run the processor and stream concurrently
    # If you want real-time tokens → run processor + streamer concurrently.
    # If you only care about the final response → just await process() and parse the result
    processor_task = asyncio.create_task(
        lm_request_processor.process(
            question="I want to go to Tokyo, Japan. What should I do?",
            event_emitter=event_emitter
        )
    )

    async for event in streamer.stream():
        token = json.loads(event)
        print(token)

    await processor_task
    await event_emitter.close()

if __name__ == "__main__":
    asyncio.run(main())
