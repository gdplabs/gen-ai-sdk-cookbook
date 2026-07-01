"""Example script to build and run a multi-retriever RAG pipeline.

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/synthesize-responses-from-multiple-retrievers
"""

import asyncio
import os
from typing import Any, NotRequired, TypedDict

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_generation.repacker import Repacker
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.request_processor import build_lm_request_processor
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import parallel, step, transform
from gllm_pipeline.types import Val
from gllm_retrieval.chunk_processor import DedupeChunkProcessor
from gllm_retrieval.retriever import SmartSearchWebRetriever, VectorRetriever

from indexer import create_internal_retriever, ingest_internal_data

load_dotenv()

SYSTEM_PROMPT = """
You are a research assistant. Use only the provided context to answer the question.
If the context is not enough, say what is missing.

Context:
{context}
"""

USER_PROMPT = "Question: {query}"


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


async def create_web_retriever() -> SmartSearchWebRetriever:
    return await SmartSearchWebRetriever.create(
        base_url=os.environ["SMART_SEARCH_BASE_URL"],
        token=os.environ["SMART_SEARCH_TOKEN"],
    )


def create_response_synthesizer() -> ResponseSynthesizer:
    lm_request_processor = build_lm_request_processor(
        model_id=os.environ["LANGUAGE_MODEL"],
        credentials=os.environ["OPENAI_API_KEY"],
        system_template=SYSTEM_PROMPT,
        user_template=USER_PROMPT,
    )
    return ResponseSynthesizer.stuff(
        lm_request_processor=lm_request_processor,
        chunks_repacker=Repacker(mode="chunk"),
    )


def build_pipeline(
    web_retriever: SmartSearchWebRetriever,
    vector_retriever: VectorRetriever,
    response_synthesizer: ResponseSynthesizer,
) -> Pipeline:
    return Pipeline(
        [
            parallel(
                branches={
                    "web": step(
                        web_retriever,
                        input_map={"query": "query", "top_k": Val(5)},
                        output_state="web_chunks",
                        name="web_retriever",
                    ),
                    "vector": step(
                        vector_retriever,
                        input_map={"query": "query", "top_k": Val(5)},
                        output_state="vector_chunks",
                        name="vector_retriever",
                    ),
                },
                input_states=["query"],
                name="parallel_retrieval",
            ),
            transform(
                combine_retrieved_chunks,
                input_states=["web_chunks", "vector_chunks"],
                output_state="chunks",
                name="combine_retrieved_chunks",
            ),
            step(
                DedupeChunkProcessor(),
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
                response_synthesizer,
                input_map={"query": "query", "chunks": "chunks"},
                output_state="response",
                name="response_synthesizer",
            ),
        ],
        state_type=MultiRetrieverResearchState,
    )


async def main() -> None:
    vector_retriever = create_internal_retriever()
    await ingest_internal_data(vector_retriever)

    web_retriever = await create_web_retriever()
    response_synthesizer = create_response_synthesizer()
    pipeline = build_pipeline(web_retriever, vector_retriever, response_synthesizer)

    result = await pipeline.invoke(
        {
            "query": "How can GL SDK combine internal knowledge with external research?",
            "merged_top_k": 8,
        }
    )

    print(result["response"])
    print("Sources:")
    for chunk in result["chunks"]:
        print(f"- {chunk.metadata.get('source_type')}: {chunk.metadata.get('source')}")


if __name__ == "__main__":
    asyncio.run(main())
