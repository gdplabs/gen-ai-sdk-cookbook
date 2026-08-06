import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    thinking=True,
    output_transformers=[OutputTransformerConfig.event_filter(["thinking"])],
)

async def main() -> None:
    try:
        query = """Solve the equation 2x + 4 = 10."""
        event_emitter = EventEmitter.with_print_handler()
        output = await lm_invoker.invoke(query, event_emitter=event_emitter)
        print(output)
    finally:
        await lm_invoker.release_resources()


asyncio.run(main())
