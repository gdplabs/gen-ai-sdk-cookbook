import asyncio
from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.model import AnthropicLM
from gllm_inference.input_transformer import InputTransformerConfig

lm_invoker = AnthropicLMInvoker(
    AnthropicLM.CLAUDE_SONNET_4_6,
    input_transformers=[InputTransformerConfig.filter_empty()],
)


async def main() -> None:
    try:
        query = """Name an animal whose name starts with the letter A!"""
        output = await lm_invoker.invoke([query, " ", ""])  # The empty strings will be filtered out!
        print(output)
    finally:
        await lm_invoker.release_resources()


asyncio.run(main())
