import asyncio

from dotenv import load_dotenv

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool

load_dotenv()


async def main() -> None:
    web_search_tool = NativeTool.web_search()

    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[web_search_tool])

    query = "How much did `Zootopia 2` make in the box office?"
    output = await lm_invoker.invoke(query)
    for item in output.outputs:
        print(f"=== Output item: {item.type!r} ===\n{item.output}\n")


if __name__ == "__main__":
    asyncio.run(main())
