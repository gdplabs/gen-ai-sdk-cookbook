"""Runnable example for parallel pipeline processing."""

import asyncio
import time
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import parallel, step


class AnalysisState(TypedDict, total=False):
    input_document: str
    extracted_text: str
    sentiment_score: str
    detected_topics: list[str]
    named_entities: list[str]
    language_info: str
    analysis_report: dict[str, object]


class DocumentExtractor(Component):
    @main
    async def execute(self, document: str) -> str:
        return document.strip()


class SentimentAnalyzer(Component):
    @main
    async def execute(self, text: str) -> str:
        await asyncio.sleep(0.35)
        return "positive"


class TopicDetector(Component):
    @main
    async def execute(self, text: str) -> list[str]:
        await asyncio.sleep(0.30)
        return ["pipelines", "parallelism", "observability"]


class EntityExtractor(Component):
    @main
    async def execute(self, text: str) -> list[str]:
        await asyncio.sleep(0.25)
        return ["GL SDK", "LangGraph"]


class LanguageDetector(Component):
    @main
    async def execute(self, text: str) -> str:
        await asyncio.sleep(0.20)
        return "en"


class ReportGenerator(Component):
    @main
    async def execute(
        self,
        sentiment: str,
        topics: list[str],
        entities: list[str],
        language: str,
    ) -> dict[str, object]:
        return {
            "sentiment": sentiment,
            "topics": topics,
            "entities": entities,
            "language": language,
        }


def build_sequential_pipeline() -> Pipeline:
    return Pipeline(
        [
            step(DocumentExtractor(), input_map={"document": "input_document"}, output_state="extracted_text", name="extract"),
            step(SentimentAnalyzer(), input_map={"text": "extracted_text"}, output_state="sentiment_score", name="sentiment"),
            step(TopicDetector(), input_map={"text": "extracted_text"}, output_state="detected_topics", name="topics"),
            step(EntityExtractor(), input_map={"text": "extracted_text"}, output_state="named_entities", name="entities"),
            step(LanguageDetector(), input_map={"text": "extracted_text"}, output_state="language_info", name="language"),
            step(
                ReportGenerator(),
                input_map={
                    "sentiment": "sentiment_score",
                    "topics": "detected_topics",
                    "entities": "named_entities",
                    "language": "language_info",
                },
                output_state="analysis_report",
                name="report",
            ),
        ],
        state_type=AnalysisState,
    )


def build_parallel_pipeline() -> Pipeline:
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
                    "entities": step(
                        EntityExtractor(),
                        input_map={"text": "extracted_text"},
                        output_state="named_entities",
                        name="entities",
                    ),
                    "language": step(
                        LanguageDetector(),
                        input_map={"text": "extracted_text"},
                        output_state="language_info",
                        name="language",
                    ),
                },
                input_states=["extracted_text"],
                name="content_analysis_parallel",
            ),
            step(
                ReportGenerator(),
                input_map={
                    "sentiment": "sentiment_score",
                    "topics": "detected_topics",
                    "entities": "named_entities",
                    "language": "language_info",
                },
                output_state="analysis_report",
                name="report",
            ),
        ],
        state_type=AnalysisState,
    )


async def run_pipeline(name: str, pipeline: Pipeline, state: AnalysisState) -> tuple[AnalysisState, float]:
    start = time.perf_counter()
    result = await pipeline.invoke(state)
    elapsed = time.perf_counter() - start
    print(f"{name} duration: {elapsed:.2f}s")
    print(f"{name} report: {result['analysis_report']}")
    return result, elapsed


async def main() -> None:
    state: AnalysisState = {
        "input_document": "GL SDK pipelines can analyze one document through several independent steps.",
    }
    sequential_result, sequential_duration = await run_pipeline(
        "Sequential pipeline",
        build_sequential_pipeline(),
        state,
    )
    parallel_result, parallel_duration = await run_pipeline(
        "Parallel pipeline",
        build_parallel_pipeline(),
        state,
    )
    print(f"Equivalent report: {sequential_result['analysis_report'] == parallel_result['analysis_report']}")
    print(f"Speedup: {sequential_duration / parallel_duration:.2f}x")


if __name__ == "__main__":
    asyncio.run(main())
