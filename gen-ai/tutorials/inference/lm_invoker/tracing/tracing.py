"""LM invoker custom trace attributes example.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker#add-custom-trace-attributes
"""

import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM


async def main() -> None:
    """Invoke an LM with custom trace attributes attached to its OpenTelemetry span."""
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    try:
        output = await lm_invoker.invoke(
            "Summarize the order status.",
            trace_attributes={
                "app.request.id": "request-123",
                "app.tenant.id": "tenant-456",
                "app.workflow.retry": False,
            },
        )
        print(f"output: {output.text}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
