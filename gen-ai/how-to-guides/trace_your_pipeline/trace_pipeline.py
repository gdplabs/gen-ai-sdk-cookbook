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

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps.pipeline_step import BasePipelineStep


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


class LabelStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        prefix = "[LONG]" if state["score"] > 10 else "[short]"
        return {"label": f"{prefix} {state['uppercase_text']}"}


class FinalizeStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        return {"result": f"{state['label']} | score={state['score']}"}


pipeline = Pipeline(
    [
        UppercaseStep(name="uppercase"),
        ScoreStep(name="score"),
        LabelStep(name="label_text"),
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

    span_names = [span.name for span in exporter.get_finished_spans()]
    print(f"Captured {len(span_names)} spans")
    for name in span_names:
        print(name)


if __name__ == "__main__":
    asyncio.run(main())
