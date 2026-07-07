from typing import Any, NotRequired, TypedDict

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import parallel, step, transform
from gllm_pipeline.types import Val
from gllm_retrieval.chunk_processor import DedupeChunkProcessor


class MultiRetrieverResearchState(TypedDict):
    query: str
    merged_top_k: int
    web_chunks: NotRequired[list[Chunk]]
    vector_chunks: NotRequired[list[Chunk]]
    chunks: NotRequired[list[Chunk]]
    response: NotRequired[str]


def tag_chunks(chunks: list[Chunk], source_type: str) -> list[Chunk]:
    return [
        chunk.model_copy(update={"metadata": {**chunk.metadata, "source_type": source_type}}, deep=True)
        for chunk in chunks
    ]


def combine_retrieved_chunks(state: dict[str, Any]) -> list[Chunk]:
    web_chunks = tag_chunks(state.get("web_chunks", []), "web")
    vector_chunks = tag_chunks(state.get("vector_chunks", []), "vector")
    return [*web_chunks, *vector_chunks]


def limit_chunks(state: dict[str, Any]) -> list[Chunk]:
    return state["chunks"][: state["merged_top_k"]]


def build_pipeline(
    web_retriever: SmartSearchWebRetriever,
    vector_retriever: VectorRetriever,
    response_synthesizer: ResponseSynthesizer,
) -> Pipeline:
    return Pipeline(
        steps=[
            parallel(
                branches={
                    "web": step(
                        component=web_retriever,
                        input_map={"query": "query", "top_k": Val(5)},
                        output_state="web_chunks",
                        name="web_retriever",
                    ),
                    "vector": step(
                        component=vector_retriever,
                        input_map={"query": "query", "top_k": Val(5)},
                        output_state="vector_chunks",
                        name="vector_retriever",
                    ),
                },
                input_states=["query"],
                copy_keys=[],
                name="parallel_retrieval",
            ),
            transform(
                combine_retrieved_chunks,
                input_states=["web_chunks", "vector_chunks"],
                output_state="chunks",
                name="combine_retrieved_chunks",
            ),
            step(
                component=DedupeChunkProcessor(),
                input_map={"chunks": "chunks"},
                output_state="chunks",
                name="dedupe_chunks",
            ),
            transform(
                limit_chunks,
                input_states=["chunks", "merged_top_k"],
                output_state="chunks",
                name="limit_chunks",
            ),
            step(
                component=response_synthesizer,
                input_map={"query": "query", "chunks": "chunks"},
                output_state="response",
                name="response_synthesizer",
            ),
        ],
        state_type=MultiRetrieverResearchState,
    )
