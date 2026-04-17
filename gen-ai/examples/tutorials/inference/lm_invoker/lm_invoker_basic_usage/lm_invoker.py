import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

load_dotenv()


async def main():
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    response = await lm_invoker.invoke("What is France's capital?")
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
