import asyncio
from gllm_generation.repacker.repacker import Repacker
from gllm_core.schema import Chunk

def rough_token_count(chunk: Chunk) -> int:
    # Extremely rough token estimate: words * 1.3
    return int(len(str(chunk.content).split()) * 1.3)

async def main():
    chunks = [
        Chunk(content="Short intro."),
        Chunk(content="Detailed middle section with more words."),
        Chunk(content="Final notes.")
    ]
    repacker = Repacker(
        method="sides",
        mode="context",
        delimiter="\n\n",
        size_func=rough_token_count,
        size_limit=10,
    )
    context = await repacker.repack(chunks)
    print(context)

if __name__ == "__main__":
    asyncio.run(main())
