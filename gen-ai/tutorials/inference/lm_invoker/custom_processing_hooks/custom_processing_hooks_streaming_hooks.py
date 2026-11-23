import asyncio

from gllm_core.event import EventEmitter
from gllm_inference.lm_invoker import OpenAILMInvoker


async def log_stream_event(event, streamer):
    if event.type.endswith("delta"):
        print(f"stream event: {event.type}")


async def main() -> None:
    event_emitter = EventEmitter.with_print_handler()
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-5-nano",
        streaming_hooks=[log_stream_event],
    )
    output = await lm_invoker.invoke(
        "Write a short poem about the sea.",
        event_emitter=event_emitter,
    )
    print(output.text)


if __name__ == "__main__":
    asyncio.run(main())
