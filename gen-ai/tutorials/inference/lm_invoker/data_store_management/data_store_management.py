import asyncio

from gllm_inference.lm_invoker import GoogleLMInvoker
from gllm_inference.schema import NativeTool


async def main() -> None:
    lm_invoker = GoogleLMInvoker("gemini-3.1-flash-lite-preview")

    store = await lm_invoker.data_store.create()

    # Option 1: as dictionary
    data_store_tool = {"type": "data_store", "data_stores": [store]}
    # Option 2: as native tool object
    data_store_tool = NativeTool.data_store(data_stores=[store])

    lm_invoker.set_tools([data_store_tool])


if __name__ == "__main__":
    asyncio.run(main())
