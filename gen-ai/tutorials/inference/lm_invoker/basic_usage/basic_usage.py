import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM


async def main() -> None:
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    try:
        output = await lm_invoker.invoke("What is the capital city of Indonesia?")
        print(f"output: {output.text}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
