"""Response Synthesizer quickstart using stuff strategy.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#quickstart
"""

import asyncio

from dotenv import load_dotenv

from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    query = "How old is Alex?"
    chunks = [
        Chunk(content="Alex is 25 years old."),
        Chunk(content="Bob is 30 years old."),
    ]

    synthesizer = ResponseSynthesizer.preset.stuff(model_id="openai/gpt-5-nano")
    response = await synthesizer.synthesize(query=query, chunks=chunks)
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
