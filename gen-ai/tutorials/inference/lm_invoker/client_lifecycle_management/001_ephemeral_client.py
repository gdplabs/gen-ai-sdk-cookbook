"""Default ephemeral client lifecycle: a fresh client is opened and closed per call.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/client-lifecycle-management#ephemeral-client
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

load_dotenv()


async def main() -> None:
    """Invoke with the default ephemeral client lifecycle."""
    # Default: ephemeral. No client is retained; nothing to clean up.
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)

    response = await lm_invoker.invoke("What is the capital of France?")
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())
