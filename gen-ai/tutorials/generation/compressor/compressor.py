"""Compressor quickstart using LLMLinguaCompressor.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/compressor#quickstart
"""

import asyncio

from gllm_generation.compressor import LLMLinguaCompressor


def main() -> None:
    # Choose device_map="cuda" for GPU, or "cpu" if no GPU
    compressor = LLMLinguaCompressor(
        model_name="microsoft/phi-2",
        device_map="cpu",
        rate=0.5,                      # default compression rate (keep ~50%)
        target_token=-1,               # -1 = no strict target; you can set e.g., 800
        use_sentence_level_filter=False,
        use_context_level_filter=True,
        use_token_level_filter=True,
        rank_method="longllmlingua",   # recommended
    )

    instruction = "Answer the question using the provided context."
    context = (
        "Document 1: ... long text ...\n"
        "Document 2: ... long text ...\n"
        "Document 3: ... long text ..."
    )
    query = "What are the main differences between approach A and B?"

    # Optionally override defaults at call time
    options = {
        "rate": 0.4,                   # compress further to ~40%
        # "target_token": 800,         # alternatively, target a specific token count
        # "use_sentence_level_filter": True,
        # "rank_method": "longllmlingua",
    }

    compressed = asyncio.run(compressor.run(
        context=context,
        query=query,
        instruction=instruction,
        options=options,
    ))

    print("Original length:", len(context))
    print("Compressed length:", len(compressed))
    print("Compressed preview:\n", compressed[:500])


if __name__ == "__main__":
    main()
