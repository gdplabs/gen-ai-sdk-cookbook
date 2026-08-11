"""Externally provided http_client: the caller builds and closes the transport.

Authors:
    Delfia N. A. Putri (delfia.n.a.putri@gdplabs.id)

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/client-lifecycle-management#externally-provided-client
"""

import asyncio

import httpx
from dotenv import load_dotenv
from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.model import AnthropicLM
from gllm_inference.schema import ClientConfig, ClientLifecycle

load_dotenv()


async def main() -> None:
    """Invoke with a caller-owned httpx.AsyncClient, then close it explicitly."""
    http_client = httpx.AsyncClient(trust_env=False)

    lm_invoker = AnthropicLMInvoker(
        AnthropicLM.CLAUDE_SONNET_4_6,
        client_config=ClientConfig(
            lifecycle=ClientLifecycle.PERSISTENT, http_client=http_client
        ),
    )

    try:
        response = await lm_invoker.invoke("What is the capital of France?")
        print(response.content)
    finally:
        # You built http_client, so you close it — release_resources() on the invoker
        # clears its reference but never calls .close() on your transport.
        await http_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
