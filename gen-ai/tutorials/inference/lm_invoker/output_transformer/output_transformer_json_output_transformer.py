import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    output_transformers=[OutputTransformerConfig.json()],
)


async def main() -> None:
    try:
        query = """Return a JSON object with keys 'name' and 'age' for a person named John who is 30 years old!"""
        output = await lm_invoker.invoke(query)
        print(output)
    finally:
        await lm_invoker.release_resources()


asyncio.run(main())
