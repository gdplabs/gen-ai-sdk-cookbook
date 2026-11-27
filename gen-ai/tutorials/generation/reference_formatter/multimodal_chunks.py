"""Reference Formatter: multimodal chunks.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/reference-formatter#multimodal-chunks
"""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_generation.reference_formatter import LMReferenceFormatter


async def main() -> None:
    """Judge an image chunk and a text chunk together."""
    load_dotenv()
    image = Path(__file__).parent / "data" / "dog.png"
    candidate_chunks = [
        Chunk(content=image.read_bytes(), metadata={"file_name": "dog.png"}),
        Chunk(
            content="Jakarta is the capital of Indonesia.",
            metadata={"file_name": "indonesia.txt"},
        ),
    ]

    ref_formatter = LMReferenceFormatter.from_preset("openai/gpt-5-nano")
    try:
        references = await ref_formatter.format_reference(
            response="The picture shows a dog.", chunks=candidate_chunks
        )
        print(references)
    finally:
        await ref_formatter.lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
