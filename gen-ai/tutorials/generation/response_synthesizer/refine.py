"""Response Synthesizer: Refine Strategy.

Demonstrates the Refine strategy for iteratively refining an answer by
processing chunks sequentially.

Uses the preset configuration for simplicity.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#id-2.-refine
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    query = "What is the history of Python?"
    chunks = [
        Chunk(content="Python was created in 1991 by Guido van Rossum."),
        Chunk(content="Python 2.0 was released in 2000."),
        Chunk(
            content="Python 3.0 was released in 2008, breaking backward compatibility."
        ),
    ]

    # Using preset with default refine configuration
    synthesizer = ResponseSynthesizer.refine_preset(
        model_id="openai/gpt-5",
        batch_size=1,  # Process one chunk at a time
        stream_drafts=False,  # Only stream the final response
    )

    response = await synthesizer.synthesize(query=query, chunks=chunks)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
