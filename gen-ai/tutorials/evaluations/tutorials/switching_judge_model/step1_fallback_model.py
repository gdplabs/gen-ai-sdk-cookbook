"""Step 1: Add a fallback judge to a metric.

GPT judges first. If its call fails, MiMo takes over.

To reproduce a failure, change GPT's model_id to a made-up id such as "openrouter/openai/gpt-6-luna-fake".
An invalid OPENROUTER_API_KEY would not show the fallback: both judges use that key.

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

    with_fallback = GEvalCompletenessMetric(models=gpt, fallback_models=[mimo])
    result = await with_fallback.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
