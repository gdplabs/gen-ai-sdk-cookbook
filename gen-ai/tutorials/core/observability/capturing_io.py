"""Capture a component's input and output onto its span.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/observability#capturing-component-input-and-output
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

from gllm_core.observability import ComponentIOCaptureConfig, configure_component_io_capture
from gllm_core.schema import Component, main

# Process-wide, off by default. Records real input/output — enable only where that is safe.
configure_component_io_capture(ComponentIOCaptureConfig(capture_input=True, capture_output=True))


class Greeter(Component):
    @main
    async def greet(self, name: str) -> str:
        return f"Hello, {name}!"


async def main_() -> None:
    await Greeter().run(name="world")
    provider.force_flush()

    for span in exporter.get_finished_spans():
        print(span.name, dict(span.attributes))


asyncio.run(main_())
