"""Reference Formatter: Customizing the Similarity Embedding Input.

Demonstrates context_config to control what text is embedded for similarity scoring.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/reference-formatter#customizing-the-similarity-embedding-input
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk, ContextConfig
from gllm_inference.em_invoker import build_em_invoker
from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter

load_dotenv()

candidate_chunks = [
    Chunk(
        content="Indonesia is a country in Southeast Asia.",
        metadata={"file_name": "indonesia.txt"},
    ),
    Chunk(
        content="The capital of Indonesia is Jakarta.",
        metadata={"file_name": "indonesia.txt"},
    ),
]
response = (
    "Indonesia is a country in Southeast Asia. "
    "The capital of Indonesia is Jakarta."
)

context_config = ContextConfig(
    fields=["content", "metadata"],
    template="{content}\nSource: {metadata_json}",
)


async def main() -> None:
    em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
    try:
        ref_formatter = SimilarityBasedReferenceFormatter(
            em_invoker,
            threshold=0.7,
            context_config=context_config,
        )
        references = await ref_formatter.format_reference(
            response=response, chunks=candidate_chunks
        )
        print(references)
    finally:
        await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
