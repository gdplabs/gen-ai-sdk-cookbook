"""Use multiple judges on a metric.

Passes a list to `models`, so MiMo and GPT both score the same test case.

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
    mimo = build_lm_invoker(
        model_id="openrouter/xiaomi/mimo-v2.6-flash",
        config={"provider": {"order": ["makora"], "allow_fallbacks": False}},
    )
    gpt = build_lm_invoker(model_id="openrouter/openai/gpt-6-luna")

    multi_judge = GEvalCompletenessMetric(models=[mimo, gpt])
    result = await multi_judge.evaluate(RETURNS_CASE)
    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
