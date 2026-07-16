"""Example of using OneToOneQueryTransformer to rewrite queries for improved retrieval.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/query-transformer
"""

import asyncio

from dotenv import load_dotenv

from gllm_inference.request_processor import build_lm_request_processor
from gllm_inference.schema.lm_output import LMOutput
from gllm_retrieval.query_transformer.one_to_one_query_transformer import OneToOneQueryTransformer

load_dotenv()


def extract_lm_output(result: str | list[str] | dict[str, str | list[str]] | LMOutput) -> str | list[str]:
    if isinstance(result, LMOutput):
        return result.outputs[0].output
    return result  # type: ignore[return-value]


async def main() -> None:
    lmrp = build_lm_request_processor(
        model_id="openai/gpt-5-nano",
        system_template="You are a helpful assistant that rewrites queries for better retrieval. Rewrite the following query. Only output the transformed query.",
        user_template="Query: {query}",
    )

    transformer = OneToOneQueryTransformer(lm_request_processor=lmrp, extract_func=extract_lm_output)

    single_input = "Find recent research on diffusion transformers."
    result = await transformer.transform(single_input)
    print(result[0])


if __name__ == "__main__":
    asyncio.run(main())
