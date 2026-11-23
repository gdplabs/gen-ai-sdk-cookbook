"""Reference Formatter quickstart using SimilarityBasedReferenceFormatter.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/reference-formatter#quickstart
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_inference.em_invoker import build_em_invoker
from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter

load_dotenv()

candidate_chunks = [
    Chunk(
        content="Indonesia is a country in Southeast Asia.",
        metadata={"file_name": "indonesia.txt"},
    ),
    Chunk(
        content="Malaysia is a country in Southeast Asia.",
        metadata={"file_name": "malaysia.txt"},
    ),
    Chunk(
        content="Singapore is a country in Southeast Asia.",
        metadata={"file_name": "singapore.txt"},
    ),
    Chunk(
        content="The capital of Indonesia is Jakarta.",
        metadata={"file_name": "indonesia.txt"},
    ),
    Chunk(
        content="The capital of Malaysia is Kuala Lumpur.",
        metadata={"file_name": "malaysia.txt"},
    ),
    Chunk(
        content="The capital of Singapore is Singapore.",
        metadata={"file_name": "singapore.txt"},
    ),
]
response = (
    "Indonesia is a country in Southeast Asia. "
    "The capital of Indonesia is Jakarta."
)


async def main() -> None:
    em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
    try:
        ref_formatter = SimilarityBasedReferenceFormatter(em_invoker, threshold=0.7)
        references = await ref_formatter.format_reference(
            response=response, chunks=candidate_chunks
        )
        print(references)
    finally:
        await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
