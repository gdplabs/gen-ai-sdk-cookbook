"""Reference Formatter: filtering chunks with a decisions model.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/reference-formatter#filtering-with-a-decisions-model
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_generation.reference_formatter import DMReferenceFormatter

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
]
response = "Indonesia is a country in Southeast Asia."


async def main() -> None:
    ref_formatter = DMReferenceFormatter.from_config(
        model_id="openrouter/typesafe/jev-1.13", threshold=0.7
    )
    try:
        references = await ref_formatter.format_reference(
            response=response, chunks=candidate_chunks
        )
        print(references)
    finally:
        await ref_formatter.dm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
