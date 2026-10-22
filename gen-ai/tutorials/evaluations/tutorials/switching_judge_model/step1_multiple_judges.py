"""Step 1: Use multiple judges on a metric.

Passes a list to `models`, so GPT, MiMo, and Llama all score the same test case.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    gpt = build_lm_invoker(
        model_id="openrouter/openai/gpt-6-luna",
        config={"provider": {"order": ["openai"], "allow_fallbacks": False}},
    )
    mimo = build_lm_invoker(
        model_id="openrouter/xiaomi/mimo-v2.6-flash",
        config={"provider": {"order": ["makora"], "allow_fallbacks": False}},
    )
    llama = build_lm_invoker(model_id="openrouter/meta-llama/llama-3.3-70b-instruct")

    multi_judge = GEvalCompletenessMetric(models=[gpt, mimo, llama])
    result = await multi_judge.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
