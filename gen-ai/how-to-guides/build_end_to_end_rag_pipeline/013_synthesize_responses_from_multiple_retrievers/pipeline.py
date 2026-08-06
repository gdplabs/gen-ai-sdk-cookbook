"""Example script to build and run a multi-retriever RAG pipeline.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/synthesize-responses-from-multiple-retrievers
    [2] https://gdplabs.gitbook.io/sdk/gl-smart-search/guides/authentication (for SMART_SEARCH_TOKEN)
"""

import asyncio
import os
from typing import Any, NotRequired, TypedDict

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_generation.repacker import Repacker
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import parallel, step, transform
from gllm_pipeline.types import Val
from gllm_retrieval.chunk_processor import DedupeChunkProcessor
from gllm_retrieval.retriever import SmartSearchWebRetriever, VectorRetriever

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

em_invoker = OpenAIEMInvoker(
    model_name=os.environ["EMBEDDING_MODEL"],
)

def create_internal_retriever() -> VectorRetriever:
    data_store = ChromaDataStore(
        collection_name="internal_research_docs",
        client_type=ChromaClientType.PERSISTENT,
        persist_directory="data/chroma",
    ).with_vector(em_invoker=em_invoker)

    return VectorRetriever(data_store=data_store)


async def ingest_internal_data(vector_retriever: VectorRetriever) -> None:
    """Index sample chunks so this example is runnable from a clean project.

    In production, run ingestion separately; see index-your-data-with-vector-data-store.md.
    """
    chunks = [
        Chunk(
            id="internal-pipeline-overview",
            content="GL SDK pipelines orchestrate steps, parallel branches, and response synthesis.",
            metadata={"source": "internal-docs"},
        ),
        Chunk(
            id="internal-vector-search",
            content="VectorRetriever searches ChromaDB for internal chunks that match a user query.",
            metadata={"source": "internal-docs"},
        ),
        Chunk(
            id="internal-response-synthesis",
            content="ResponseSynthesizer generates an answer from retrieved context chunks.",
            metadata={"source": "internal-docs"},
        ),
    ]
    await vector_retriever.data_store.vector.create(chunks)


async def create_web_retriever() -> SmartSearchWebRetriever:
    return await SmartSearchWebRetriever.create(
        base_url=os.environ["SMART_SEARCH_BASE_URL"],
        token=os.environ["SMART_SEARCH_TOKEN"],
    )


def create_response_synthesizer() -> ResponseSynthesizer:
    lm_invoker = build_lm_invoker(model_id=os.environ["LANGUAGE_MODEL"]).prompt.build(
        system_template=SYSTEM_PROMPT,
        user_template=USER_PROMPT,
    )
    return ResponseSynthesizer.stuff(
        lm_invoker=lm_invoker,
        chunks_repacker=Repacker(mode="chunk"),
    )


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
                        web_retriever,
                        input_map={"query": "query", "top_k": Val(5)},
                        output_state="web_chunks",
                    ),
                    "vector": step(
                        vector_retriever,
                        input_map={"query": "query", "top_k": Val(5)},
                        output_state="vector_chunks",
                    ),
                },
                input_states=["query"],
            ),
            transform(
                combine_retrieved_chunks,
                input_states=["web_chunks", "vector_chunks"],
                output_state="chunks",
            ),
            step(
                DedupeChunkProcessor(),
                input_map={"chunks": "chunks"},
                output_state="chunks",
            ),
            transform(
                limit_chunks,
                input_states=["chunks", "merged_top_k"],
                output_state="chunks",
            ),
            step(
                response_synthesizer,
                input_map={"query": "query", "chunks": "chunks"},
                output_state="response",
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

    try:
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
    finally:
        await response_synthesizer.strategy.lm_invoker.release_resources()
        await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
