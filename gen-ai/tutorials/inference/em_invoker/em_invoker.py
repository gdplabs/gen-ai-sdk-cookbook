import asyncio

from dotenv import load_dotenv
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM

load_dotenv()


async def main():
    em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)
    response = await em_invoker.invoke("Hello world!")
    print(f"Vectorized text:\n{response}")


if __name__ == "__main__":
    asyncio.run(main())
