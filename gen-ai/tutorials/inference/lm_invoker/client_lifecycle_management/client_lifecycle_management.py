import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)

# ... perform invocations ...

async def cleanup():
    await lm_invoker.release_resources()

asyncio.run(cleanup())
