import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Message

load_dotenv()


messages = [
    Message.system("Talk like a pirate"),
    Message.user("What is France's capital?"),
]


async def main():
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    response = await lm_invoker.invoke(messages)
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
