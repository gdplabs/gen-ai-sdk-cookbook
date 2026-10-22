"""Add a fallback judge to a metric.

GPT judges first. If its call fails, MiMo takes over.

To reproduce a failure, give only GPT an invalid key:
    gpt = build_lm_invoker(model_id="openrouter/openai/gpt-6-luna", credentials="sk-or-invalid")
MiMo still reads OPENROUTER_API_KEY from .env, so it can take over.

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
    gpt = build_lm_invoker(model_id="openrouter/openai/gpt-6-luna")
    mimo = build_lm_invoker(
        model_id="openrouter/xiaomi/mimo-v2.6-flash",
        config={"provider": {"order": ["makora"], "allow_fallbacks": False}},
    )

    with_fallback = GEvalCompletenessMetric(models=gpt, fallback_models=[mimo])
    result = await with_fallback.evaluate(RETURNS_CASE)
    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
