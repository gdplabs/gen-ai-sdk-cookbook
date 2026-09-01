"""Use the shared gllm-core tracer directly.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/observability#the-shared-tracer
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

exporter = InMemorySpanExporter()
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)

from gllm_core.observability import SpanAttribute, get_tracer

tracer = get_tracer()
with tracer.start_as_current_span("my-span") as span:
    span.set_attribute(SpanAttribute.COMPONENT_NAME, "MyComponent")

provider.force_flush()
for finished in exporter.get_finished_spans():
    print(finished.name, dict(finished.attributes))
