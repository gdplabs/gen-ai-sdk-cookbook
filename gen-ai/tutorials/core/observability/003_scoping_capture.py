"""Scope content capture to a code block with capture_content.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/observability#scoping-capture-to-a-code-block
"""

import asyncio

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

exporter = InMemorySpanExporter()
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)

from gllm_core.observability import ComponentIOCaptureConfig, capture_content
from gllm_core.schema import Component, main

class Greeter(Component):
    @main
    async def greet(self, name: str) -> str:
        return f"Hello, {name}!"

async def main_() -> None:
    greeter = Greeter()
    input_key = "gllm.component.input"

    # Process-wide capture is off, so the span carries only the component name.
    await greeter.run(name="outside-scope")
    provider.force_flush()
    outside_span = list(exporter.get_finished_spans())[-1]
    outside_captured = input_key in (outside_span.attributes or {})
    print("outside scope, input captured:", outside_captured)

    # Scoped override: capture applies for the duration of the block only.
    scoped_config = ComponentIOCaptureConfig(capture_input=True)
    with capture_content(component_io_capture=scoped_config):
        await greeter.run(name="inside-scope")
    # Capture policy is restored here.

    provider.force_flush()
    inside_span = list(exporter.get_finished_spans())[-1]
    inside_captured = input_key in (inside_span.attributes or {})
    print("inside scope, input captured:", inside_captured)
    print(inside_span.name, dict(inside_span.attributes))

asyncio.run(main_())
