"""Runnable example for pipeline step exclusion."""

import asyncio
from typing import Any, TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import parallel, step
from gllm_pipeline.steps.pipeline_step import BasePipelineStep
from langgraph.runtime import Runtime
from langgraph.types import RunnableConfig
from pydantic import BaseModel


class ExclusionState(TypedDict, total=False):
    input_document: str
    extracted_text: str
    sentiment_score: str
    detected_topics: list[str]
    language_info: str
    analysis_report: dict[str, object]


class DocumentExtractor(Component):
    @main
    async def execute(self, document: str) -> str:
        return document.strip()


class SentimentAnalyzer(Component):
    @main
    async def execute(self, text: str) -> str:
        return "positive"


class TopicDetector(Component):
    @main
    async def execute(self, text: str) -> list[str]:
        return ["pipelines", "feature-flags", "debugging"]


class LanguageDetector(Component):
    @main
    async def execute(self, text: str) -> str:
        return "en"


class ReportStep(BasePipelineStep):
    async def execute(
        self,
        state: dict[str, Any],
        runtime: Runtime[dict[str, Any] | BaseModel],
        config: RunnableConfig | None = None,
    ) -> dict[str, object]:
        return {
            "analysis_report": {
                "sentiment": state.get("sentiment_score", "skipped"),
                "topics": state.get("detected_topics", []),
                "language": state.get("language_info", "skipped"),
            }
        }


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            step(DocumentExtractor(), input_map={"document": "input_document"}, output_state="extracted_text", name="extract"),
            parallel(
                {
                    "sentiment": step(
                        SentimentAnalyzer(),
                        input_map={"text": "extracted_text"},
                        output_state="sentiment_score",
                        name="sentiment",
                    ),
                    "topics": step(
                        TopicDetector(),
                        input_map={"text": "extracted_text"},
                        output_state="detected_topics",
                        name="topics",
                    ),
                    "language": step(
                        LanguageDetector(),
                        input_map={"text": "extracted_text"},
                        output_state="language_info",
                        name="language",
                    ),
                },
                input_states=["extracted_text"],
                name="analysis_parallel",
            ),
            ReportStep("report"),
        ],
        state_type=ExclusionState,
    )


async def show_run(title: str, pipeline: Pipeline, state: ExclusionState) -> None:
    result = await pipeline.invoke(state)
    current_exclusions = list(getattr(getattr(pipeline, "_exclusions", None), "excluded_paths", []))
    print(title)
    print(f"Current exclusions: {current_exclusions}")
    print(f"Report: {result['analysis_report']}")


async def main() -> None:
    state: ExclusionState = {
        "input_document": "A configurable pipeline lets teams disable expensive branches when they are not needed.",
    }
    pipeline = build_pipeline()

    await show_run("Full pipeline", pipeline, state)

    pipeline.exclusions.exclude("analysis_parallel.topics")
    await show_run("After excluding the topics branch", pipeline, state)

    pipeline.exclusions.exclude("analysis_parallel")
    await show_run("After excluding the entire parallel block", pipeline, state)

    pipeline.exclusions.clear()
    await show_run("After clearing exclusions", pipeline, state)


if __name__ == "__main__":
    asyncio.run(main())
