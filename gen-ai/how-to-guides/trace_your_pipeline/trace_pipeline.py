"""Runnable example for tracing a pipeline with OpenTelemetry."""

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

from gllm_core.observability import ComponentIOCaptureConfig, configure_component_io_capture
from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step
from gllm_pipeline.steps.pipeline_step import BasePipelineStep

# Opt in to recording each component's input/output on its span.
# This is a process-wide policy and is off by default.
configure_component_io_capture(ComponentIOCaptureConfig(capture_input=True, capture_output=True))


class TraceState(TypedDict, total=False):
    text: str
    uppercase_text: str
    score: int
    label: str
    result: str


class UppercaseStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        return {"uppercase_text": state["text"].upper()}


class ScoreStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        return {"score": len(state["text"])}


class Labeler(Component):
    """A component-backed step. It emits its own span, named after the class,
    below the enclosing ``pipeline.step`` span."""

    @main
    async def label(self, uppercase_text: str, score: int) -> str:
        prefix = "[LONG]" if score > 10 else "[short]"
        return f"{prefix} {uppercase_text}"


class FinalizeStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        return {"result": f"{state['label']} | score={state['score']}"}


pipeline = Pipeline(
    [
        UppercaseStep(name="uppercase"),
        ScoreStep(name="score"),
        step(
            Labeler(),
            input_map={"uppercase_text": "uppercase_text", "score": "score"},
            output_state=["label"],
            name="label_text",
        ),
        FinalizeStep(name="finalize"),
    ],
    name="my_pipeline_service",
    state_type=TraceState,
)


async def main() -> None:
    short_result = await pipeline.invoke({"text": "hi"}, thread_id="trace-short")
    long_result = await pipeline.invoke({"text": "hello, world!"}, thread_id="trace-long")
    provider.force_flush()

    print(short_result["result"])
    print(long_result["result"])

    spans = exporter.get_finished_spans()
    print(f"Captured {len(spans)} spans")
    for span in spans:
        print(span.name)
        for key in ("gllm.component.name", "gllm.component.input", "gllm.component.output"):
            if key in (span.attributes or {}):
                print(f"  {key}: {span.attributes[key]}")


if __name__ == "__main__":
    asyncio.run(main())
