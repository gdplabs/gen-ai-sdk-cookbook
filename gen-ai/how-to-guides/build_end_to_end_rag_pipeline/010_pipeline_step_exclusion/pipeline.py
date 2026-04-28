"""Runnable example for pipeline step exclusion."""

import asyncio
from typing import TypedDict

from gllm_core.logging import LoggerManager
from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import if_else, parallel, step
from gllm_pipeline.steps.pipeline_step import BasePipelineStep


class ExclusionState(TypedDict, total=False):
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
        return "positive"


class TopicDetector(Component):
    @main
    async def execute(self, text: str) -> list[str]:
        return ["pipelines", "feature-flags", "debugging"]


class EntityExtractor(Component):
    @main
    async def execute(self, text: str) -> list[str]:
        return ["GL SDK", "Feature Flags"]


class LanguageDetector(Component):
    @main
    async def execute(self, text: str) -> str:
        return "en"


class ReportGenerator(Component):
    @main
    async def execute(
        self,
        sentiment: str | None = None,
        topics: list[str] | None = None,
        entities: list[str] | None = None,
        language: str | None = None,
    ) -> dict[str, object]:
        return {
            "sentiment": sentiment or "skipped",
            "topics": topics or [],
            "entities": entities or [],
            "language": language or "skipped",
        }


class ReportGeneratorStep(BasePipelineStep):
    async def execute(self, state, runtime=None, config=None):
        del runtime, config
        generator = ReportGenerator()
        report = await generator.execute(
            sentiment=state.get("sentiment_score"),
            topics=state.get("detected_topics"),
            entities=state.get("named_entities"),
            language=state.get("language_info"),
        )
        return {"analysis_report": report}


def quiet_gllm_logging() -> None:
    logger_manager = LoggerManager()
    for name in [
        "DocumentExtractor",
        "SentimentAnalyzer",
        "TopicDetector",
        "EntityExtractor",
        "LanguageDetector",
        "ReportGenerator",
        "report",
    ]:
        logger_manager.get_logger(name).disabled = True


def create_basic_pipeline() -> Pipeline:
    return Pipeline(
        [
            step(DocumentExtractor(), "extracted_text", {"document": "input_document"}, name="extract"),
            step(SentimentAnalyzer(), "sentiment_score", {"text": "extracted_text"}, name="sentiment"),
            step(TopicDetector(), "detected_topics", {"text": "extracted_text"}, name="topics"),
            ReportGeneratorStep("report"),
        ],
        state_type=ExclusionState,
    )


def create_conditional_pipeline() -> Pipeline:
    return Pipeline(
        [
            step(DocumentExtractor(), "extracted_text", {"document": "input_document"}, name="extract"),
            if_else(
                condition=lambda state: len(state["extracted_text"]) > 60,
                if_branch=[
                    step(TopicDetector(), "detected_topics", {"text": "extracted_text"}, name="detailed"),
                ],
                else_branch=[
                    step(LanguageDetector(), "language_info", {"text": "extracted_text"}, name="quick"),
                ],
                name="conditional_analysis",
            ),
        ],
        state_type=ExclusionState,
    )


def create_adaptive_pipeline(include_sentiment: bool, include_entities: bool, debug_mode: bool = False) -> Pipeline:
    pipeline = Pipeline(
        [
            step(DocumentExtractor(), "extracted_text", {"document": "input_document"}, name="extract"),
            parallel(
                {
                    "sentiment": step(
                        SentimentAnalyzer(),
                        "sentiment_score",
                        {"text": "extracted_text"},
                        name="sentiment",
                    ),
                    "topics": step(
                        TopicDetector(),
                        "detected_topics",
                        {"text": "extracted_text"},
                        name="topics",
                    ),
                    "entities": step(
                        EntityExtractor(),
                        "named_entities",
                        {"text": "extracted_text"},
                        name="entities",
                    ),
                    "language": step(
                        LanguageDetector(),
                        "language_info",
                        {"text": "extracted_text"},
                        name="language",
                    ),
                },
                input_states=["extracted_text"],
                name="analysis_parallel",
            ),
            ReportGeneratorStep("report"),
        ],
        state_type=ExclusionState,
    )

    exclusions = []
    if not include_sentiment:
        exclusions.append("analysis_parallel.sentiment")
    if not include_entities:
        exclusions.append("analysis_parallel.entities")
    if debug_mode:
        exclusions.extend(["analysis_parallel.topics", "analysis_parallel.language"])
    if exclusions:
        pipeline.exclusions.exclude(*exclusions)

    return pipeline


def get_current_exclusions(pipeline: Pipeline) -> list[str]:
    exclusions = getattr(pipeline, "_exclusions", None)
    if not exclusions:
        return []
    return list(exclusions.excluded_paths)


async def show_run(title: str, pipeline: Pipeline, state: ExclusionState) -> None:
    result = await pipeline.invoke(state)
    print(title)
    print(f"Current exclusions: {get_current_exclusions(pipeline)}")
    print(f"Report: {result['analysis_report']}")


async def main() -> None:
    quiet_gllm_logging()

    state: ExclusionState = {
        "input_document": "A configurable pipeline lets teams disable expensive branches when they are not needed.",
    }

    basic_pipeline = create_basic_pipeline()
    await show_run("Full pipeline result", basic_pipeline, state)

    basic_pipeline.exclusions.exclude("sentiment")
    await show_run("Without sentiment", basic_pipeline, state)

    conditional_pipeline = create_conditional_pipeline()
    conditional_pipeline.exclusions.exclude("conditional_analysis.true")
    conditional_result = await conditional_pipeline.invoke(state)
    print("Conditional pipeline after excluding the detailed branch")
    print(f"Current exclusions: {get_current_exclusions(conditional_pipeline)}")
    print(f"Conditional result keys: {sorted(conditional_result.keys())}")

    adaptive_pipeline = create_adaptive_pipeline(
        include_sentiment=False,
        include_entities=True,
        debug_mode=True,
    )
    await show_run("Adaptive pipeline", adaptive_pipeline, state)

    lifecycle_pipeline = create_adaptive_pipeline(True, True)
    print(f"Lifecycle start: {get_current_exclusions(lifecycle_pipeline)}")
    lifecycle_pipeline.exclusions.exclude("analysis_parallel.sentiment", "analysis_parallel.topics")
    print(f"After exclude: {get_current_exclusions(lifecycle_pipeline)}")
    lifecycle_pipeline.exclusions.include("analysis_parallel.sentiment")
    print(f"After include: {get_current_exclusions(lifecycle_pipeline)}")
    print(f"Excluded steps: {lifecycle_pipeline.exclusions.list_excluded()}")
    lifecycle_pipeline.exclusions.clear()
    print(f"After clear: {get_current_exclusions(lifecycle_pipeline)}")


if __name__ == "__main__":
    asyncio.run(main())
