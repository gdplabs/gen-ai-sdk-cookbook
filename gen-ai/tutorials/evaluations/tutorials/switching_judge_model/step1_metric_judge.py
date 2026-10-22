"""Step 1: Switch the model on a metric.

Same eval as Step 0, with the same test case and metric. The only change is the model: GPT instead of the default judge.

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

    completeness = GEvalCompletenessMetric(models=gpt)
    result = await completeness.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
