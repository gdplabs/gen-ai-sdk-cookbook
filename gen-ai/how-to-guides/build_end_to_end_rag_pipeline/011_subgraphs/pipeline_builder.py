"""Runnable example for modular pipelines built with subgraphs."""

import asyncio
from typing import TypedDict

from gllm_core.logging import LoggerManager
from gllm_core.schema import Component, main
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step, subgraph


class MainRAGState(TypedDict, total=False):
    user_query: str
    processed_query: str
    expanded_query: str
    retrieved_documents: list[str]
    filtered_documents: list[str]
    reranked_documents: list[str]
    selected_documents: list[str]
    context: str
    prompt: str
    generated_response: str
    formatted_response: str
    validated_response: str
    response_metadata: dict[str, object]


class QueryProcessingState(TypedDict, total=False):
    user_query: str
    processed_query: str
    expanded_query: str


class RetrievalState(TypedDict, total=False):
    query: str
    retrieved_documents: list[str]
    filtered_documents: list[str]
    reranked_documents: list[str]
    selected_documents: list[str]
    context: str


class GenerationState(TypedDict, total=False):
    query: str
    context: str
    prompt: str
    generated_response: str
    formatted_response: str
    validated_response: str
    response_metadata: dict[str, object]


class QueryProcessor(Component):
    @main
    async def execute(self, query: str) -> str:
        return query.strip().lower()


class QueryExpander(Component):
    @main
    async def execute(self, query: str) -> str:
        return f"{query} | focus: nocturnal forest creatures"


class DocumentRetriever(Component):
    @main
    async def execute(self, query: str) -> list[str]:
        del query
        return [
            "Luminafox lives in moonlit forests and is active at night.",
            "Dusk Panther patrols twilight woods and stalks prey after sunset.",
            "Bramble Owl watches the canopy and hunts in low light.",
            "Glowhopper glimmers in wetland grass and leaves a faint trail of light.",
        ]


class DocumentFilter(Component):
    @main
    async def execute(self, documents: list[str]) -> list[str]:
        return [document for document in documents if "night" in document or "light" in document or "sunset" in document]


class RelevanceReranker(Component):
    @main
    async def execute(self, documents: list[str], query: str) -> list[str]:
        del query
        return sorted(documents, key=len, reverse=True)


class TopKSelector(Component):
    @main
    async def execute(self, documents: list[str]) -> list[str]:
        return documents[:3]


class ContextBuilder(Component):
    @main
    async def execute(self, documents: list[str]) -> str:
        return " ".join(documents)


class PromptBuilder(Component):
    @main
    async def execute(self, query: str, context: str) -> str:
        return f"Question: {query}\nContext: {context}"


class LLMGenerator(Component):
    @main
    async def execute(self, prompt: str) -> str:
        del prompt
        return "Luminafox, Dusk Panther, and Bramble Owl are highlighted as nocturnal creatures."


class ResponseFormatter(Component):
    @main
    async def execute(self, response: str) -> str:
        return f"Answer: {response}"


class ResponseValidator(Component):
    @main
    async def execute(self, response: str) -> str:
        if response.startswith("Answer:"):
            return response
        return "Answer: Sorry, I do not have enough information."


class MetadataExtractor(Component):
    @main
    async def execute(self, response: str, context: str) -> dict[str, object]:
        return {
            "response_length": len(response),
            "source_count": 3,
            "context_preview": context[:60],
        }


def quiet_gllm_logging() -> None:
    logger_manager = LoggerManager()
    for name in [
        "QueryProcessor",
        "QueryExpander",
        "DocumentRetriever",
        "DocumentFilter",
        "RelevanceReranker",
        "TopKSelector",
        "ContextBuilder",
        "PromptBuilder",
        "LLMGenerator",
        "ResponseFormatter",
        "ResponseValidator",
        "MetadataExtractor",
    ]:
        logger_manager.get_logger(name).disabled = True


class ModularRAGPipelineBuilder:
    """Modular RAG pipeline builder using subgraphs."""

    def build(self) -> Pipeline:
        preprocessing_step = self._build_preprocessing_subgraph()
        retrieval_step = self._build_retrieval_subgraph()
        generation_step = self._build_generation_subgraph()

        return Pipeline(
            steps=[preprocessing_step, retrieval_step, generation_step],
            state_type=MainRAGState,
            recursion_limit=100,
            name="modular_rag_pipeline",
        )

    def _build_preprocessing_subgraph(self):
        preprocessing_pipeline = Pipeline(
            [
                step(QueryProcessor(), "processed_query", {"query": "user_query"}, name="process_query"),
                step(QueryExpander(), "expanded_query", {"query": "processed_query"}, name="expand_query"),
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
                step(DocumentRetriever(), "retrieved_documents", {"query": "query"}, name="retrieve_documents"),
                step(DocumentFilter(), "filtered_documents", {"documents": "retrieved_documents"}, name="filter_documents"),
                step(
                    RelevanceReranker(),
                    "reranked_documents",
                    {"documents": "filtered_documents", "query": "query"},
                    name="rerank_documents",
                ),
                step(TopKSelector(), "selected_documents", {"documents": "reranked_documents"}, name="select_documents"),
                step(ContextBuilder(), "context", {"documents": "selected_documents"}, name="build_context"),
            ],
            state_type=RetrievalState,
            name="retrieval_pipeline",
        )
        return subgraph(
            retrieval_pipeline,
            input_map={"query": "expanded_query"},
            output_state_map={
                "retrieved_documents": "retrieved_documents",
                "filtered_documents": "filtered_documents",
                "reranked_documents": "reranked_documents",
                "selected_documents": "selected_documents",
                "context": "context",
            },
            name="retrieval_step",
        )

    def _build_generation_subgraph(self):
        generation_pipeline = Pipeline(
            [
                step(PromptBuilder(), "prompt", {"query": "query", "context": "context"}, name="build_prompt"),
                step(LLMGenerator(), "generated_response", {"prompt": "prompt"}, name="generate_response"),
                step(ResponseFormatter(), "formatted_response", {"response": "generated_response"}, name="format_response"),
                step(ResponseValidator(), "validated_response", {"response": "formatted_response"}, name="validate_response"),
                step(
                    MetadataExtractor(),
                    "response_metadata",
                    {"response": "validated_response", "context": "context"},
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
                "prompt": "prompt",
                "generated_response": "generated_response",
                "formatted_response": "formatted_response",
                "validated_response": "validated_response",
                "response_metadata": "response_metadata",
            },
            name="generation_step",
        )


async def main() -> None:
    quiet_gllm_logging()

    pipeline = ModularRAGPipelineBuilder().build()
    result = await pipeline.invoke({"user_query": "What are some forest animals?"})
    print(f"Processed query: {result['processed_query']}")
    print(f"Expanded query: {result['expanded_query']}")
    print(f"Selected documents: {result['selected_documents']}")
    print(f"Validated response: {result['validated_response']}")
    print(f"Metadata: {result['response_metadata']}")


if __name__ == "__main__":
    asyncio.run(main())
