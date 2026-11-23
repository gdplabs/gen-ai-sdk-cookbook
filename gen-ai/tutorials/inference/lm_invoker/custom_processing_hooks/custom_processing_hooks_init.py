import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker


def capture_output_item(item, output):
    # item: raw OpenAI response output item
    # output: aggregated LMOutput object
    _ = (item, output)


async def observe_stream(event, streamer):
    # event: raw OpenAI stream event
    # streamer: output transformer chain used by LM invoker
    _ = (event, streamer)


async def main() -> None:
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-5-nano",
        output_hooks=[capture_output_item],
        streaming_hooks=[observe_stream],
    )
    print(f"Initialized LM invoker with hooks: {lm_invoker}")


if __name__ == "__main__":
    asyncio.run(main())
