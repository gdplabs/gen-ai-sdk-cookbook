"""Example of using OneToOneQueryTransformer to rewrite queries for improved retrieval.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/retrieval/query-transformer
"""

import asyncio

from dotenv import load_dotenv

from gllm_inference.lm_invoker import build_lm_invoker
from gllm_retrieval.query_transformer import OneToOneQueryTransformer

load_dotenv()


async def main() -> None:
    """Rewrite a single query using an LM invoker-backed query transformer."""
    lm_invoker = build_lm_invoker(model_id="openai/gpt-5.6-luna").prompt.build(
        system_template="You are a helpful assistant that rewrites queries for better retrieval. Rewrite the following query. Only output the transformed query.",
        user_template="Query: {query}",
    )

    transformer = OneToOneQueryTransformer(lm_invoker=lm_invoker)

    single_input = "Find recent research on diffusion transformers."
    result = await transformer.transform(single_input)
    print(result[0])


if __name__ == "__main__":
    asyncio.run(main())
