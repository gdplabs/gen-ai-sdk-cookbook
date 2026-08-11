"""ClientManager used as an async context manager for several persistent invokers.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/client-lifecycle-management#with-clientmanager
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.client_management import ClientManager
from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.model import AnthropicLM
from gllm_inference.schema import ClientConfig, ClientLifecycle

load_dotenv()


async def main() -> None:
    """Run several persistent invokers under one ClientManager scope."""
    async with ClientManager() as manager:
        client_config = ClientConfig(
            lifecycle=ClientLifecycle.PERSISTENT, manager=manager
        )
        lm_invoker = AnthropicLMInvoker(
            AnthropicLM.CLAUDE_SONNET_4_6, client_config=client_config
        )

        response = await lm_invoker.invoke("What is the capital of France?")
        print(response.content)

    # manager.__aexit__() closes every client it tracks here.


if __name__ == "__main__":
    asyncio.run(main())
