import asyncio
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()

MODEL_ID = os.getenv("LANGUAGE_MODEL", "openai/gpt-4o-mini")


async def main():
    query = "How old is Alex?"
    chunks = [Chunk(content="Alex is 25 years old."), Chunk(content="Bob is 30 years old.")]

    synthesizer = ResponseSynthesizer.preset.stuff(MODEL_ID)
    response = await synthesizer.synthesize(query=query, chunks=chunks)
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
