"""Response Synthesizer: Map Reduce Strategy.

Demonstrates the Map Reduce strategy for processing large amounts of content
in parallel and then combining the results.

Uses the preset configuration for simplicity.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#id-1.-map-reduce
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    query = "Summarize the key features of Python"
    chunks = [
        Chunk(content="Python was created in 1991 by Guido van Rossum."),
        Chunk(content="Python 2.0 was released in 2000."),
        Chunk(
            content="Python 3.0 was released in 2008, breaking backward compatibility."
        ),
    ]

    # Using preset with default map-reduce configuration
    synthesizer = ResponseSynthesizer.map_reduce_preset(
        map_model_id="openai/gpt-5-nano",  # Model for the map phase
        reduce_model_id="openai/gpt-5",  # Model for the reduce phase
        batch_size=2,  # Process 2 chunks at a time in map phase
        max_iterations=10,  # Iterate max 10 times
    )

    response = await synthesizer.synthesize(query=query, chunks=chunks)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
