import asyncio

from dotenv import load_dotenv
from gllm_inference.builder import build_lm_invoker
from gllm_inference.model import AnthropicLM, GoogleLM, OpenAILM
from gllm_inference.schema import ModelProvider

load_dotenv()

# Easily switch between models by changing the model_id
model_id = f"{ModelProvider.ANTHROPIC}/{AnthropicLM.CLAUDE_SONNET_4}"  # Using Anthropic model
# model_id = f"{ModelProvider.GOOGLE}/{GoogleLM.GEMINI_2_5_FLASH_LITE}"  # Using Google model
# model_id = f"{ModelProvider.OPENAI}/{OpenAILM.GPT_5_NANO}"  # Using OpenAI model


async def main():
    lm_invoker = build_lm_invoker(model_id=model_id)
    response = await lm_invoker.invoke("What is France's capital?")
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
