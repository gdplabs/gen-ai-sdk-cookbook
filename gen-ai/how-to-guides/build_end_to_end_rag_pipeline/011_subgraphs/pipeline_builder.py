"""Runnable example for modular pipelines built with subgraphs."""

import asyncio
from typing import TypedDict

from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step, subgraph


class MainRAGState(TypedDict, total=False):
    user_query: str
    processed_query: str
    expanded_query: str
    context: str
    final_response: str
    metadata: dict[str, object]


class QueryProcessingState(TypedDict, total=False):
    user_query: str
    processed_query: str
    expanded_query: str


class RetrievalState(TypedDict, total=False):
    query: str
    retrieved_documents: list[str]
    context: str


class GenerationState(TypedDict, total=False):
    query: str
    context: str
    final_response: str
    metadata: dict[str, object]


class QueryProcessor(Component):
    @main
    async def execute(self, query: str) -> str:
        return query.strip().lower()


class QueryExpander(Component):
    @main
    async def execute(self, query: str) -> str:
        return f"{query} | focus: forest animals"


class DocumentRetriever(Component):
    @main
    async def execute(self, query: str) -> list[str]:
        return [
            "Luminafox lives in moonlit forests and is active at night.",
            "Dusk Panther patrols twilight woods and stalks prey after sunset.",
            "Bramble Owl watches the canopy and hunts in low light.",
        ]


class ContextBuilder(Component):
    @main
    async def execute(self, documents: list[str]) -> str:
        return " ".join(documents)


class ResponseGenerator(Component):
    @main
    async def execute(self, query: str, context: str) -> str:
        return (
            "Forest animals mentioned in the retrieved context: "
            "Luminafox, Dusk Panther, and Bramble Owl."
        )


class MetadataExtractor(Component):
    @main
    async def execute(self, response: str, context: str) -> dict[str, object]:
        return {
            "response_length": len(response),
            "source_count": 3,
            "context_preview": context[:60],
        }


class ModularRAGPipelineBuilder:
    def build(self) -> Pipeline:
        return Pipeline(
            [
                self._build_preprocessing_subgraph(),
                self._build_retrieval_subgraph(),
                self._build_generation_subgraph(),
            ],
            state_type=MainRAGState,
            name="modular_rag_pipeline",
        )

    def _build_preprocessing_subgraph(self):
        preprocessing_pipeline = Pipeline(
            [
                step(QueryProcessor(), input_map={"query": "user_query"}, output_state="processed_query", name="process_query"),
                step(QueryExpander(), input_map={"query": "processed_query"}, output_state="expanded_query", name="expand_query"),
            ],
            state_type=QueryProcessingState,
            name="preprocessing_pipeline",
        )
        return subgraph(
            preprocessing_pipeline,
            input_map={"user_query": "user_query"},
            output_state_map={
                "processed_query": "processed_query",
                "expanded_query": "expanded_query",
            },
            name="preprocessing_step",
        )

    def _build_retrieval_subgraph(self):
        retrieval_pipeline = Pipeline(
            [
                step(DocumentRetriever(), input_map={"query": "query"}, output_state="retrieved_documents", name="retrieve_documents"),
                step(ContextBuilder(), input_map={"documents": "retrieved_documents"}, output_state="context", name="build_context"),
            ],
            state_type=RetrievalState,
            name="retrieval_pipeline",
        )
        return subgraph(
            retrieval_pipeline,
            input_map={"query": "expanded_query"},
            output_state_map={"context": "context"},
            name="retrieval_step",
        )

    def _build_generation_subgraph(self):
        generation_pipeline = Pipeline(
            [
                step(
                    ResponseGenerator(),
                    input_map={"query": "query", "context": "context"},
                    output_state="final_response",
                    name="generate_response",
                ),
                step(
                    MetadataExtractor(),
                    input_map={"response": "final_response", "context": "context"},
                    output_state="metadata",
                    name="extract_metadata",
                ),
            ],
            state_type=GenerationState,
            name="generation_pipeline",
        )
        return subgraph(
            generation_pipeline,
            input_map={
                "query": "processed_query",
                "context": "context",
            },
            output_state_map={
                "final_response": "final_response",
                "metadata": "metadata",
            },
            name="generation_step",
        )


async def main() -> None:
    pipeline = ModularRAGPipelineBuilder().build()
    result = await pipeline.invoke({"user_query": "What are some forest animals?"})
    print(f"Processed query: {result['processed_query']}")
    print(f"Expanded query: {result['expanded_query']}")
    print(f"Final response: {result['final_response']}")
    print(f"Metadata: {result['metadata']}")


if __name__ == "__main__":
    asyncio.run(main())
