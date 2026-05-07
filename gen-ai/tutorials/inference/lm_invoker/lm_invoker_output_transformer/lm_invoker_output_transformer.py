import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

load_dotenv()


async def json_transformer_example():
    lm_invoker = OpenAILMInvoker(
        OpenAILM.GPT_5_NANO,
        output_transformers=[OutputTransformerConfig.json()],
    )

    query = "Return a JSON object with keys 'name' and 'age' for a person named John who is 30 years old!"
    output = await lm_invoker.invoke(query)
    print("=== JSON Output Transformer ===")
    print(output)


if __name__ == "__main__":
    asyncio.run(json_transformer_example())
