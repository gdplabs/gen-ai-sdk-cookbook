"""ClientManager constructed directly, for invokers that outlive any single function.

Authors:
    Delfia N. A. Putri (delfia.n.a.putri@gdplabs.id)

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
    """Build a ClientManager once, use across invocations, then close it explicitly."""
    # e.g. built once at app startup and stashed on app state
    manager = ClientManager()

    client_config = ClientConfig(lifecycle=ClientLifecycle.PERSISTENT, manager=manager)
    lm_invoker = AnthropicLMInvoker(
        AnthropicLM.CLAUDE_SONNET_4_6, client_config=client_config
    )

    try:
        # ... invoker lives on, handling requests for as long as the app runs ...
        response = await lm_invoker.invoke("What is the capital of France?")
        print(response.content)
    finally:
        # e.g. in a FastAPI lifespan shutdown block.
        await manager.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
