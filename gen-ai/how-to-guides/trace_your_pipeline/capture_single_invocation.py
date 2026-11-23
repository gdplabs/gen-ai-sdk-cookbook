"""Capture component input/output for a single pipeline invocation with trace_config.

Unlike ``configure_component_io_capture`` (a process-wide policy, see ``trace_pipeline.py``),
``trace_config`` on ``pipeline.invoke`` scopes capture to that one call and restores the
previous policy afterward.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/trace-your-pipeline#capture-for-a-single-invocation
"""

import asyncio
from typing import TypedDict

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

# Configure tracing before importing gllm_pipeline.
exporter = InMemorySpanExporter()
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)

from gllm_core.observability import ComponentIOCaptureConfig
from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step


class TraceState(TypedDict, total=False):
    name: str
    greeting: str


class Greeter(Component):
    @main
    async def greet(self, name: str) -> str:
        return f"Hello, {name}!"


pipeline = Pipeline(
    [
        step(
            Greeter(),
            input_map={"name": "name"},
            output_state=["greeting"],
            name="greet",
        ),
    ],
    name="greeter_service",
    state_type=TraceState,
)


async def main() -> None:
    # This invocation opts in via trace_config -> the Greeter span carries input/output.
    await pipeline.invoke(
        {"name": "scoped"},
        thread_id="with-capture",
        trace_config={
            "component_io_capture": ComponentIOCaptureConfig(capture_input=True, capture_output=True)
        },
    )
    # This invocation uses the default (process-wide) policy -> no input/output on the span.
    await pipeline.invoke({"name": "plain"}, thread_id="without-capture")
    provider.force_flush()

    greeter_spans = [s for s in exporter.get_finished_spans() if s.name == "Greeter"]
    with_capture, without_capture = greeter_spans[0], greeter_spans[-1]

    print("with trace_config, input captured:", "gllm.component.input" in (with_capture.attributes or {}))
    print("without trace_config, input captured:", "gllm.component.input" in (without_capture.attributes or {}))


if __name__ == "__main__":
    asyncio.run(main())
