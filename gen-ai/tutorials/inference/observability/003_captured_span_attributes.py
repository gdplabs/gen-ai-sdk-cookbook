"""Inspect the content attributes captured onto an LM invocation span.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/observability#captured-span-attributes
"""

import asyncio

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.observability import (
    LMTraceContentConfig,
    configure_lm_trace_content,
)

exporter = InMemorySpanExporter()
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)

configure_lm_trace_content(
    LMTraceContentConfig(
        system_instructions=True,
        input_text=True,
        output_text=True,
        output_thinking=True,
    )
)


async def main() -> None:
    """Invoke an LM and print each finished span's captured content attributes."""
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    try:
        await lm_invoker.invoke("What is the capital of France?")
        provider.force_flush()

        for span in exporter.get_finished_spans():
            print(span.name, dict(span.attributes))
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
