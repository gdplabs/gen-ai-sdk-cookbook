import os
import asyncio
from gllm_inference.lm_invoker import OpenAIChatCompletionsLMInvoker
from gllm_inference.output_transformer import OutputTransformerConfig

lm_invoker = OpenAIChatCompletionsLMInvoker(
    model_name="deepseek-ai/DeepSeek-R1",
    base_url="https://api.deepinfra.com/v1",
    api_key=os.getenv("DEEPINFRA_API_KEY"),
    output_transformers=[OutputTransformerConfig.think_tag()],
    output_analytics=True,
)


async def main() -> None:
    try:
        query = """Solve this equation: 2x + 3 = 11"""
        output = await lm_invoker.invoke(query)
        print(output)
    finally:
        await lm_invoker.release_resources()


asyncio.run(main())
